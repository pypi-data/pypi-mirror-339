"""
Functions for loading BPNet models from legacy HDF5 files.

Adapted from https://github.com/jmschrei/bpnet-lite.
"""

import torch
import torch.nn as nn
from pathlib import Path
from functools import wraps
from typing import Union, Dict, Optional, Callable, TypeVar, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import h5py
    from ..models.bpnet import BPNet
    from ..models.chrombpnet import ChromBPNet
    from ..models.dragonnfruit import DragoNNFruit, DynamicBPNet

# Model type names
_BPNET = "bpnet"
_CHROMBPNET = "chrombpnet"
_DRAGONNFRUIT = "dragonnfruit"
_DYNAMICBPNET = "dynamicbpnet"

F = TypeVar("F", bound=Callable[..., Any])


def _requires_h5py(func: F) -> F:
    """Decorator that ensures h5py is available."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            import h5py  # noqa: F401

            return func(*args, **kwargs)
        except ImportError:
            raise ImportError(
                f"h5py is required for {func.__name__}. "
                "Please install it with: pip install h5py"
            )

    return wrapper  # type: ignore


class _H5WeightWriter:
    """Helper class for writing weights to HDF5 files."""

    def __init__(self, group: "h5py.Group"):
        self.group = group

    def add_weights(
        self, name: str, weight: torch.Tensor, bias: Optional[torch.Tensor] = None
    ) -> None:
        """Add weight and optional bias to a layer."""
        group = self.group.create_group(f"{name}/{name}")
        group.create_dataset("kernel:0", data=weight.detach().numpy())
        if bias is not None:
            group.create_dataset("bias:0", data=bias.detach().numpy())


@_requires_h5py
def read_h5_weights(
    filename: Union[str, Path], model: nn.Module
) -> Dict[str, torch.Tensor]:
    """Read weights from a legacy HDF5 file into a state dict.

    Parameters
    ----------
    filename: str or Path
        Path to the HDF5 file containing trained model parameters
    model: nn.Module
        Model instance to determine the appropriate reading strategy

    Returns
    -------
    dict
        PyTorch state dictionary containing model weights

    Raises
    ------
    ImportError
        If h5py is not installed
    ValueError
        If model type is not supported
    """
    model_type = model.__class__.__name__.lower()
    if model_type == _BPNET:
        return _read_bpnet_weights_from_h5(filename)
    elif model_type == _DYNAMICBPNET:
        return _read_dynamicbpnet_weights_from_h5(filename)
    elif model_type == _CHROMBPNET:
        return _read_chrombpnet_weights_from_h5(filename)
    elif model_type == _DRAGONNFRUIT:
        return _read_dragonnfruit_weights_from_h5(filename)
    else:
        raise ValueError(f"Unsupported model type for HDF5 loading: {model_type}")


@_requires_h5py
def _read_bpnet_weights_from_h5(
    source: Union[str, Path, "h5py.Group"], 
    prefix: Optional[str] = None
) -> Dict[str, torch.Tensor]:
    """Read BPNet weights from a legacy TensorFlow HDF5 file into a state dict.

    The HDF5 structure for BPNet is:
    /model_weights/
        bpnet_1st_conv/
            kernel:0
            bias:0
        bpnet_1conv/
            kernel:0
            bias:0
        ...
        prof_out_precrop/
            kernel:0
            bias:0

    Parameters
    ----------
    source: str, Path, or h5py.Group
        Path to the HDF5 file or HDF5 group containing trained model parameters
    prefix: str, optional, default=None
        Prefix for layer names (e.g., "wo_bias_")

    Returns
    -------
    dict
        PyTorch state dictionary containing model weights
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "r") as h5:
            weights = h5["model_weights"]
            return _read_bpnet_weights_from_h5(weights, prefix)
    
    # If source is an HDF5 group, process it directly
    weights = source
    state_dict = {}
    
    if prefix is None:
        # Determine prefix based on model version
        if "bpnet_1conv" in weights.keys():
            prefix = ""
        else:
            prefix = "wo_bias_"

    def read_layer(
        name: str, weight_key: str, bias_key: str, is_conv: bool = True
    ) -> None:
        """Helper to read a layer's weights and bias."""
        layer = weights[f"{prefix}{name}/{prefix}{name}"]
        weight = torch.tensor(layer["kernel:0"][:])
        if is_conv:
            weight = weight.permute(2, 1, 0)
        else:
            weight = weight.T
        state_dict[weight_key] = weight
        if "bias:0" in layer:
            state_dict[bias_key] = torch.tensor(layer["bias:0"][:])

    # Initial convolution
    read_layer("bpnet_1st_conv", "initial_conv.weight", "initial_conv.bias")

    # Dilated convolutions
    i = 1
    while f"{prefix}bpnet_{i}conv" in weights:
        read_layer(
            f"bpnet_{i}conv", f"dilated_convs.{i-1}.weight", f"dilated_convs.{i-1}.bias"
        )
        i += 1

    # Profile head (conv)
    read_layer("prof_out_precrop", "profile_conv.weight", "profile_conv.bias")

    # Count head (linear)
    count_layer_name = "logcount_predictions"
    if f"{prefix}{count_layer_name}" in weights:
        read_layer(
            count_layer_name,
            "count_head.weight",
            "count_head.bias",
            is_conv=False,
        )

    return state_dict


