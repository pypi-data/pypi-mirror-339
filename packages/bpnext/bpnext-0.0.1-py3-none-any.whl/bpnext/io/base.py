"""Base I/O functionality for model weights."""

from pathlib import Path
from typing import Union, Optional, Dict, Any
import torch
import torch.nn as nn
import warnings


def load_weights(
    model: nn.Module, filename: Union[str, Path], format: Optional[str] = None
) -> None:
    """Load weights from a file into a model.

    Parameters
    ----------
    model : nn.Module
        Model to load weights into
    filename : str or Path
        Path to the file containing trained model parameters
    format : str, optional
        Format of the weights file. If None, will be inferred from file extension.
        Supported formats:
        - "h5", "hdf5": Legacy TensorFlow HDF5 format
        - "pt", "pth": PyTorch saved state dict
        - "dbsf": DBSF binary storage format
    """
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"No such file: '{path}'")

    # Infer format from file extension if not specified
    if format is None:
        format = path.suffix[1:]  # Remove leading dot using pathlib

    # Map similar extensions to same format
    format_map = {"h5": "h5", "hdf5": "h5", "pt": "pth", "pth": "pth", "dbsf": "dbsf"}

    format = format_map.get(format.lower())
    if format not in format_map.values():
        raise ValueError(
            f"Unsupported format: {format}. "
            f"Supported formats are: {', '.join(set(format_map.values()))}"
        )

    # Load state dict based on format
    if format == "h5":
        from .hdf5 import read_h5_weights

        state_dict = read_h5_weights(path, model)
        model.load_state_dict(state_dict)
    elif format == "pth":
        state_dict = torch.load(path)
        model.load_state_dict(state_dict)
    elif format == "dbsf":
        from .dbsf import load_into_model

        load_into_model(model, path)


def save_weights(
    model: nn.Module, 
    filename: Union[str, Path], 
    format: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """Save model weights to a file.

    Parameters
    ----------
    model : nn.Module
        Model whose weights to save
    filename : str or Path
        Path to save the weights file
    format : str, optional
        Format to save in. If None, will be inferred from file extension.
        Supported formats:
        - "h5", "hdf5": Legacy TensorFlow HDF5 format
        - "pt", "pth": PyTorch state dict
        - "dbsf": DBSF binary storage format
    metadata : Dict[str, Any], optional
        Additional metadata to store with the model. 
        **Note**: Metadata is only supported in DBSF format and will be ignored for HDF5 and PyTorch formats.

    Notes
    -----
    If you need to store metadata alongside your model (such as training information, 
    dataset details, or hyperparameters), you should use the DBSF format. The HDF5 and 
    PyTorch formats only store model weights and do not support additional metadata.
    """
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Infer format from file extension if not specified
    if format is None:
        format = path.suffix[1:]

    format_map = {"h5": "h5", "hdf5": "h5", "pt": "pth", "pth": "pth", "torch": "pth", "pytorch": "pth", "dbsf": "dbsf"}

    format = format_map.get(format.lower())
    if format not in format_map.values():
        raise ValueError(
            f"Unsupported format: {format}. "
            f"Supported formats are: {', '.join(set(format_map.values()))}"
        )
    
    # Warn if metadata is provided but format doesn't support it
    if metadata and format != "dbsf":
        warnings.warn(
            f"Metadata provided but will be ignored because the selected format '{format}' "
            f"does not support metadata. Use DBSF format to save metadata.",
            UserWarning
        )

    # Save based on format
    if format == "h5":
        from .hdf5 import write_h5_weights

        write_h5_weights(path, model)
    elif format == "pth":
        torch.save(model.state_dict(), path)
    elif format == "dbsf":
        from .dbsf import write_dbsf
        write_dbsf(path, model, metadata=metadata)
