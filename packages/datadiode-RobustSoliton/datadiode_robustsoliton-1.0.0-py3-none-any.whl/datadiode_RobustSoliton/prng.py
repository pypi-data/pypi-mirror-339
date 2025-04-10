"""
Random number generators for fountain codes.
Provides different PRNG implementations for block selection.
"""
import numpy as np
from enum import Enum
import ctypes

class PRNGType(Enum):
    """Types of PRNGs available"""
    NUMPY_MT = "numpy_mt"         # NumPy's Mersenne Twister (RandomState)
    NUMPY_PCG = "numpy_pcg"       # NumPy's PCG64 (Generator)
    XORSHIFT = "xorshift"         # Fast xorshift* algorithm

class XorshiftRNG:
    """
    Implementation of the xorshift* algorithm for fast random number generation.
    Based on the provided code:
    
    uint64_t v = 4101842887655102017LL;
    uint64_t vv = 2685821657736338717LL;
    
    void seed(uint64_t seed) {
        Random32(seed);
    }
    
    uint64_t int64() {
        v ^= v >> 21; 
        v ^= v << 35; 
        v ^= v >> 4;
        return v * vv;
    }
    """
    def __init__(self, seed=None):
        # Constants from the provided code
        self.v = 4101842887655102017  # Initial state
        self.vv = 2685821657736338717  # Multiplier constant
        
        # Seed the generator if a seed is provided
        if seed is not None:
            self.seed(seed)
    
    def seed(self, seed):
        """Seed the generator with a 64-bit integer"""
        # Convert the seed to a 64-bit integer if necessary
        if not isinstance(seed, int):
            seed = hash(seed) & ((1 << 64) - 1)  # Convert to 64-bit unsigned int
        
        # XOR the seed with the state
        self.v ^= seed
        # Mix the seed by generating a number
        self._next_int64()
    
    def _next_int64(self):
        """Generate the next 64-bit random integer"""
        # Apply xorshift operations
        self.v ^= (self.v >> 21) & ((1 << 64) - 1)  # Ensure 64-bit unsigned
        self.v ^= (self.v << 35) & ((1 << 64) - 1)
        self.v ^= (self.v >> 4) & ((1 << 64) - 1)
        
        # Multiply by the constant for better statistical properties (xorshift*)
        result = (self.v * self.vv) & ((1 << 64) - 1)
        return result
    
    def random(self):
        """Generate a random float in [0, 1)"""
        # Convert to double precision float using the same scaling factor as the original code
        return 5.42101086242752217E-20 * self._next_int64()
    
    def randint(self, low, high=None):
        """Generate a random integer in the range [low, high)"""
        if high is None:
            high = low
            low = 0
        
        if low >= high:
            raise ValueError("low must be less than high")
        
        # Get the range size and generate a random number within that range
        range_size = high - low
        return low + (self._next_int64() % range_size)
    
    def choice(self, a, size=None, replace=True, p=None):
        """
        Random choice from an array-like object.
        
        Args:
            a: Array-like object
            size: Output shape (or None for a single value)
            replace: Whether to sample with replacement
            p: Probability array (not implemented for xorshift)
        
        Returns:
            Random samples from a
        """
        if p is not None:
            raise NotImplementedError("Probability weights not implemented for XorshiftRNG")
        
        # Convert to array for indexing
        a = np.asarray(a)
        
        if size is None:
            # Return a single random element
            idx = self.randint(0, len(a))
            return a[idx]
        
        # Handle multi-element selection
        if replace:
            # With replacement: simple random sampling
            indices = [self.randint(0, len(a)) for _ in range(size)]
        else:
            # Without replacement: Fisher-Yates shuffle
            if size > len(a):
                raise ValueError("Cannot take more elements than available without replacement")
            
            # Create a copy of the indices
            indices = list(range(len(a)))
            
            # Shuffle the first 'size' elements
            for i in range(size):
                j = self.randint(i, len(indices))
                indices[i], indices[j] = indices[j], indices[i]
            
            # Take the first 'size' elements
            indices = indices[:size]
        
        return a[indices]

class PCG64RNG:
    """Wrapper around NumPy's PCG64 generator."""
    def __init__(self, seed=None):
        from numpy.random import Generator, PCG64
        self.pcg = np.random.PCG64(seed)
        self.rng = np.random.Generator(self.pcg)
    
    def seed(self, seed):
        """Seed the generator"""
        # Use the same PCG instance but reseed it
        self.pcg.seed(seed)
    
    def random(self):
        """Generate a random float in [0, 1)"""
        return self.rng.random()
    
    def randint(self, low, high=None):
        """Generate a random integer in the range [low, high)"""
        return self.rng.integers(low, high)
    
    def choice(self, a, size=None, replace=True, p=None):
        """Random choice from an array-like object."""
        return self.rng.choice(a, size=size, replace=replace, p=p)

