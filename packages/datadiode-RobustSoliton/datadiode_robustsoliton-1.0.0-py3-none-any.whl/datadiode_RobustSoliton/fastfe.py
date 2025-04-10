import math
import os
import multiprocessing as mp
from collections import Counter
from functools import partial

def count_bytes_in_chunk(file_path, start_pos, chunk_size):
    """Count byte frequencies in a specific chunk of a file"""
    byte_counter = Counter()
    
    with open(file_path, 'rb') as f:
        f.seek(start_pos)
        data = f.read(chunk_size)
        byte_counter.update(data)
    
    return byte_counter

def calculate_entropy_parallel(file_path, num_processes=None):
    """
    Calculate file entropy using parallel processing
    
    Args:
        file_path: Path to the file
        num_processes: Number of CPU cores to use (defaults to all available)
    
    Returns:
        entropy value (bits per byte)
    """
    # Get file size
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return 0
    
    # Determine number of processes to use
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    # Limit processes based on file size (no need for many processes on small files)
    num_processes = min(num_processes, max(1, file_size // (1024 * 1024)))
    
    # Calculate chunk size for each process
    chunk_size = file_size // num_processes
    remainder = file_size % num_processes
    
    # Create a list of (start_position, chunk_size) for each process
    chunks = []
    start_pos = 0
    for i in range(num_processes):
        # Distribute remainder across first few chunks
        current_chunk_size = chunk_size + (1 if i < remainder else 0)
        chunks.append((start_pos, current_chunk_size))
        start_pos += current_chunk_size
    
    # Create a pool of worker processes
    with mp.Pool(processes=num_processes) as pool:
        # Process each chunk in parallel
        counter_func = partial(count_bytes_in_chunk, file_path)
        counters = pool.starmap(counter_func, chunks)
    
    # Combine all counters
    combined_counter = Counter()
    for counter in counters:
        combined_counter.update(counter)
    
    # Calculate entropy
    entropy = 0
    for count in combined_counter.values():
        probability = count / file_size
        entropy -= probability * math.log2(probability)
    
    return entropy

def analyze_file_compressibility(file_path, num_processes=None):
    """
    Analyze if a file can be compressed based on entropy
    
    Args:
        file_path: Path to the file
        num_processes: Number of CPU cores to use
        
    Returns:
        dict with entropy and compression information
    """
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return {"error": "File is empty", "can_be_compressed": False}
    
    entropy = calculate_entropy_parallel(file_path, num_processes)
    
    # Interpret entropy
    compression_potential = "Unknown"
    if entropy >= 7.9:
        compression_potential = "Minimal (0-5% reduction)"
    elif entropy >= 7.5:
        compression_potential = "Low (5-15% reduction)"
    elif entropy >= 6.5:
        compression_potential = "Moderate (15-30% reduction)"
    elif entropy >= 5.0:
        compression_potential = "Good (30-50% reduction)"
    else:
        compression_potential = "Excellent (>50% reduction)"
    
    can_be_compressed = entropy < 7.5
    
    return {
        "file_size": file_size,
        "entropy": entropy,
        "bits_per_byte": entropy,
        "optimal_compression_ratio": 8 / entropy if entropy > 0 else float('inf'),
        "compression_potential": compression_potential,
        "can_be_compressed": can_be_compressed,
        "recommendation": (
            "This file is likely compressible." if can_be_compressed 
            else "This file is likely already compressed or encrypted."
        )
    }

if __name__ == "__main__":
    import sys
    import time
    
    if len(sys.argv) != 2:
        print("Usage: python entropy_parallel.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)
    
    start_time = time.time()
    results = analyze_file_compressibility(file_path)
    elapsed_time = time.time() - start_time
    
    print(f"Entropy Analysis Results (completed in {elapsed_time:.2f} seconds):")
    print(f"File size: {results['file_size']:,} bytes")
    print(f"Entropy: {results['entropy']:.6f} bits per byte")
    print(f"Optimal compression ratio: {results['optimal_compression_ratio']:.2f}:1")
    print(f"Compression potential: {results['compression_potential']}")
    print(f"\nConclusion: {results['recommendation']}")
