from typing import Optional, Union

import torch
import torch.nn as nn
import torch.nn.functional as F

from .bpnet import BPNet
from ._mixins import WeightsIOMixin


class CellStateController(nn.Module):
    """Neural network that generates dynamic convolution biases from cell states.

    This controller network takes cell state embeddings and generates bias terms
    that modulate the dilated convolutions in DynamicBPNet. This allows the
    network to adapt its behavior based on cell-specific features.

    Parameters
    ----------
    in_features : int
        Number of input features (cell state dimensions).
    hidden_dims : int or list[int]
        Either a single integer specifying one hidden layer dimension,
        or a list of integers specifying dimensions of multiple hidden layers.
    out_features : int
        Number of output features (matches total number of convolution channels).
    dropout : float, optional
        Dropout probability between layers. Default is 0.0 (no dropout).
    """

    def __init__(
        self, 
        in_features: int, 
        hidden_dims: Union[int, list[int]],
        out_features: int,
        dropout: float = 0.0
    ):
        super().__init__()
        self.in_features = in_features
        self.hidden_dims = [hidden_dims] if isinstance(hidden_dims, int) else hidden_dims
        self.out_features = out_features
        self.dropout = dropout

        layers = []
        
        # Input layer
        prev_dim = in_features
        
        # Hidden layers
        for hidden_dim in self.hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            prev_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, out_features))
        
        self.layers = nn.ModuleList(layers)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Generate dynamic biases from cell states.

        Parameters
        ----------
        x : torch.Tensor
            Cell state tensor of shape (batch_size, in_features).

        Returns
        -------
        torch.Tensor
            Generated bias terms of shape (batch_size, out_features).
        """
        hidden_layers, output_layer = self.layers[:-1], self.layers[-1]
        # Apply each layer with activation and dropout between hidden layers
        for layer in hidden_layers:
            x = layer(x)
            x = F.relu(x)
            if self.dropout > 0:
                x = F.dropout(x, p=self.dropout, training=self.training)
        x = output_layer(x)
        return x


class DynamicBPNet(BPNet):
    """BPNet variant with cell-state-dependent convolution biases.

    This model extends BPNet by replacing static convolution biases with
    dynamically generated ones based on cell state information. This allows
    the model to adapt its sequence processing behavior to different cell types
    or conditions.

    Parameters
    ----------
    controller : CellStateController
        Controller network that generates dynamic biases.
    hidden_channels : int, default=512
        Number of channels for all convolution layers.
    num_layers : int, default=8
        Number of dilated residual convolution layers.
    **kwargs
        Additional arguments passed to BPNet. See BPNet class for details.

    Notes
    -----
    Unlike the base BPNet, this model:
    1. Does not use static biases in dilated convolutions
    2. Does not include a count prediction head
    3. Requires cell state information during forward pass
    """

    def __init__(
        self,
        controller: CellStateController,
        hidden_channels: int = 512,
        num_layers: int = 8,
        **kwargs,
    ):
        # Initialize with no bias in dilated convs since we'll add dynamic biases
        super().__init__(
            hidden_channels=hidden_channels,
            num_layers=num_layers,
            dilated_conv_bias=False,
            **kwargs,
        )

        self.controller = controller

        # Create separate linear layers for each dilated conv to generate biases
        self.bias_layers = nn.ModuleList(
            [
                nn.Linear(controller.out_features, hidden_channels)
                for _ in range(num_layers)
            ]
        )

        # Remove count predictor since we only need profiles
        delattr(self, "count_head")
    
    def copy_weights_from_model(self, source_model, freeze: bool = False):
        """Copy convolution weights from a source model instance.

        This method copies convolution weights from a source model instance
        into the current DynamicBPNet model. It specifically copies weights for:
        1. The initial convolution layer
        2. The dilated convolution layers
        3. The profile convolution layer

        Parameters
        ----------
        source_model : nn.Module
            Source model instance to copy weights from. Can be a BPNet or DynamicBPNet.
        freeze : bool, default=False
            Whether to freeze the copied weights during training.

        Notes
        -----
        The source model should have compatible architecture (same number of
        layers and matching filter sizes). This method only copies weights for
        convolution layers and does not affect the controller or bias layers.
        """
        # If the source model is a DragoNNFruit model, extract the accessibility component
        if hasattr(source_model, 'accessibility'):
            source_model = source_model.accessibility
        
        # Copy initial convolution weights
        self.initial_conv.weight = nn.Parameter(source_model.initial_conv.weight.clone())
        self.initial_conv.weight.requires_grad = not freeze
        
        if hasattr(source_model.initial_conv, 'bias') and source_model.initial_conv.bias is not None:
            self.initial_conv.bias = nn.Parameter(source_model.initial_conv.bias.clone())
            self.initial_conv.bias.requires_grad = not freeze
        
        # Copy dilated convolution weights
        for i, conv in enumerate(self.dilated_convs):
            if i < len(source_model.dilated_convs):
                source_conv = source_model.dilated_convs[i]
                conv.weight = nn.Parameter(source_conv.weight.clone())
                conv.weight.requires_grad = not freeze
        
        # Copy profile convolution weights
        self.profile_conv.weight = nn.Parameter(source_model.profile_conv.weight.clone())
        self.profile_conv.weight.requires_grad = not freeze
        
        if hasattr(source_model.profile_conv, 'bias') and source_model.profile_conv.bias is not None:
            self.profile_conv.bias = nn.Parameter(source_model.profile_conv.bias.clone())
            self.profile_conv.bias.requires_grad = not freeze

    def forward(self, x: torch.Tensor, cell_states: torch.Tensor) -> torch.Tensor:
        """Forward pass with dynamic biases from cell states.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor of shape (batch_size, in_channels, seq_length)
            containing one-hot encoded DNA sequences.
        cell_states : torch.Tensor
            Cell state tensor of shape (batch_size, controller_in_features)
            used to generate dynamic biases.

        Returns
        -------
        torch.Tensor
            Profile predictions of shape (batch_size, out_channels, output_length).
            The output_length is smaller than seq_length due to convolutions.
        """
        # Get controller output
        controller_output = self.controller(cell_states)

        # Initial convolution (with static bias)
        x = self.initial_conv(x)
        x = F.relu(x)

        # Dilated convolutions with dynamic biases
        for _, (conv, crop, bias_layer) in enumerate(
            zip(self.dilated_convs, self.crops, self.bias_layers)
        ):
            # Generate dynamic bias for this layer
            dynamic_bias = bias_layer(controller_output).unsqueeze(-1)

            # Apply convolution and add dynamic bias
            x_conv = conv(x) + dynamic_bias
            x_conv = F.relu(x_conv)

            # Crop the residual to match conv output
            x = crop(x)
            x = x + x_conv

        # Profile head
        return self.profile_conv(x)


class DragoNNFruit(nn.Module, WeightsIOMixin):
    """Model for interpreting single-cell ATAC-seq data from sequence and cell state information.

    This implementation is based on:
    - https://github.com/jmschrei/dragonnfruit

    This model combines three components:
    1. A bias model (BPNet) that captures Tn5 cutting enzyme sequence preferences
    2. An accessibility model (DynamicBPNet) that processes sequences through convolutions
       with cell-state-dependent parameters
    3. A controller network within the accessibility model that modulates
       convolution parameters based on cell state

    The bias model's parameters are frozen during training, while the
    accessibility model and its controller are trained together.

    Parameters
    ----------
    bias : BPNet
        A pre-trained BPNet model for capturing Tn5 bias, typically trained
        on GC-matched non-peak regions.
    accessibility : DynamicBPNet
        A DynamicBPNet model that processes sequences and is modulated by
        cell state.
    name : str, optional
        Name identifier for the model.

    Notes
    -----
    The model combines outputs as follows:
    final_output = read_depth + bias_profile + accessibility_profile

    where:
    - read_depth accounts for sequencing depth differences
    - bias_profile captures sequence-specific Tn5 bias
    - accessibility_profile represents cell-state-dependent accessibility
    """

    def __init__(
        self, bias: BPNet, accessibility: DynamicBPNet, name: Optional[str] = None
    ):
        super().__init__()

        # Freeze the bias model parameters
        for parameter in bias.parameters():
            parameter.requires_grad = False

        self.bias = bias
        self.accessibility = accessibility
        self.name = name
    
    def copy_weights_from_model(self, source_model, freeze_bias: bool = True, freeze_accessibility: bool = False):
        """Copy weights from a source model instance into both bias and accessibility components.
        
        This method copies weights from a source model instance into both the bias and 
        accessibility components of the DragoNNFruit model. For the bias component, all weights
        are copied and typically frozen. For the accessibility component, only the convolution
        weights are copied, while the controller network remains unchanged.
        
        Parameters
        ----------
        source_model : nn.Module
            Source model instance to copy weights from. Can be a BPNet or DragoNNFruit.
        freeze_bias : bool, default=True
            Whether to freeze the bias model parameters after copying.
            Typically set to True as the bias model should remain fixed.
        freeze_accessibility : bool, default=False
            Whether to freeze the copied accessibility model convolution weights.
            Typically set to False to allow fine-tuning.
            
        Notes
        -----
        This is a convenience method that:
        1. Copies the source model into the bias component (completely replacing it)
        2. Copies only the convolution weights into the accessibility component
        3. Applies the specified freezing settings to each component
        
        The controller network in the accessibility component remains unchanged
        and trainable regardless of the freeze_accessibility setting.
        """
        # Replace the bias model with the source model
        if hasattr(source_model, 'bias'):
            # If the source model is a ChromBPNet / DragoNNFruit model, extract its bias component
            self.bias = source_model.bias
        else:
            raise ValueError("Source model must be a ChromBPNet or DragoNNFruit model and include a bias component.")
            
        # Freeze or unfreeze the bias model parameters
        for parameter in self.bias.parameters():
            parameter.requires_grad = not freeze_bias
            
        # Copy convolution weights into the DynamicBPNet component
        self.accessibility.copy_weights_from_model(source_model, freeze=freeze_accessibility)

    def forward(
        self, X: torch.Tensor, cell_states: torch.Tensor, read_depths: torch.Tensor
    ) -> torch.Tensor:
        """Forward pass through the model.

        Parameters
        ----------
        X : torch.Tensor
            Input tensor of shape (batch_size, in_channels, seq_length)
            containing one-hot encoded DNA sequences.
        cell_states : torch.Tensor
            Cell state tensor of shape (batch_size, controller_in_features)
            that modulates the accessibility model.
        read_depths : torch.Tensor
            Read depth tensor of shape (batch_size, 1) containing log-scaled
            sequencing depth per cell or group of cells.

        Returns
        -------
        torch.Tensor
            Predicted logit profiles of shape (batch_size, profile_length)
            combining bias, accessibility, and read depth effects.
        """

        bias_profile, _ = self.bias(X)
        accessibility_profile = self.accessibility(X, cell_states)

        # Add read depths, bias profile (first channel), and accessibility profile
        return read_depths.unsqueeze(-1) + bias_profile + accessibility_profile


__all__ = ["DragoNNFruit", "DynamicBPNet", "CellStateController"]