class MT19937RNG:
    """Wrapper around NumPy's RandomState (Mersenne Twister)."""
    def __init__(self, seed=None):
        self.rng = np.random.RandomState(seed)
    
    def seed(self, seed):
        """Seed the generator"""
        self.rng.seed(seed)
    
    def random(self):
        """Generate a random float in [0, 1)"""
        return self.rng.random()
    
    def randint(self, low, high=None):
        """Generate a random integer in the range [low, high)"""
        return self.rng.randint(low, high)
    
    def choice(self, a, size=None, replace=True, p=None):
        """Random choice from an array-like object."""
        return self.rng.choice(a, size=size, replace=replace, p=p)

def get_prng(prng_type, seed=None):
    """
    Factory function to create a PRNG of the specified type.
    
    Args:
        prng_type: Type of PRNG (from PRNGType enum)
        seed: Random seed
    
    Returns:
        A PRNG instance
    """
    if isinstance(prng_type, str):
        prng_type = PRNGType(prng_type)
    
    if prng_type == PRNGType.NUMPY_MT:
        return MT19937RNG(seed)
    elif prng_type == PRNGType.NUMPY_PCG:
        return PCG64RNG(seed)
    elif prng_type == PRNGType.XORSHIFT:
        return XorshiftRNG(seed)
    else:
        raise ValueError(f"Unknown PRNG type: {prng_type}")

def choose_blocks_with_prng(K, degree, seed=None, prng_type=PRNGType.NUMPY_MT):
    """
    Choose degree distinct blocks from K blocks using the specified PRNG.
    
    Args:
        K: Number of blocks
        degree: Number of blocks to choose
        seed: Random seed for reproducibility
        prng_type: Type of PRNG to use
    
    Returns:
        List of chosen block indices
    """
    # Create a PRNG of the specified type
    prng = get_prng(prng_type, seed)
    
    # Choose indices without replacement
    return prng.choice(K, size=degree, replace=False)

# For backward compatibility
def choose_blocks(K, degree, seed=None, prng_type=PRNGType.NUMPY_MT):
    """
    Choose degree distinct blocks from K blocks.
    Default to NumPy's RandomState for backward compatibility.
    
    Args:
        K: Number of blocks
        degree: Number of blocks to choose
        seed: Random seed for reproducibility
        prng_type: Type of PRNG to use
    
    Returns:
        List of chosen block indices
    """
    return choose_blocks_with_prng(K, degree, seed, prng_type)

def pcg32_random(seed):
    """
    Fast PCG32 implementation in pure Python.
    This is a 32-bit random number generator based on the PCG algorithm.
    
    Args:
        seed: 64-bit unsigned integer seed
        
    Returns:
        A 32-bit random number
    """
    # PCG32 state and constants
    MULTIPLIER = 6364136223846793005  # PCG32 multiplier
    INCREMENT = 1442695040888963407   # PCG32 increment
    
    # Convert to 64-bit unsigned int if needed
    state = seed & 0xFFFFFFFFFFFFFFFF
    
    # Update state
    state = (state * MULTIPLIER + INCREMENT) & 0xFFFFFFFFFFFFFFFF
    
    # Generate output - PCG uses a complex permutation function
    xorshifted = ((state >> 18) ^ state) >> 27
    rot = state >> 59
    return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF

# Implementation of Ran from Numerical Recipes 3rd edition
class NRRRNG:
    """
    Implementation of the Ran generator from Numerical Recipes (3rd edition).
    This is a 64-bit random number generator with excellent statistical properties.
    """
    def __init__(self, seed=None):
        # Initialize with default or provided seed
        self.u = 0
        self.v = 0
        self.w = 0
        
        # Default seed if none provided
        if seed is None:
            seed = 123456789
            
        self.seed(seed)
    
    def seed(self, seed):
        """Seed the generator with a 64-bit integer"""
        # Convert the seed to a 64-bit unsigned integer
        seed = abs(int(seed)) & 0xFFFFFFFFFFFFFFFF
        
        # Initialize the state variables
        self.u = seed ^ 4101842887655102017
        self.v = self.u * 2685821657736338717 % 2**64
        self.w = self.v * 5 % 2**64
        
        # Warm up the generator
        for _ in range(5):
            self.int64()
    
    def int64(self):
        """Generate the next 64-bit random integer"""
        self.u = self.u * 2862933555777941757 + 7046029254386353087 % 2**64
        self.v ^= self.v >> 17
        self.v ^= self.v << 31
        self.v ^= self.v >> 8
        self.w = 4294957665 * (self.w & 0xFFFFFFFF) + (self.w >> 32)
        x = self.u ^ (self.u << 21)
        x ^= x >> 35
        x ^= x << 4
        return (x + self.v) ^ self.w
    
    def random(self):
        """Generate a random float in [0, 1)"""
        return self.int64() * 5.42101086242752217E-20
    
    def randint(self, low, high=None):
        """Generate a random integer in the range [low, high)"""
        if high is None:
            high = low
            low = 0
        
        if low >= high:
            raise ValueError("low must be less than high")
        
        # Get the range size and generate a random number within that range
        range_size = high - low
        return low + (self.int64() % range_size)
    
    def choice(self, a, size=None, replace=True, p=None):
        """Random choice from an array-like object"""
        if p is not None:
            raise NotImplementedError("Probability weights not implemented for NRRRNG")
        
        # Convert to array for indexing
        a = np.asarray(a)
        
        if size is None:
            # Return a single random element
            idx = self.randint(0, len(a))
            return a[idx]
        
        # Handle multi-element selection
        if replace:
            # With replacement: simple random sampling
            indices = [self.randint(0, len(a)) for _ in range(size)]
        else:
            # Without replacement: Fisher-Yates shuffle
            if size > len(a):
                raise ValueError("Cannot take more elements than available without replacement")
            
            # Create a copy of the indices
            indices = list(range(len(a)))
            
            # Shuffle the first 'size' elements
            for i in range(size):
                j = self.randint(i, len(indices))
                indices[i], indices[j] = indices[j], indices[i]
            
            # Take the first 'size' elements
            indices = indices[:size]
        
        return a[indices]