@_requires_h5py
def _read_dynamicbpnet_weights_from_h5(
    source: Union[str, Path, "h5py.Group"],
    prefix: Optional[str] = None
) -> Dict[str, torch.Tensor]:
    """Read DynamicBPNet weights from a legacy TensorFlow HDF5 file into a state dict.

    The HDF5 structure for DynamicBPNet is similar to BPNet but includes:
    - No count head
    - No bias in dilated convolutions
    - Additional bias_layer groups for dynamic biases
    - A controller network for generating bias terms

    Parameters
    ----------
    source: str, Path, or h5py.Group
        Path to the HDF5 file or HDF5 group containing trained model parameters
    prefix: str, optional, default=None
        Prefix for layer names (e.g., "wo_bias_")

    Returns
    -------
    dict
        PyTorch state dictionary containing model weights
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "r") as h5:
            weights = h5["model_weights"]
            return _read_dynamicbpnet_weights_from_h5(weights, prefix)
    
    # If source is an HDF5 group, process it directly
    weights = source
    state_dict = {}
    
    if prefix is None:
        # Determine prefix based on model version
        if "bpnet_1conv" in weights.keys():
            prefix = ""
        else:
            prefix = "wo_bias_"

    def read_layer(
        name: str, weight_key: str, bias_key: str, is_conv: bool = True
    ) -> None:
        """Helper to read a layer's weights and bias."""
        layer = weights[f"{prefix}{name}/{prefix}{name}"]
        weight = torch.tensor(layer["kernel:0"][:])
        if is_conv:
            weight = weight.permute(2, 1, 0)
        else:
            weight = weight.T
        state_dict[weight_key] = weight
        if "bias:0" in layer:
            state_dict[bias_key] = torch.tensor(layer["bias:0"][:])

    # Initial convolution
    read_layer("bpnet_1st_conv", "initial_conv.weight", "initial_conv.bias")

    # Dilated convolutions (without bias) and bias layers
    i = 1
    while f"{prefix}bpnet_{i}conv" in weights:
        # Read dilated convolution weights (no bias)
        layer = weights[f"{prefix}bpnet_{i}conv/{prefix}bpnet_{i}conv"]
        weight = torch.tensor(layer["kernel:0"][:]).permute(2, 1, 0)
        state_dict[f"dilated_convs.{i-1}.weight"] = weight
        
        # Read bias_layer weights and bias
        if f"{prefix}bias_layer_{i}" in weights:
            bias_layer = weights[f"{prefix}bias_layer_{i}/{prefix}bias_layer_{i}"]
            # For linear layers, the kernel needs to be transposed
            weight = torch.tensor(bias_layer["kernel:0"][:]).T
            state_dict[f"bias_layers.{i-1}.weight"] = weight
            
            if "bias:0" in bias_layer:
                bias = torch.tensor(bias_layer["bias:0"][:])
                state_dict[f"bias_layers.{i-1}.bias"] = bias
        
        i += 1

    # Profile head (conv)
    read_layer("prof_out_precrop", "profile_conv.weight", "profile_conv.bias")

    # Read controller weights if present
    if f"{prefix}controller" in weights:
        controller_group = weights[f"{prefix}controller"]
        controller_weights = _read_linear_weights_from_h5(controller_group)
        for key, value in controller_weights.items():
            state_dict[f"controller.{key}"] = value

    return state_dict


