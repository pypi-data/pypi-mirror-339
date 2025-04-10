"""Base classes and mixins for YAB models."""

from pathlib import Path
from typing import Union, Optional, Dict, Any


class WeightsIOMixin:
    """Mixin that adds save_weights and load_weights methods to a model."""

    def load_weights(
        self, filename: Union[str, Path], format: Optional[str] = None
    ) -> None:
        """Load model weights from a file.

        Parameters
        ----------
        filename : str or Path
            Path to the file containing trained model parameters
        format : str, optional
            Format of the weights file. If None, will be inferred from file extension.
            Supported formats:
            - "h5", "hdf5": Legacy TensorFlow HDF5 format
            - "pt", "pth": PyTorch saved state dict
            - "dbsf": DeepBind Storage Format
        """
        from ..io.base import load_weights

        load_weights(self, filename, format)

    def save_weights(
        self, filename: Union[str, Path], format: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Save model weights to a file.

        Parameters
        ----------
        filename : str or Path
            Path to save the weights file
        format : str, optional
            Format to save in. If None, will be inferred from file extension.
            Supported formats:
            - "h5", "hdf5": Legacy TensorFlow HDF5 format
            - "pt", "pth": PyTorch state dict
            - "dbsf": DeepBind Storage Format
        metadata : Dict[str, Any], optional
            Additional metadata to store with the model (DBSF format only)
        """
        from ..io.base import save_weights

        save_weights(self, filename, format, metadata)