# Fast XorShift implementation for block selection
def fast_xorshift(seed, K, degree):
    """
    Fast implementation of Xorshift* algorithm for block selection.
    
    Args:
        seed: Initial seed value
        K: Number of blocks
        degree: Number of indices to select
        
    Returns:
        List of selected indices
    """
    # Handle special cases
    if degree == 1:
        return [seed % K]
    elif degree >= K:
        return list(range(K))
    
    # Initialize xorshift state
    v = 4101842887655102017 if seed == 0 else seed
    vv = 2685821657736338717  # Multiplier for xorshift*
    
    # Create array for index-value pairs
    data = np.zeros((K, 2), dtype=np.uint64)
    data[:, 0] = np.arange(K)
    
    # Generate random values using xorshift* algorithm
    for i in range(K):
        # Xorshift* algorithm
        v ^= (v >> 21) & ((1 << 64) - 1)
        v ^= (v << 35) & ((1 << 64) - 1) 
        v ^= (v >> 4) & ((1 << 64) - 1)
        data[i, 1] = (v * vv) & ((1 << 64) - 1)
    
    # Sort by random values
    data = data[data[:, 1].argsort()]
    
    # Return the first 'degree' indices
    return data[:degree, 0].astype(np.int32).tolist()

# Fast NRR implementation specifically for block selection
def fast_nrr(seed, K, degree):
    """
    Fast implementation of Numerical Recipes Ran algorithm for block selection.
    
    Args:
        seed: Initial seed value
        K: Number of blocks
        degree: Number of indices to select
        
    Returns:
        List of selected indices
    """
    # Handle special cases
    if degree == 1:
        return [seed % K]
    elif degree >= K:
        return list(range(K))
    
    # Initialize state variables
    u = seed ^ 4101842887655102017
    v = u * 2685821657736338717 % 2**64
    w = v * 5 % 2**64
    
    # Create array for index-value pairs
    data = np.zeros((K, 2), dtype=np.uint64)
    data[:, 0] = np.arange(K)
    
    # Generate random values using NRR algorithm
    for i in range(K):
        # NRR algorithm from Numerical Recipes 3rd edition - with fixed overflow
        u = (u * 2862933555777941757 + 7046029254386353087) & 0xFFFFFFFFFFFFFFFF
        v ^= v >> 17
        v ^= v << 31
        v ^= v >> 8
        w = 4294957665 * (w & 0xFFFFFFFF) + (w >> 32)
        x = u ^ (u << 21)
        x ^= x >> 35
        x ^= x << 4
        # Ensure value fits in uint64
        data[i, 1] = ((x + v) ^ w) & 0xFFFFFFFFFFFFFFFF
    
    # Sort by random values
    data = data[data[:, 1].argsort()]
    
    # Return the first 'degree' indices
    return data[:degree, 0].astype(np.int32).tolist()

def get_blocks_from_seed(K, degree, seed):
    """
    Deterministically generate block indices from a seed using NumPy's optimized
    PCG64 implementation for maximum performance.
    
    Args:
        K: Number of blocks
        degree: Number of blocks to choose
        seed: Random seed to deterministically generate indices
    
    Returns:
        List of chosen block indices
    """
    # Handle edge cases
    if K <= 0 or degree <= 0:
        return []
    
    # Cap degree at K
    degree = min(degree, K)
    
    # Quick paths for common cases
    if degree == 1:
        # For degree=1 (most common case), use simple modulo (fastest method)
        return [seed % K]
    elif degree >= K:
        # If we need all blocks, just return sequential indices
        return list(range(K))
    
    # Use NumPy's PCG64 for maximum performance (900-1000 Mbps)
    try:
        # Import numpy's Generator+PCG64 if available (newer versions)
        from numpy.random import Generator, PCG64
        rng = Generator(PCG64(seed))
        # Use optimized implementation for best performance
        return rng.choice(K, size=degree, replace=False).tolist()
    except ImportError:
        # Fall back to standard RandomState
        rng = np.random.RandomState(seed)
        return rng.choice(K, size=degree, replace=False).tolist()