@_requires_h5py
def _read_chrombpnet_weights_from_h5(
    source: Union[str, Path, "h5py.Group"],
) -> Dict[str, torch.Tensor]:
    """Read ChromBPNet weights from a legacy HDF5 file.

    Parameters
    ----------
    source: str, Path, or h5py.Group
        Path to the HDF5 file containing trained model parameters
        or an HDF5 group containing trained model parameters

    Returns
    -------
    dict
        PyTorch state dictionary containing model weights
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "r") as h5:
            weights = h5["model_weights"]
            return _read_chrombpnet_weights_from_h5(weights)
    
    state_dict = {}
    
    # Check for combined ChromBPNet model with nested structure
    if "model" in source and "model_wo_bias" in source:
        # Load bias model (no prefix, nested under model/)
        bias_weights = _read_bpnet_weights_from_h5(source["model"], prefix="")
        for key, value in bias_weights.items():
            state_dict[f"bias.{key}"] = value
            
        # Load accessibility model (with wo_bias_ prefix, nested under model_wo_bias/)
        acc_weights = _read_bpnet_weights_from_h5(source["model_wo_bias"], prefix="wo_bias_")
        for key, value in acc_weights.items():
            state_dict[f"accessibility.{key}"] = value
    
    else:
        # This is a single BPNet model, which should be loaded as a BPNet model accordingly
        raise ValueError("The HDF5 file appears to contain a single BPNet model, which should be loaded as a BPNet model accordingly")

    return state_dict



@_requires_h5py
def _read_linear_weights_from_h5(
    source: Union[str, Path, "h5py.Group"]
) -> Dict[str, torch.Tensor]:
    """Read weights from linear layers in an HDF5 file or group.
    
    This function is designed to read weights from a controller network that consists
    of multiple linear layers stacked together. It handles both single linear layers
    and more complex architectures with multiple hidden layers.
    
    Parameters
    ----------
    source: str, Path, or h5py.Group
        Path to the HDF5 file or HDF5 group containing trained model parameters
        
    Returns
    -------
    dict
        PyTorch state dictionary containing model weights for the linear layers
    """
    import h5py
    
    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "r") as h5:
            return _read_linear_weights_from_h5(h5)
    
    # If source is an HDF5 group, process it directly
    state_dict = {}
    
    # Check if this is a sequential model structure
    if "sequential" in source:
        # Process sequential model structure
        sequential = source["sequential"]
        layer_idx = 0
        
        # Find all dense layers in the sequential group
        dense_layers = sorted([k for k in sequential.keys() if k.startswith("dense_")])
        
        for layer_name in dense_layers:
            layer = sequential[layer_name]
            
            if "kernel:0" in layer:
                # For linear layers, the kernel needs to be transposed
                weight = torch.tensor(layer["kernel:0"][:]).T
                state_dict[f"layers.{layer_idx}.weight"] = weight
                
                # Add bias if present
                if "bias:0" in layer:
                    bias = torch.tensor(layer["bias:0"][:])
                    state_dict[f"layers.{layer_idx}.bias"] = bias
                
                layer_idx += 1
    else:
        # Process flat structure or direct layer access
        for layer_name in source.keys():
            # Skip non-layer entries
            if not isinstance(source[layer_name], h5py.Group):
                continue
                
            layer = source[layer_name]
            
            # Check if this is a linear layer (has kernel and possibly bias)
            if "kernel:0" in layer:
                # For linear layers, the kernel needs to be transposed
                weight = torch.tensor(layer["kernel:0"][:]).T
                state_dict["layers.0.weight"] = weight
                
                # Add bias if present
                if "bias:0" in layer:
                    bias = torch.tensor(layer["bias:0"][:])
                    state_dict["layers.0.bias"] = bias
            
            # Handle nested layers
            elif any(isinstance(layer[subname], h5py.Group) for subname in layer.keys()):
                # Find all dense layers in the nested structure
                dense_layers = []
                for subname in layer.keys():
                    if isinstance(layer[subname], h5py.Group) and "kernel:0" in layer[subname]:
                        dense_layers.append(subname)
                
                # Sort dense layers if they have numeric indices
                dense_layers = sorted(dense_layers, key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else 0)
                
                for i, subname in enumerate(dense_layers):
                    sublayer = layer[subname]
                    if "kernel:0" in sublayer:
                        weight = torch.tensor(sublayer["kernel:0"][:]).T
                        state_dict[f"layers.{i}.weight"] = weight
                        
                        if "bias:0" in sublayer:
                            bias = torch.tensor(sublayer["bias:0"][:])
                            state_dict[f"layers.{i}.bias"] = bias
    
    return state_dict


@_requires_h5py
def _read_dragonnfruit_weights_from_h5(
    source: Union[str, Path, "h5py.Group"],
) -> Dict[str, torch.Tensor]:
    """Read DragoNNFruit weights from a legacy HDF5 file.

    Parameters
    ----------
    source: str, Path, or h5py.Group
        Path to the HDF5 file containing trained model parameters
        or an HDF5 group containing trained model parameters

    Returns
    -------
    dict
        PyTorch state dictionary containing model weights
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "r") as h5:
            weights = h5["model_weights"]
            return _read_dragonnfruit_weights_from_h5(weights)

    state_dict = {}
    
    # Load bias model weights (regular BPNet)
    bias_weights = _read_bpnet_weights_from_h5(source["model"], prefix="")
    for key, value in bias_weights.items():
        state_dict[f"bias.{key}"] = value

    # Load accessibility model weights (DynamicBPNet)
    acc_weights = _read_dynamicbpnet_weights_from_h5(source["model_wo_bias"], prefix="wo_bias_")
    for key, value in acc_weights.items():
        state_dict[f"accessibility.{key}"] = value

    print(state_dict.keys())
    return state_dict


