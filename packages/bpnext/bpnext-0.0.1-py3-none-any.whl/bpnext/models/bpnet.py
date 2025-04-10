from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from ._mixins import WeightsIOMixin


class Crop1d(nn.Module):
    """1D cropping layer that crops equal amounts from both sides.

    This layer is used to match the dimensions of residual connections
    in the BPNet architecture by removing equal amounts of data from
    both ends of the sequence.

    Parameters
    ----------
    crop_size : int
        Number of elements to remove from each end of the sequence.
    """

    def __init__(self, crop_size: int):
        super().__init__()
        self.crop_size = crop_size

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Crop input tensor symmetrically.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor of shape (batch_size, channels, length)

        Returns
        -------
        torch.Tensor
            Cropped tensor of shape (batch_size, channels, length - 2*crop_size)
        """
        return x[:, :, self.crop_size : -self.crop_size]


class BPNet(nn.Module, WeightsIOMixin):
    """Base neural network for predicting TF binding profiles from DNA sequences.

    This implementation is based on:
    - https://github.com/jmschrei/bpnet-lite
    - https://github.com/kundajelab/chrombpnet (original TensorFlow implementation)

    The model consists of:
    1. An initial convolution layer to process raw DNA sequences
    2. A series of dilated convolutions with residual connections
    3. Two prediction heads:
       - Profile head: predicts binding profile at each position
       - Count head: predicts total binding counts

    Note: Unlike bpnet-lite which uses output trimming, this implementation uses
    cropping of residual connections. This may lead to slight numerical differences
    in the outputs, particularly near the sequence edges, when compared to bpnet-lite.

    Parameters
    ----------
    hidden_channels : int, default=512
        Number of channels for all convolution layers.
    num_layers : int, default=8
        Number of dilated residual convolution layers.
    in_channels : int, default=4
        Number of input channels (e.g. 4 for one-hot encoded DNA sequences).
    out_channels : int, default=1
        Number of output channels in the profile head.
    num_control_tracks : int, default=0
        Number of control tracks to be concatenated with the learned features.
    initial_conv_kernel_size : int, default=21
        Kernel size for the initial convolution.
    residual_block_kernel_size : int, default=3
        Kernel size for the dilated residual blocks.
    profile_conv_kernel_size : int, default=75
        Kernel size for the final profile head convolution.
    dilation_rate : int, default=2
        Base dilation rate. The dilation at layer ``i`` is computed as: dilation_rate ** (i+1)
    alpha : float, default=1.0
        Scaling factor for the loss function.
    profile_output_bias : bool, default=True
        Whether to include a bias term in the profile head.
    count_output_bias : bool, default=True
        Whether to include a bias term in the count head.
    initial_conv_bias : bool, default=True
        Whether to include a bias term for the initial convolution.
    dilated_conv_bias : bool, default=True
        Whether to include bias terms in the dilated convolutions.
    name : str, optional
        Name of the model instance.
    """

    def __init__(
        self,
        hidden_channels: int = 512,
        num_layers: int = 8,
        *,
        in_channels: int = 4,  # 4 nucleotides
        out_channels: int = 1,
        num_control_tracks: int = 0,
        initial_conv_kernel_size: int = 21,
        residual_block_kernel_size: int = 3,
        profile_conv_kernel_size: int = 75,
        dilation_rate: int = 2,
        alpha: float = 1.0,
        profile_output_bias: bool = True,
        count_output_bias: bool = True,
        initial_conv_bias: bool = True,
        dilated_conv_bias: bool = True,
        name: Optional[str] = None,
    ):
        """
        Initialize the BPNet model.

        See class docstring for parameter descriptions.
        """
        super().__init__()
        self.hidden_channels = hidden_channels
        self.num_layers = num_layers

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_control_tracks = num_control_tracks

        self.initial_conv_kernel_size = initial_conv_kernel_size
        self.residual_block_kernel_size = residual_block_kernel_size
        self.profile_kernel_size = profile_conv_kernel_size

        self.dilation_rate = dilation_rate
        self.alpha = alpha

        self.profile_output_bias = profile_output_bias
        self.count_output_bias = count_output_bias
        self.initial_conv_bias = initial_conv_bias
        self.dilated_conv_bias = dilated_conv_bias

        self.name = name or f"bpnet.{hidden_channels}.{num_layers}"

        # Initial convolution
        self.initial_conv = nn.Conv1d(
            in_channels=in_channels,
            out_channels=hidden_channels,
            kernel_size=initial_conv_kernel_size,
            padding="valid",
            bias=initial_conv_bias,
        )

        # Dilated convolution blocks with residual connections
        self.dilated_convs = nn.ModuleList()
        self.crops = nn.ModuleList()

        for i in range(self.num_layers):
            dilation = self.dilation_rate ** (i + 1)
            padding = 0  # Use no padding for dilated convs

            conv = nn.Conv1d(
                in_channels=hidden_channels,
                out_channels=hidden_channels,
                kernel_size=self.residual_block_kernel_size,
                padding=padding,
                dilation=dilation,
                bias=self.dilated_conv_bias,
            )
            self.dilated_convs.append(conv)

            # Crop layer for residual connection
            crop_size = ((self.residual_block_kernel_size - 1) * dilation) // 2
            self.crops.append(Crop1d(crop_size))
    
        out_crop_size = (self.profile_kernel_size - 1) // 2
        self.out_crop = Crop1d(out_crop_size)

        # Profile head
        n_channels = (
            hidden_channels + num_control_tracks
            if num_control_tracks > 0
            else hidden_channels
        )
        self.profile_conv = nn.Conv1d(
            in_channels=n_channels,
            out_channels=self.out_channels,
            kernel_size=self.profile_kernel_size,
            padding=0,
            bias=self.profile_output_bias,
        )

        # Count head
        n_count_features = (
            hidden_channels + 1 if num_control_tracks > 0 else hidden_channels
        )
        self.count_head = nn.Linear(
            in_features=n_count_features, out_features=out_channels, bias=self.count_output_bias
        )

    def forward(
        self, X: torch.Tensor, X_ctl: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the network.

        Parameters
        ----------
        X : torch.Tensor
            Input tensor of shape (batch_size, in_channels, seq_length)
            containing one-hot encoded DNA sequences.
        X_ctl : torch.Tensor, optional
            Control track tensor of shape (batch_size, num_control_tracks, seq_length).
            Default is None.

        Returns
        -------
        y_profile : torch.Tensor
            Profile predictions of shape (batch_size, out_channels, output_length).
            The output_length is smaller than seq_length due to convolutions.
        y_counts : torch.Tensor
            Count predictions of shape (batch_size, out_channels).
        """
        # Initial convolution
        x = self.initial_conv(X)
        x = F.relu(x)

        # Dilated convolutions with residual connections
        for conv, crop in zip(self.dilated_convs, self.crops):
            x_conv = conv(x)
            x_conv = F.relu(x_conv)
            x = crop(x)  # Crop the residual to match conv output
            x = x + x_conv
        
        # (1) Profile head

        # Add control tracks if provided
        if X_ctl is not None:
            # Crop control tracks to match current feature map size
            crop_size = (X.shape[2] - x.shape[2]) // 2
            X_ctl = X_ctl[:, :, crop_size : X_ctl.shape[2] - crop_size]
            x_w_ctl = torch.cat([x, X_ctl], dim=1)
            y_profile = self.profile_conv(x_w_ctl)
        else:
            y_profile = self.profile_conv(x)

        # (2) Counts head

        # Global average pooling
        x_mean = torch.mean(self.out_crop(x), dim=2)

        if X_ctl is not None:
            # Sum control tracks and add to count features
            x_ctl_sum = torch.sum(self.out_crop(X_ctl), dim=(1, 2))
            x_mean = torch.cat([x_mean, torch.log1p(x_ctl_sum).unsqueeze(-1)], dim=-1)

        y_counts = self.count_head(x_mean)

        return y_profile, y_counts

    def _get_output_padding(self) -> int:
        """Calculate total padding/cropping of the model output.
        
        Returns
        -------
        int
            Number of positions removed from input sequence length
        """
        # Initial conv padding
        padding = self.initial_conv_kernel_size - 1
        
        # Dilated convs padding
        for i in range(self.num_layers):
            dilation = self.dilation_rate ** (i + 1)
            padding += 2 * ((self.residual_block_kernel_size - 1) * dilation // 2)
        
        # Profile conv padding
        padding += self.profile_kernel_size - 1
        
        return padding
