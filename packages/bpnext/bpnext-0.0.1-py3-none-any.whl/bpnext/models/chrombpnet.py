from typing import Optional, Tuple

import torch
from .bpnet import BPNet
from ._mixins import WeightsIOMixin


class ChromBPNet(torch.nn.Module, WeightsIOMixin):
    """Model for analyzing chromatin accessibility data using sequence information.

    This implementation is based on:
    - https://github.com/jmschrei/bpnet-lite
    - https://github.com/kundajelab/chrombpnet (original TensorFlow implementation)

    ChromBPNet combines two BPNet networks to separate technical bias from
    biological signal in ATAC-seq data:

    1. A bias model (frozen) that captures sequence preferences of the Tn5
       transposase, trained on non-peak "background" regions.
    2. An accessibility model (trainable) that learns sequence features
       associated with chromatin accessibility.

    The model combines these components additively in logit space:
    logit(p) = bias_profile + accessibility_profile

    where p is the probability of observing a cut at each position.

    Parameters
    ----------
    bias : BPNet
        A pre-trained BPNet model for capturing Tn5 bias. This model should be
        trained on GC-matched non-peak regions to learn the sequence preferences
        of the Tn5 transposase. Its parameters will be frozen during training.
    accessibility : BPNet
        A BPNet model that will learn sequence features associated with
        chromatin accessibility. This model's parameters will be trained.
    name : str, optional
        Name identifier for the model.

    Notes
    -----
    The bias model's parameters are automatically frozen during initialization.
    Both models produce profile and count predictions, but ChromBPNet only uses
    their profile outputs, combining them additively in logit space.

    Examples
    --------
    >>> bias_model = BPNet(hidden_channels=512)
    >>> # Train bias model on non-peak regions...
    >>> accessibility_model = BPNet(hidden_channels=512)
    >>> model = ChromBPNet(bias_model, accessibility_model)
    >>> # Only accessibility_model parameters will be updated during training
    >>> profile, counts = model(sequences)
    """

    def __init__(self, bias: BPNet, accessibility: BPNet, name: Optional[str] = None):
        """Initialize ChromBPNet model.

        See class docstring for parameter descriptions.
        """
        super().__init__()

        # Freeze the bias model parameters
        for parameter in bias.parameters():
            parameter.requires_grad = False

        self.bias = bias
        self.accessibility = accessibility
        self.name = name

    def forward(
        self, X: torch.Tensor, X_ctl: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the model.

        Parameters
        ----------
        X : torch.Tensor
            Input tensor of shape (batch_size, 4, seq_length) containing
            one-hot encoded DNA sequences.
        X_ctl : torch.Tensor, optional
            Control track tensor of shape (batch_size, num_control_tracks, seq_length).
            If provided, will be used by both bias and accessibility models.

        Returns
        -------
        y_profile : torch.Tensor
            Combined profile predictions of shape (batch_size, 1, output_length).
            This combines the bias and accessibility profiles additively in
            logit space.
        y_counts : torch.Tensor
            Combined count predictions of shape (batch_size, 1). This combines
            the bias and accessibility counts in log space.
        """
        acc_profile, acc_counts = self.accessibility(X, X_ctl)
        bias_profile, bias_counts = self.bias(X, X_ctl)

        y_profile = acc_profile + bias_profile
        y_counts = torch.log(torch.exp(acc_counts) + torch.exp(bias_counts))

        return y_profile, y_counts