@_requires_h5py
def write_h5_weights(filename: Union[str, Path], model: nn.Module) -> None:
    """Write model weights to a legacy HDF5 file format.

    Parameters
    ----------
    filename : str or Path
        Path to save the HDF5 file
    model : nn.Module
        Model whose weights to save

    Raises
    ------
    ImportError
        If h5py is not installed
    ValueError
        If model type is not supported
    """
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    model_type = model.__class__.__name__.lower()
    if model_type == _BPNET:
        _write_bpnet_weights_to_h5(path, model)
    elif model_type == _DYNAMICBPNET:
        _write_dynamicbpnet_weights_to_h5(path, model)
    elif model_type == _CHROMBPNET:
        _write_chrombpnet_weights_to_h5(path, model)
    elif model_type == _DRAGONNFRUIT:
        _write_dragonnfruit_weights_to_h5(path, model)
    else:
        raise ValueError(f"Unsupported model type for HDF5 saving: {model_type}")


@_requires_h5py
def _write_bpnet_weights_to_h5(
    source: Union[str, Path, "h5py.Group"], model: "BPNet", prefix: str = ""
) -> None:
    """Write BPNet weights to a legacy TensorFlow HDF5 format.

    Parameters
    ----------
    source : str, Path, or h5py.Group
        Path to save the HDF5 file or HDF5 group to write to
    model : BPNet
        BPNet model whose weights to save
    prefix : str, optional
        Prefix for layer names (e.g., "wo_bias_")
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "w") as h5:
            weights = h5.create_group("model_weights")
            _write_bpnet_weights_to_h5(weights, model, prefix)
            return
    
    writer = _H5WeightWriter(source)

    # Initial convolution
    writer.add_weights(
        f"{prefix}bpnet_1st_conv",
        model.initial_conv.weight.permute(2, 1, 0),
        model.initial_conv.bias,
    )

    # Dilated convolutions
    for i, conv in enumerate(model.dilated_convs, 1):
        writer.add_weights(
            f"{prefix}bpnet_{i}conv", 
            conv.weight.permute(2, 1, 0), 
            conv.bias
        )

    # Profile and count heads
    writer.add_weights(
        f"{prefix}prof_out_precrop",
        model.profile_conv.weight.permute(2, 1, 0),
        model.profile_conv.bias,
    )
    
    # Only write count head if it exists
    if hasattr(model, "count_head"):
        writer.add_weights(
            f"{prefix}logcount_predictions",
            model.count_head.weight.T,
            model.count_head.bias,
        )


@_requires_h5py
def _write_dynamicbpnet_weights_to_h5(
    source: Union[str, Path, "h5py.Group"], model: "DynamicBPNet", prefix: str = "wo_bias_"
) -> None:
    """Write DynamicBPNet weights to a legacy TensorFlow HDF5 format.

    Parameters
    ----------
    source : str, Path, or h5py.Group
        Path to save the HDF5 file or HDF5 group to write to
    model : DynamicBPNet
        DynamicBPNet model whose weights to save
    prefix : str, optional
        Prefix for layer names, defaults to "wo_bias_"
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "w") as h5:
            weights = h5.create_group("model_weights")
            _write_dynamicbpnet_weights_to_h5(weights, model, prefix)
            return
    
    # If source is an HDF5 group, process it directly
    weights = source
    writer = _H5WeightWriter(weights)

    # Initial convolution
    writer.add_weights(
        f"{prefix}bpnet_1st_conv",
        model.initial_conv.weight.permute(2, 1, 0),
        model.initial_conv.bias,
    )

    # Dilated convolutions (without bias) and bias layers
    for i, (conv, bias_layer) in enumerate(zip(model.dilated_convs, model.bias_layers), 1):
        # Write dilated convolution weights (no bias)
        group = weights.create_group(f"{prefix}bpnet_{i}conv/{prefix}bpnet_{i}conv")
        group.create_dataset("kernel:0", data=conv.weight.permute(2, 1, 0).detach().numpy())
        
        # Write bias_layer weights and bias
        bias_group = weights.create_group(f"{prefix}bias_layer_{i}/{prefix}bias_layer_{i}")
        bias_group.create_dataset("kernel:0", data=bias_layer.weight.T.detach().numpy())
        if bias_layer.bias is not None:
            bias = torch.tensor(bias_layer.bias.detach().numpy())
            bias_group.create_dataset("bias:0", data=bias)

    # Profile head
    writer.add_weights(
        f"{prefix}prof_out_precrop",
        model.profile_conv.weight.permute(2, 1, 0),
        model.profile_conv.bias,
    )
    
    # Write controller weights
    controller_group = weights.create_group(f"{prefix}controller")
    _write_linear_weights_to_h5(controller_group, model.controller)


