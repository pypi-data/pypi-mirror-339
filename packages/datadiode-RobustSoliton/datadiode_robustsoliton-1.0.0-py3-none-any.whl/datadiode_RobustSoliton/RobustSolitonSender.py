"""
RobustSolitonSender: A robust FEC implementation with file chunking.
Processes large files in manageable chunks.

This module allows for reliable file transfer over lossy networks using 
Robust Soliton fountain codes. It breaks files into manageable chunks and
applies Forward Error Correction to ensure data integrity.

Command-line usage:
    python -m src.RobustSolitonSender file.bin --host receiver-ip --port 12345 [options]

Parameters:
    file            : Path to the file to send
    --host          : Destination hostname/IP (default: localhost)
    --port          : Destination port (default: 12345)
    --chunk-size    : Size of file chunks (default: 10MB)
    --block-size    : Size of data blocks (default: 8192 bytes)
    --packet-rate   : Optional rate limiting (packets/sec)
    --overhead      : Redundancy factor (default: 6.0)
    --fec           : Error correction strength (default: 1.0)
    --c             : Robust Soliton parameter (default: 0.1)
    --delta         : Decoding failure probability (default: 0.05)
"""
import argparse
import socket
import time
import os
import sys
import math
import struct
import re
import hashlib
import threading
from datadiode_RobustSoliton.fixed_fec import Encoder
from datadiode_RobustSoliton.utils import load_large_file_chunk, get_file_size, get_file_hash
from datadiode_RobustSoliton.prng import PRNGType
from datadiode_RobustSoliton.fastfe import analyze_file_compressibility

# Chunk size in bytes (10 MB default)
DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024

def parse_size(size_str):
    """
    Parse a size string with optional MB/Mb/mb suffix.
    
    Args:
        size_str: String like "10MB" or "100mb" or just "50"
        
    Returns:
        Size in bytes
    """
    # If it's already an int, just return it
    if isinstance(size_str, int):
        return size_str
        
    # Check for MB suffix
    match = re.match(r'^(\d+)([mM][bB])?$', str(size_str))
    if not match:
        # Try to convert as a plain number
        try:
            return int(size_str)
        except ValueError:
            raise ValueError(f"Invalid size format: {size_str}. Use a number or a number followed by MB/Mb/mb.")
    
    # Extract the number and convert to bytes
    number = int(match.group(1))
    return number * 1024 * 1024

def analyze_compressibility_thread(file_path, result_dict):
    """
    Analyze file compressibility in a separate thread.
    Stores results in the provided dictionary.
    
    Args:
        file_path: Path to the file to analyze
        result_dict: Dictionary to store results (modified in-place)
    """
    try:
        print(f"Starting compressibility analysis for {os.path.basename(file_path)}...")
        
        # Analyze file compressibility
        results = analyze_file_compressibility(file_path)
        
        # Store results in the provided dictionary
        result_dict.update(results)
    except Exception as e:
        result_dict["error"] = f"Error analyzing compressibility: {str(e)}"
        print(f"Error in compressibility analysis thread: {e}")

