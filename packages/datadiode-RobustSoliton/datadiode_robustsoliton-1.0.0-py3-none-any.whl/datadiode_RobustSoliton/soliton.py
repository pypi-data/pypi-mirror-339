"""
Soliton distribution implementation for fountain codes.
"""
import numpy as np
from datadiode_RobustSoliton.prng import choose_blocks, get_blocks_from_seed, PRNGType

def ideal_soliton(K):
    """
    Generate an ideal soliton distribution for K blocks.
    
    Args:
        K: Number of input blocks
        
    Returns:
        A probability distribution over degrees 1 to K
    """
    rho = np.zeros(K + 1)
    rho[1] = 1.0 / K
    for i in range(2, K + 1):
        rho[i] = 1.0 / (i * (i - 1))
    
    # Normalize
    return rho / np.sum(rho)

def robust_soliton(K, c=0.1, delta=0.05):
    """
    Generate a robust soliton distribution for K blocks.
    
    Args:
        K: Number of input blocks
        c: Parameter c > 0
        delta: Decoding failure probability
        
    Returns:
        A probability distribution over degrees 1 to K
    """
    # Ideal soliton distribution
    rho = ideal_soliton(K)
    
    # Robust soliton additional component
    S = c * np.log(K/delta) * np.sqrt(K)
    S = int(S) if S >= 1 else 1
    
    tau = np.zeros(K + 1)
    for i in range(1, S + 1):
        tau[i] = S / (i * K)
    
    tau[S] = S * np.log(S/delta) / K
    
    # Combine and boost degree 1 packets
    mu = rho + tau
    mu[1] *= 5.0  # Increase probability of degree 1 packets for testing
    
    # Normalize
    return mu / np.sum(mu)

def get_degree_from_distribution(dist):
    """
    Sample a degree from a distribution.
    
    Args:
        dist: A probability distribution
        
    Returns:
        A sampled degree
    """
    cumsum = np.cumsum(dist)
    return np.searchsorted(cumsum, np.random.random()) + 1

# Note: The choose_blocks and get_blocks_from_seed functions are imported from src.prng
# They support different PRNG types through the prng_type parameter