@_requires_h5py
def _write_chrombpnet_weights_to_h5(
    source: Union[str, Path, "h5py.Group"], model: "ChromBPNet"
) -> None:
    """Write ChromBPNet weights to a legacy HDF5 format.
    
    Parameters
    ----------
    source : str, Path, or h5py.Group
        Path to save the HDF5 file or HDF5 group to write to
    model : ChromBPNet
        ChromBPNet model whose weights to save
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "w") as h5:
            weights = h5.create_group("model_weights")
            _write_chrombpnet_weights_to_h5(weights, model)
            return
    
    # If source is an HDF5 group, process it directly
    # Create groups for bias and accessibility models using the nested structure
    bias_group = source.create_group("model/")
    acc_group = source.create_group("model_wo_bias/")

    # Save bias model weights (no prefix)
    _write_bpnet_weights_to_h5(bias_group, model.bias)

    # Save accessibility model weights (with wo_bias_ prefix)
    _write_bpnet_weights_to_h5(acc_group, model.accessibility, prefix="wo_bias_")


@_requires_h5py
def _write_linear_weights_to_h5(
    source: Union[str, Path, "h5py.Group"], controller: nn.Module
) -> None:
    """Write controller network weights to an HDF5 file or group.
    
    This function writes weights from a controller network with multiple linear layers
    to an HDF5 file or group. It handles both simple linear layers and more complex 
    architectures with multiple hidden layers organized in a sequential structure.
    
    Parameters
    ----------
    source : str, Path, or h5py.Group
        Path to save the HDF5 file or HDF5 group to write to
    controller : nn.Module
        Controller network whose weights to save
    """
    import h5py
    
    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "w") as h5:
            _write_linear_weights_to_h5(h5, controller)
            return
    
    # If source is an HDF5 group, process it directly
    group = source
    
    # Get the state dict of the controller
    state_dict = controller.state_dict()
    
    # Determine if this is a simple linear layer or a sequential model
    is_sequential = any("layers." in key for key in state_dict.keys())
    
    if is_sequential:
        # Create a sequential group
        seq_group = group.create_group("sequential")
        
        # Group the layers by their index in the sequential module
        layer_indices = set()
        for key in state_dict.keys():
            if "layers." in key:
                # Extract the layer index from keys like "layers.0.weight"
                parts = key.split(".")
                if len(parts) >= 2 and parts[1].isdigit():
                    layer_indices.add(int(parts[1]))
        
        # Process each layer in order
        for idx in sorted(layer_indices):
            # Check if this is a linear layer (has weight and possibly bias)
            if f"layers.{idx}.weight" in state_dict:
                # Create a dense layer group with a name based on the index
                dense_group = seq_group.create_group(f"dense_{idx}")
                
                # Add weight (transposed to match TensorFlow convention)
                weight = state_dict[f"layers.{idx}.weight"].detach().numpy().T
                dense_group.create_dataset("kernel:0", data=weight)
                
                # Add bias if present
                if f"layers.{idx}.bias" in state_dict:
                    bias = state_dict[f"layers.{idx}.bias"].detach().numpy()
                    dense_group.create_dataset("bias:0", data=bias)
    else:
        # This is a simple model with direct layer access
        # Create a single layer group
        layer_group = group.create_group("dense")
        
        # Add weight and bias
        if "weight" in state_dict:
            weight = state_dict["weight"].detach().numpy().T
            layer_group.create_dataset("kernel:0", data=weight)
        
        if "bias" in state_dict:
            bias = state_dict["bias"].detach().numpy()
            layer_group.create_dataset("bias:0", data=bias)


@_requires_h5py
def _write_dragonnfruit_weights_to_h5(
    source: Union[str, Path, "h5py.Group"], model: "DragoNNFruit"
) -> None:
    """Write DragoNNFruit weights to a legacy HDF5 format.
    
    Parameters
    ----------
    source : str, Path, or h5py.Group
        Path to save the HDF5 file or HDF5 group to write to
    model : DragoNNFruit
        DragoNNFruit model whose weights to save
    """
    import h5py

    # Check if source is a file path or an HDF5 group
    if isinstance(source, (str, Path)):
        with h5py.File(source, "w") as h5:
            weights = h5.create_group("model_weights")
            _write_dragonnfruit_weights_to_h5(weights, model)
            return
    
    # If source is an HDF5 group, process it directly
    # Save bias model (regular BPNet)
    bias_group = source.create_group("model/")
    _write_bpnet_weights_to_h5(bias_group, model.bias)

    # Save accessibility model (DynamicBPNet)
    acc_group = source.create_group("model_wo_bias/")
    _write_dynamicbpnet_weights_to_h5(acc_group, model.accessibility, prefix="wo_bias_")

