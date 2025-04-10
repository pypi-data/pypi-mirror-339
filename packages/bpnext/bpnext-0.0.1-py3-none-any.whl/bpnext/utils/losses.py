"""
Loss functions used by BPNet for training.

This module provides specialized loss functions for training BPNet models:
- MNLLLoss: Multinomial negative log-likelihood for profile prediction
- log1pMSELoss: MSE loss in log(x+1) space for count prediction

Adapted from https://github.com/jmschrei/bpnet-lite.
"""

import torch


def MultinomialNLLLoss(logps: torch.Tensor, true_counts: torch.Tensor) -> torch.Tensor:
    """Multinomial negative log-likelihood loss.

    Computes the negative log likelihood of observing the true counts under a
    multinomial distribution with probabilities derived from logps. This is used
    for the profile prediction task in BPNet.

    For counts k = [k₁, ..., kₘ], total count N = ∑₍ᵢ₌₁₎ᵐ kᵢ, and 
    predicted log probabilities log(p₁), ..., log(pₘ), 
    the multinomial likelihood is

        $$
        P(k; N, p) = \frac{N!}{\prod_{i=1}^{m} k_i!} \prod_{i=1}^{m} p_i^{k_i}
        $$

    Taking the logarithm gives

        $$
        \log P(k; N, p) = \log N! - \sum_{i=1}^{m} \log k_i! + \sum_{i=1}^{m} k_i \log p_i
        $$

    The negative log-likelihood is then

        $$
        -\log P(k; N, p) = -\log N! + \sum_{i=1}^{m} \log k_i! - \sum_{i=1}^{m} k_i \log p_i
        $$

    We use the log-gamma function to compute the factorial term:

        $$  
        \log N! = \log \Gamma(N + 1)
        \log k_i! = \log \Gamma(k_i + 1)
        $$

    The MNLL loss is then

      $$
      loss = –\log \Gamma(N + 1) + \sum_{i=1}^{m} \log \Gamma(k_i + 1) - \sum_{i=1}^{m} k_i \log p_i
      $$

    Parameters
    ----------
    logps : torch.Tensor, shape=(batch_size, ..., num_classes)
        Log probabilities from log_softmax.
    true_counts : torch.Tensor, shape=(batch_size, ..., num_classes)
        True count values. Must match the shape of logps.

    Returns
    -------
    torch.Tensor, shape=(batch_size, ...)
        The multinomial negative log likelihood of observing the true counts
        given the predicted probabilities.
        Averaged over all dimensions except batch
    """
    # Input validation
    if logps.shape != true_counts.shape:
        raise RuntimeError(f"Shape mismatch: logps shape {logps.shape} != true_counts shape {true_counts.shape}")
    
    if logps.dim() < 2:
        raise RuntimeError(f"Input tensors must have at least 2 dimensions, got {logps.dim()} dimensions")

    log_fact_sum = torch.lgamma(torch.sum(true_counts, dim=-1) + 1)
    log_prod_fact = torch.sum(torch.lgamma(true_counts + 1), dim=-1)
    log_prod_exp = torch.sum(true_counts * logps, dim=-1)
    return -log_fact_sum + log_prod_fact - log_prod_exp


def Log1pMSELoss(predicted_logcounts: torch.Tensor, true_counts: torch.Tensor) -> torch.Tensor:
    """Mean squared error loss in log1p space.
    
    Computes MSE between log1p-transformed true counts and predicted log counts:
    loss = mean((log(true_counts + 1) - predicted_logcounts)**2)

    Parameters
    ----------
    predicted_logcounts : torch.Tensor, shape=(batch_size, ...)
        Model predictions in log space. These should be direct model outputs,
        not transformed. The model is expected to predict log counts directly.

    true_counts : torch.Tensor, shape=(batch_size, ...)
        True counts in original (non-log) space. Must match the shape of
        predicted_logcounts. These will be transformed using log1p internally.

    Returns
    -------
    torch.Tensor, shape=(batch_size, ...)
        MSE loss averaged over all dimensions except batch.
    """
    # Input validation
    if predicted_logcounts.shape != true_counts.shape:
        raise RuntimeError(f"Shape mismatch: predicted_logcounts shape {predicted_logcounts.shape} != true_counts shape {true_counts.shape}")

    if predicted_logcounts.dim() < 2:
        raise RuntimeError(f"Input tensors must have at least 2 dimensions, got {predicted_logcounts.dim()} dimensions")

    log_true = torch.log1p(true_counts)
    return torch.mean(torch.square(log_true - predicted_logcounts), dim=-1)