def send_file_chunked(file_path, dest_addr=('localhost', 12345), chunk_size=DEFAULT_CHUNK_SIZE,
              block_size=8192, packet_rate=None, overhead_factor=6.0, c=0.03, delta=0.05, fec_level=1.0,
              first_chunk_multiplier=5.0, multicast=None, broadcast=False, ttl=1):
    """
    Send a file over UDP using Robust Soliton FEC with chunking.
    
    Args:
        file_path: Path to the file to send
        dest_addr: (ip, port) tuple for the destination
        chunk_size: Size of each file chunk to process independently
        block_size: Size of each block in bytes
        packet_rate: Number of packets to send per second
        overhead_factor: Factor of extra packets to send (e.g., 1.5 = 50% more packets)
        c: Base parameter for Robust Soliton distribution
        delta: Base decoding failure probability 
        fec_level: Mathematical coefficient that adjusts Robust Soliton parameters (c and delta)
        multicast: Multicast address to use instead of unicast
        broadcast: Enable broadcast mode
        ttl: Time-to-live for multicast packets
    """
    import tqdm
    
    # Validate parameters
    if fec_level <= 0:
        raise ValueError("FEC level must be greater than 0")
    
    if overhead_factor <= 1:
        raise ValueError("Overhead factor must be greater than 1")
        
    if first_chunk_multiplier <= 1:
        raise ValueError("First chunk multiplier must be greater than 1")
    
    # Validate file exists and can be opened
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file size
    file_size = get_file_size(file_path)
    print(f"File size: {file_size/1024/1024:.2f} MB")
    
    # Extract just the filename from the path (no directories)
    filename = os.path.basename(file_path)
    print(f"Using filename: {filename}")
    
    # Start a thread to analyze file compressibility in the background
    compressibility_results = {}
    compression_thread = threading.Thread(
        target=analyze_compressibility_thread, 
        args=(file_path, compressibility_results),
        daemon=True  # Make thread a daemon so it doesn't block program exit
    )
    compression_thread.start()
    
    # Calculate number of chunks
    num_chunks = math.ceil(file_size / chunk_size)
    
    # Import tqdm for progress bar
    import tqdm
    
    # Only print this once before progress bar starts
    if packet_rate is not None:
        print(f"Sending {num_chunks} chunks of {chunk_size/1024/1024:.2f} MB each, rate limited to {packet_rate} packets/second")
    else:
        print(f"Sending {num_chunks} chunks of {chunk_size/1024/1024:.2f} MB each at maximum speed")
    
    # Create UDP socket - determine if IPv6 or IPv4
    is_ipv6 = ':' in dest_addr[0] if not multicast else ':' in multicast
    
    # Check for broadcast and multicast conflicts
    if broadcast and multicast:
        raise ValueError("Cannot use both broadcast and multicast modes simultaneously")
    
    if is_ipv6:
        # IPv6 address
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        
        # Set multicast TTL for IPv6
        if multicast:
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
    else:
        # IPv4 address
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Set multicast TTL for IPv4
        if multicast:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
        # Enable broadcast mode if requested
        if broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Set socket buffer size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 16)  # 16MB buffer
    
    # If multicast is specified, use it instead of the regular destination address
    if multicast:
        print(f"Using multicast mode with group: {multicast}")
        dest_addr = (multicast, dest_addr[1])
    
    # If broadcast is enabled, use the broadcast address
    if broadcast:
        print("Using broadcast mode")
        dest_addr = ('<broadcast>', dest_addr[1]) if not is_ipv6 else ('ff02::1', dest_addr[1])
    
    # Create progress bar with better formatting and turquoise color
    # ANSI color codes for turquoise
    TURQUOISE = '\033[38;5;45m'  # Bright turquoise
    RESET = '\033[0m'
    
    # Custom bar format with turquoise color for the progress bar
    bar_color = TURQUOISE
    bar_format = "{desc}: {percentage:3.0f}%|" + bar_color + "{bar}" + RESET + "| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {postfix}]"
    
    # Configure tqdm to match the receiver's style
    # Use a shorter bar with no dynamic overwrite for clean progress display
    custom_bar_format = "{desc:<15}:{percentage:3.0f}%|" + bar_color + "{bar}" + RESET + "|{n_fmt}/{total_fmt} [{elapsed:<5} {postfix}]"
    
    # Calculate total number of packets to be sent based on all parameters
    total_blocks = math.ceil(file_size / block_size)
    
    # Calculate the FEC adjustment factor based on the formula in the code
    fec_adjustment = 1.0 + 0.2 * (fec_level - 1.0)
    
    # Calculate first chunk's blocks and packets (with multiplier)
    blocks_per_chunk = math.ceil(chunk_size / block_size)
    first_chunk_blocks = min(blocks_per_chunk, total_blocks)
    
    # Apply both the first_chunk_multiplier and the FEC adjustment
    effective_first_chunk_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
    first_chunk_packets = int(first_chunk_blocks * effective_first_chunk_overhead)
    
    # Calculate remaining blocks and packets
    remaining_blocks = total_blocks - first_chunk_blocks
    remaining_chunks = num_chunks - 1
    
    # Apply the FEC adjustment to the remaining chunks as well
    effective_remaining_overhead = overhead_factor * fec_adjustment
    
    # Calculate packets for remaining chunks
    if remaining_chunks > 0:
        packets_per_remaining_chunk = int(remaining_blocks * effective_remaining_overhead) / remaining_chunks
        remaining_packets = int(remaining_blocks * effective_remaining_overhead)
    else:
        packets_per_remaining_chunk = 0
        remaining_packets = 0
    
    # Total expected packets
    total_packets = first_chunk_packets + remaining_packets
    
    # Add packet size information to metadata to help receiver's progress bar
    packets_meta = {
        'total_packets': total_packets,
        'first_chunk_packets': first_chunk_packets,
        'packets_per_remaining_chunk': packets_per_remaining_chunk,
        'avg_packet_size': block_size + 65,  # data + ~65 bytes overhead (UDP/IP + chunk headers)
        # Add effective overhead information for the receiver
        'effective_first_chunk_overhead': effective_first_chunk_overhead,
        'effective_remaining_overhead': effective_remaining_overhead,
        'fec_adjustment': fec_adjustment
    }
    
    # Initialize master progress bar with file size total (for visual consistency)
    master_pbar = tqdm.tqdm(
        total=file_size, 
        desc=f"Sending {filename}", 
        unit="B", 
        unit_scale=True,
        unit_divisor=1024,  # Explicitly use 1024 for binary size units to ensure correct display
        bar_format=custom_bar_format,
        position=0,     # Force position to 0 to stay on same line
        leave=True,     # Keep bar visible after completion
        dynamic_ncols=False  # Fixed width bar
    )
    
    # Initialize progress bar with chunk and packet info
    master_pbar.set_postfix(status=f"Starting... ({total_packets} packets)")
    
    
    # Send metadata about the file to help the receiver
    metadata = {
        'file_size': file_size,
        'chunk_size': chunk_size,
        'num_chunks': num_chunks,
        'block_size': block_size,
        'filename': filename
    }
    
    # Use JSON for metadata - much more reliable than struct in this case
    metadata_dict = {
        'file_size': file_size,
        'chunk_size': chunk_size,
        'num_chunks': num_chunks,
        'block_size': block_size,
        'overhead_factor': overhead_factor,
        'fec_level': fec_level,
        'c': c,
        'c_adjusted': c * fec_level,
        'delta': delta,
        'delta_adjusted': max(1e-10, min(0.9, delta / fec_level)),
        'first_chunk_multiplier': first_chunk_multiplier,
        'filename': filename,
        # Add exact total packet count at the root level for the receiver
        'total_packets': total_packets,
        # Add packets metadata to help receiver show accurate progress
        'packets_meta': packets_meta
    }
    
    # First calculate MD5 checksum of the file before sending anything
    print("Calculating MD5 checksum of the file (needed for metadata)...")
    file_md5 = get_file_hash(file_path)
    
    # Use tqdm.write to print without disrupting progress bar
    tqdm.tqdm.write(f"File MD5: {file_md5}")
    
    # Add MD5 to metadata
    metadata_dict['md5_checksum'] = file_md5
    
    # Convert to JSON string and encode as bytes
    import json
    metadata_json = json.dumps(metadata_dict)
    metadata_bytes = metadata_json.encode('utf-8')
    
    # Use tqdm.write to avoid interfering with progress bar
    tqdm.tqdm.write(f"Metadata size: {len(metadata_bytes)} bytes")
    
    # Send metadata packet with special header to identify it multiple times for reliability
    header = b'METADATA'
    metadata_packet = header + metadata_bytes
    
    tqdm.tqdm.write("Sending file metadata with MD5 checksum (sending multiple times for reliability)...")
    for _ in range(5):  # Send metadata 5 times to ensure it's received
        sock.sendto(metadata_packet, dest_addr)
        time.sleep(0.1)  # Small delay between sends
    
    # Process each chunk
    start_time = time.time()
    bytes_sent = 0
    bytes_sent_time = 0  # Track the time spent on previous chunks
    
    for chunk_id in range(num_chunks):
        chunk_start = chunk_id * chunk_size
        chunk_end = min(chunk_start + chunk_size, file_size)
        current_chunk_size = chunk_end - chunk_start
        
        # Update in progress bar instead of printing a separate message
        
        # Load this chunk of the file
        chunk_data = load_large_file_chunk(file_path, chunk_start, current_chunk_size)
        
        # Create encoder for this chunk with adjusted Robust Soliton parameters
        # Apply fec_level mathematically to the Robust Soliton parameters:
        # - Increasing c increases the number of higher-degree packets (better error correction)
        # - Decreasing delta decreases the probability of decoding failure
        c_adjusted = c * fec_level  # Increase c proportionally to fec_level
        delta_adjusted = delta / fec_level  # Decrease delta inversely to fec_level
        
        # Ensure delta remains in valid range (0,1)
        delta_adjusted = max(1e-10, min(0.9, delta_adjusted))
        
        # Create encoder for this chunk
        encoder = Encoder(chunk_data, block_size=block_size, c=c_adjusted, delta=delta_adjusted)
        num_blocks = encoder.K
        
        # Calculate number of packets to send for this chunk
        # Apply extra overhead for the first chunk since it's most critical
        # The overhead is already adjusted by the Soliton parameters, but we still apply
        # a multiplier for the first chunk to improve recovery under high packet loss
        
        # Use the same calculation as we did for total_packets at the beginning
        if chunk_id == 0:
            # First chunk uses the first_chunk_multiplier
            effective_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
        else:
            # Remaining chunks use standard overhead with FEC adjustment
            effective_overhead = overhead_factor * fec_adjustment
            
        num_packets = int(num_blocks * effective_overhead)
        
        # Update master progress with current chunk info - use status for clean display
        master_pbar.set_postfix(status=f"Chunk {chunk_id+1}/{num_chunks}")
        
        # Calculate batch size to reduce overhead
        batch_size = 100  # Larger batch size for better performance
        
        # Only apply rate limiting if packet_rate is specified
        rate_limited = packet_rate is not None
        sleep_time = batch_size / packet_rate if rate_limited else 0
        
        # No individual chunk progress bar anymore - we will update only the master progress bar
        
        # Generate chunk header to identify which chunk this packet belongs to
        # Format: chunk_id (8 bytes) + filename_length (2 bytes) + filename
        filename_bytes = filename.encode('utf-8')
        filename_len = len(filename_bytes)
        if filename_len > 255:  # Limit filename length to avoid excessive overhead
            filename_bytes = filename_bytes[:255]
            filename_len = 255
            
        chunk_header = struct.pack('!QB', chunk_id, filename_len) + filename_bytes
        
        # Send packets in batches for better performance
        for i in range(0, num_packets, batch_size):
            batch_end = min(i + batch_size, num_packets)
            batch_count = batch_end - i
            
            # Generate and send a batch of packets
            for j in range(i, batch_end):
                packet_data, packet_info = encoder.next_packet()
                try:
                    # Add chunk identifier to the packet
                    # Leave room for the chunk_header (chunk_id + filename length + filename)
                    header_size = 8 + 1 + filename_len  # 8 (chunk_id) + 1 (filename_len) + filename_len
                    max_packet_size = 65000 - header_size
                    encoded_packet = encoder.encode_packet(packet_data, packet_info, max_size=max_packet_size)
                        
                    sock.sendto(chunk_header + encoded_packet, dest_addr)
                except Exception as e:
                    print(f"Error sending packet {j}: {e}")
                    raise
            
            # Calculate and display transmission rate
            elapsed = time.time() - start_time
            if elapsed > 0:
                # Calculate overall rate: how fast the entire transfer is progressing
                overall_rate = bytes_sent / elapsed
                
                # MB/s - application-level throughput
                overall_mb_per_sec = overall_rate/1024/1024
                
                # Calculate wire speed in Mbps (megabits per second)
                # Estimate bytes sent with overhead for this chunk
                # Each packet contains: block data + UDP/IP headers + chunk header
                avg_packet_size = encoder.block_size + 65  # data + ~65 bytes overhead (UDP/IP + chunk headers)
                
                # Calculate total wire bytes sent for this chunk
                total_wire_bytes = j * avg_packet_size  # j is the packet counter
                
                # Calculate chunks sent so far (including partial chunks)
                chunks_sent = chunk_id + (j / num_packets)
                
                # Update master progress with info about chunks and packets
                # Only update progress bar every 20 packets to reduce line changes
                if j % 20 == 0:
                    # Calculate total packets sent so far
                    packets_sent_prev_chunks = 0
                    for prev_chunk in range(chunk_id):
                        # Calculate packets for each previous chunk
                        prev_num_blocks = math.ceil(min(chunk_size, file_size - prev_chunk * chunk_size) / block_size)
                        prev_multiplier = first_chunk_multiplier if prev_chunk == 0 else 1.0
                        prev_local_overhead = overhead_factor * prev_multiplier * (1.0 + 0.2 * (fec_level - 1.0))
                        packets_sent_prev_chunks += int(prev_num_blocks * prev_local_overhead)
                    
                    # Add current chunk's packets
                    total_packets_sent = packets_sent_prev_chunks + j
                    
                    # Show packets sent out of total expected in the progress bar
                    master_pbar.set_postfix(
                        status=f"Chunk {chunk_id+1}/{num_chunks}",
                        speed=f"{overall_mb_per_sec:.2f}MB/s", 
                        packets=f"{total_packets_sent}/{total_packets}"
                    )
            
            # Sleep to maintain desired sending rate (only if rate limiting is active)
            if rate_limited:
                time.sleep(sleep_time)
        
        # Track the time spent on this chunk
        chunk_end_time = time.time()
        chunk_duration = chunk_end_time - (start_time + bytes_sent_time)
        bytes_sent_time += chunk_duration
        
        # No need to restore stdout anymore
        
        # Update master progress bar
        bytes_sent += current_chunk_size
        master_pbar.update(current_chunk_size)
        
        # Update master progress with overall transfer rate
        overall_elapsed = chunk_end_time - start_time
        if overall_elapsed > 0:
            # Calculate application throughput (MB/s)
            overall_rate = bytes_sent / overall_elapsed / (1024 * 1024)
            
            # Calculate wire speed (Mbps)
            # Estimate total packet bytes including overhead
            total_packets_sent = 0
            for i in range(chunk_id + 1):
                # Calculate packets for each chunk processed so far
                chunk_blocks = math.ceil(min(chunk_size, file_size - i * chunk_size) / block_size)
                
                # Use the same calculation as earlier for consistency
                if i == 0:
                    # First chunk uses the first_chunk_multiplier
                    effective_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
                else:
                    # Remaining chunks use standard overhead with FEC adjustment
                    effective_overhead = overhead_factor * fec_adjustment
                    
                total_packets_sent += int(chunk_blocks * effective_overhead)
            
            # More accurate overhead estimation (UDP/IP headers + chunk headers)
            avg_packet_size = block_size + 65  # data + ~65 bytes overhead (UDP/IP + chunk headers)
            total_bytes_on_wire = total_packets_sent * avg_packet_size
            wire_mbps = (total_bytes_on_wire * 8) / overall_elapsed / 1000000
            
            # Calculate completion percentage for packets
            packet_completion_pct = min(100, int(total_packets_sent * 100 / total_packets))
            
            # Update progress bar with clean status including packet information
            master_pbar.set_postfix(
                status="Complete", 
                speed=f"{overall_rate:.2f}MB/s", 
                wire=f"{wire_mbps:.1f}Mbps", 
                packets=f"{total_packets_sent}/{total_packets} ({packet_completion_pct}%)"
            )
        
        # No delay between chunks - process immediately
    
    # Close master progress bar
    master_pbar.close()
    
    elapsed_time = time.time() - start_time
    print(f"Finished sending file in {elapsed_time:.2f} seconds")
    print(f"Average data rate: {file_size/elapsed_time/1024/1024:.2f} MB/sec")
    
    # We already calculated the MD5 checksum at the beginning
    print("Using previously calculated MD5 checksum for EOF marker...")
    
    # Send END signal with filename and MD5 checksum multiple times to ensure it's received
    end_header = b'ENDOFFILE:'
    
    # Structure: ENDOFFILE:filename:md5checksum
    end_data = filename + ":" + file_md5
    end_packet = end_header + end_data.encode('utf-8')
    
    print(f"Sending EOF marker with filename and MD5 checksum...")
    for _ in range(10):  # Send multiple times for redundancy
        sock.sendto(end_packet, dest_addr)
        time.sleep(0.2)  # Slightly longer delay between end signals
    
    sock.close()
    
    # Wait for compressibility analysis thread to complete (up to 2 seconds)
    # If it doesn't complete, we'll just report what we have
    compression_thread.join(timeout=2)
    
    # Print compressibility analysis results
    print("\n" + "="*60)
    print("FILE COMPRESSIBILITY ANALYSIS")
    print("="*60)
    
    if compressibility_results:
        if "error" in compressibility_results:
            print(f"Error during analysis: {compressibility_results['error']}")
        else:
            # Print basic compressibility result in the requested format
            is_compressible = compressibility_results.get('can_be_compressed', False)
            print(f"File {filename} is {'compressible' if is_compressible else 'not compressible'}")
            
            # Provide additional details
            if 'entropy' in compressibility_results:
                print(f"Entropy: {compressibility_results['entropy']:.4f} bits/byte")
            if 'compression_potential' in compressibility_results:
                print(f"Compression potential: {compressibility_results['compression_potential']}")
    else:
        print("Compressibility analysis did not complete in time.")
        
    print("="*60 + "\n")

# This entry point is kept for backwards compatibility
# The actual implementation is in main()
def main():
    """Main entry point when called directly"""
    parser = argparse.ArgumentParser(description="Send a file over UDP with Robust Soliton FEC")
    parser.add_argument("file", nargs="?", help="Path to the file to send")
    parser.add_argument("--host", default="localhost", 
                        help="Destination hostname or IP address for the receiver (IPv4 or IPv6)")
    parser.add_argument("--multicast", default=None, 
                        help="Use multicast mode with the specified multicast group address (e.g., '224.0.0.1' for IPv4 or 'ff02::1' for IPv6)")
    parser.add_argument("--broadcast", action="store_true", 
                        help="Use broadcast mode to send to network broadcast address (IPv4 only)")
    parser.add_argument("--ttl", type=int, default=1, 
                        help="Time-to-live for multicast packets (default: 1)")
    parser.add_argument("--port", type=int, default=12345, 
                        help="Destination port number for the receiver")
    parser.add_argument("--chunk-size", default="10MB", 
                        help="Size of file chunks for processing (e.g., 10MB, 50mb, or bytes as integer). Larger chunks may improve throughput but require more memory.")
    parser.add_argument("--block-size", type=int, default=8192, 
                        help="Size of individual data blocks in bytes. Smaller blocks improve error resilience but increase overhead.")
    parser.add_argument("--packet-rate", type=int, default=None, 
                        help="Limit packets sent per second (e.g., 5000). Default is unlimited for maximum speed.")
    parser.add_argument("--overhead", type=float, default=6.0, 
                        help="Redundancy factor for FEC (e.g., 6.0 = 500 percent more packets than needed). Higher values improve reliability over lossy connections.")
    parser.add_argument("--fec", type=float, default=1.0,
                        help="FEC strength level (1.0-3.0). Higher values adjust Robust Soliton parameters for better error correction at the cost of efficiency.")
    parser.add_argument("--c", type=float, default=0.1, 
                        help="Robust Soliton distribution parameter. Controls the number of high-degree blocks; higher values increase recoverability.")
    parser.add_argument("--delta", type=float, default=0.05, 
                        help="Decoding failure probability target for the Robust Soliton distribution. Lower values improve reliability.")
    parser.add_argument("--first-chunk-multiplier", type=float, default=5.0,
                        help="Multiplier for the first chunk's overhead factor (default: 5.0). Higher values improve initial recovery.")
    
    args = parser.parse_args()
    
    # Check if file is provided
    if args.file is None:
        print("Error: Please specify a file to send.")
        print("Example: datadiode-RobustSoliton send myfile.txt")
        sys.exit(1)
    
    # Validate parameters
    if args.fec <= 0:
        print("Error: FEC level must be greater than 0")
        sys.exit(1)
    
    if args.overhead <= 1:
        print("Error: Overhead factor must be greater than 1")
        sys.exit(1)
        
    if args.first_chunk_multiplier <= 1:
        print("Error: First chunk multiplier must be greater than 1")
        sys.exit(1)
    
    # Validate file exists and can be opened
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
        
    try:
        with open(args.file, 'rb') as f:
            # Just test if we can open it
            pass
    except Exception as e:
        print(f"Error: Unable to open file {args.file}: {e}")
        sys.exit(1)
    
    # Validate network parameters
    import socket
    try:
        # Test if host is valid by attempting to resolve it
        socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"Error: Invalid host or IP address: {args.host}")
        sys.exit(1)
        
    if args.port < 1 or args.port > 65535:
        print(f"Error: Port number must be between 1 and 65535")
        sys.exit(1)
    
    try:
        # Try to install tqdm if not already installed
        import tqdm
    except ImportError:
        print("Installing tqdm for progress bars...")
        import subprocess
        subprocess.call([sys.executable, "-m", "pip", "install", "tqdm"])
        import tqdm
    
    # Parse the chunk size
    chunk_size = parse_size(args.chunk_size)
    print(f"Using chunk size: {chunk_size/1024/1024:.1f} MB")
    
    send_file_chunked(args.file, dest_addr=(args.host, args.port), 
              chunk_size=chunk_size, block_size=args.block_size,
              packet_rate=args.packet_rate, overhead_factor=args.overhead,
              c=args.c, delta=args.delta, fec_level=args.fec, first_chunk_multiplier=args.first_chunk_multiplier,
              multicast=args.multicast, broadcast=args.broadcast, ttl=args.ttl)

if __name__ == "__main__":
    main()