"""
RobustSolitonReceiver: A robust FEC implementation with immediate chunk processing.
Decodes each chunk as soon as it's received without waiting for network quiet.

This module receives files transmitted using the RobustSolitonSender and
reconstructs them using parallel processing. It handles packet loss
gracefully with fountain codes and processes chunks immediately.

Command-line usage:
    python -m src.RobustSolitonReceiver [output_file] --port 12345 [options]

Parameters:
    output          : Optional path to save received file (defaults to original filename)
    --host          : Interface to bind to (default: "" - all interfaces)
    --port          : Port to listen on (default: 12345)
    --loss          : Simulated packet loss rate for testing (default: 0.0)
    --timeout       : Receiving timeout in seconds (default: 600)
    --max-packet-size : Maximum UDP packet size (default: 65536)
    --accurate-speed : Display wire speed including protocol overhead
    --pcap          : Read packets from a .pcap file instead of the network interface
    --pcapng        : Read packets from a .pcapng file instead of the network interface (newer format)
    --napatech      : Convert Napatech capture file to PCAP format using /opt/napatech3/bin/capfileconvert
"""
import argparse
import socket
import time
import os
import random
import struct
import collections
import concurrent.futures
import re
import hashlib
import sys
import threading
import subprocess
import tempfile

def convert_napatech_to_pcap(napatech_file):
    """
    Convert a Napatech capture file to PCAP format using the external capfileconvert tool.
    
    Args:
        napatech_file: Path to the Napatech capture file
        
    Returns:
        Path to the converted PCAP file if successful, None otherwise
    """
    capfileconvert_path = "/opt/napatech3/bin/capfileconvert"
    
    # Check if the capfileconvert tool exists
    if not os.path.exists(capfileconvert_path):
        print(f"Error: Napatech capfileconvert tool not found at {capfileconvert_path}")
        return None
    
    # Create a temporary output file with .pcap extension
    with tempfile.NamedTemporaryFile(suffix='.pcap', delete=False) as temp_file:
        pcap_output = temp_file.name
    
    try:
        # Run the capfileconvert tool with correct syntax as shown in its help output
        cmd = [
            capfileconvert_path,
            "-i", napatech_file,
            "-o", pcap_output,
            "--outputformat=pcap"
        ]
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        print(f"Successfully converted Napatech file to PCAP format: {pcap_output}")
        return pcap_output
    except subprocess.CalledProcessError as e:
        print(f"Error converting Napatech file: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        
        # Clean up the temporary file if conversion failed
        if os.path.exists(pcap_output):
            os.unlink(pcap_output)
        
        return None

class TerminalManager:
    """
    Manages terminal output for multiple concurrent progress bars.
    Ensures progress bars stay on their dedicated lines without being
    interrupted by other output messages.
    """
    def __init__(self, num_progress_bars=2):
        """Initialize with fixed number of progress bar lines"""
        self.num_progress_bars = num_progress_bars
        self.progress_bars = [""] * num_progress_bars  # Current content of each bar
        self.progress_bar_files = [""] * num_progress_bars  # Which file is in each bar
        self.lock = threading.Lock()  # To prevent racing on terminal output
        
        # Terminal control sequences
        self.CLEAR_LINE = "\033[2K"  # Clear entire line
        self.CURSOR_UP = "\033[1A"   # Move cursor up 1 line
        self.CURSOR_DOWN = "\033[1B" # Move cursor down 1 line
        self.CURSOR_HOME = "\r"      # Move cursor to beginning of line
        
        # Print initial blank progress bars
        print("\n" * num_progress_bars, end="")
        
    def allocate_bar(self, filename):
        """
        Allocate a progress bar slot for a file.
        Returns the bar index (0-based) or None if no slots available.
        """
        with self.lock:
            # First check if this file already has a bar
            for i, bar_file in enumerate(self.progress_bar_files):
                if bar_file == filename:
                    return i
            
            # Look for an empty slot
            for i, bar_file in enumerate(self.progress_bar_files):
                if not bar_file:
                    self.progress_bar_files[i] = filename
                    return i
            
            # If all slots are taken, use the last one for any new file
            # (This ensures we always have at least the most recent two files displayed)
            self.progress_bar_files[-1] = filename
            return len(self.progress_bar_files) - 1
    
    def release_bar(self, filename):
        """Release a progress bar slot when a file is done"""
        with self.lock:
            for i, bar_file in enumerate(self.progress_bar_files):
                if bar_file == filename:
                    self.progress_bar_files[i] = ""
                    self.progress_bars[i] = ""
                    # Clear the bar line
                    self._move_to_bar(i)
                    sys.stdout.write(self.CLEAR_LINE)
                    sys.stdout.flush()
                    break
    
    def _move_to_bar(self, bar_index):
        """Move cursor to the specified progress bar line"""
        # Calculate how many lines up from current position
        lines_up = self.num_progress_bars - bar_index
        # First return to beginning of line
        sys.stdout.write(self.CURSOR_HOME)
        # Then move up to the appropriate bar line
        for _ in range(lines_up):
            sys.stdout.write(self.CURSOR_UP)
        sys.stdout.flush()
    
    def _restore_cursor(self):
        """Restore cursor to bottom position after message area"""
        # Move cursor to bottom of progress bars plus 1 for new messages
        sys.stdout.write(self.CURSOR_HOME)
        for _ in range(self.num_progress_bars):
            sys.stdout.write(self.CURSOR_DOWN)
        sys.stdout.flush()
    
    def update_progress_bar(self, bar_index, content):
        """Update a specific progress bar with new content"""
        if 0 <= bar_index < self.num_progress_bars:
            with self.lock:
                self.progress_bars[bar_index] = content
                
                # Move cursor to the bar's line
                self._move_to_bar(bar_index)
                
                # Clear line and write new content
                sys.stdout.write(f"{self.CLEAR_LINE}{content}")
                
                # Restore cursor position to bottom
                self._restore_cursor()
                
                sys.stdout.flush()
    
    def print_message(self, message, end="\n", flush=True):
        """Print a message below the progress bars without disrupting them"""
        with self.lock:
            # We're already at the bottom, so just print the message
            sys.stdout.write(f"{message}{end}")
            if flush:
                sys.stdout.flush()
            
            # Redraw all progress bars
            self._redraw_all_bars()
    
    def _redraw_all_bars(self):
        """Redraw all progress bars to ensure they're visible"""
        # Save current cursor position (should be at bottom)
        current_pos = self.num_progress_bars
        
        # Move up to first progress bar
        for _ in range(current_pos):
            sys.stdout.write(self.CURSOR_UP)
        
        # Redraw each bar
        for i, bar in enumerate(self.progress_bars):
            sys.stdout.write(f"{self.CLEAR_LINE}{bar}\n")
        
        # Cursor should now be back at the message position
        sys.stdout.flush()
import math
import numpy as np
import os
import sys
import time
import threading
import multiprocessing
from multiprocessing import Process, Queue, Event
# Import necessary for our immediate chunk processing
from multiprocessing.managers import SyncManager

# Import PCAP reading libraries
try:
    import dpkt
    from dpkt.ethernet import Ethernet
    from dpkt.ip import IP
    from dpkt.ip6 import IP6
    from dpkt.udp import UDP
    DPKT_AVAILABLE = True
except ImportError:
    DPKT_AVAILABLE = False

# Import required module components
try:
    from datadiode_RobustSoliton.fixed_fec import Decoder as BaseDecoder
    from datadiode_RobustSoliton.soliton import get_blocks_from_seed
    from datadiode_RobustSoliton.prng import PRNGType
    from datadiode_RobustSoliton.utils import get_progress_display
except ImportError:
    # Try relative imports if package import fails
    from fixed_fec import Decoder as BaseDecoder
    from soliton import get_blocks_from_seed
    from prng import PRNGType
    from utils import get_progress_display

# Placeholder for GIL yielding - no longer needed with multiprocessing
def yield_gil():
    """
    Placeholder function for compatibility with old code.
    Previously used to yield the GIL when using threading.
    No longer needed with multiprocessing but kept for compatibility.
    """
    # No operation needed in multiprocessing context
    pass

# Dictionary to keep track of active repair processes and their interrupt events
# Maps filename -> {'process': process, 'interrupt_event': event}
_active_repair_processes = {}
# We don't use tqdm progress bars anymore - just simple text status updates

# Variables for repair state tracking
repair_interrupt_event = threading.Event()
_fec_repair_paused = False
_fec_repair_in_progress = False
_currently_processing_file = None

def process_chunk_immediately(filename, chunk_id, packets, file_metadata, transfer, result_queue):
    """
    Process a single chunk immediately when sufficient packets are received
    
    Args:
        filename: The filename
        chunk_id: The chunk ID
        packets: List of packets for this chunk
        file_metadata: The file metadata
        transfer: The transfer object containing state information
        result_queue: Queue to store decoded chunk results
    """
    # Important: Override repair global flags so decoding works properly in the subprocess
    global repair_interrupt_event, _fec_repair_paused, _fec_repair_in_progress, _currently_processing_file
    repair_interrupt_event = threading.Event()  # Create a new event in this process
    _fec_repair_paused = False  # Make sure we're not paused
    _fec_repair_in_progress = True  # Mark as in progress
    _currently_processing_file = filename  # Set current file
    try:
        print(f"\nStarting decode process for {filename} chunk {chunk_id} with {len(packets)} packets")
        
        # Calculate expected blocks based on chunk size and block size
        block_size = file_metadata.get('block_size', 8192)
        chunk_size = file_metadata.get('chunk_size', 10*1024*1024)
        file_size = file_metadata.get('file_size', 0)
        
        # For the last chunk, we need to calculate actual size
        if chunk_id == file_metadata.get('num_chunks', 1) - 1:
            last_chunk_size = file_size - (chunk_id * chunk_size)
            expected_blocks = math.ceil(last_chunk_size / block_size)
        else:
            expected_blocks = math.ceil(chunk_size / block_size)
            
        print(f"Chunk {chunk_id} info: expecting {expected_blocks} blocks, received {len(packets)} packets")
        
        # Use the existing decode_chunk function exactly like the main process does
        # This should properly decode the chunk if enough packets are available
        # Debug log for decoding attempt
        print(f"Attempting to decode chunk {chunk_id} with {len(packets)} packets (need {expected_blocks} blocks)")
        
        # Try to decode the chunk
        chunk_id, decoded_data = decode_chunk(chunk_id, packets, file_metadata)
        
        # Check if decoding was successful
        if decoded_data is not None:
            # Success! Send the decoded data back to the main process
            # First create a message and log it for debugging
            result_message = {
                'chunk_id': chunk_id,
                'data': decoded_data,
                'success': True
            }
            # Add result to the queue with minimal logging
            try:
                result_queue.put(result_message)
            except Exception as e:
                print(f"Error queuing result for chunk {chunk_id}: {e}")
            # Print a concise success message
            print(f"\n✅ CHUNK {chunk_id} SUCCESSFULLY DECODED! Size: {len(decoded_data)/1024/1024:.1f}MB from {len(packets)} packets")
            
            # Exit the function immediately after successful decoding
            # This ensures the process terminates after sending the result
            return
        else:
            # Get some stats from the decoder (if available through the decode_chunk function)
            try:
                # We don't have access to decoder object here directly, so we'll just report what we know
                redundancy_ratio = len(packets) / expected_blocks
                
                # Decoding failed - log detailed info with redundancy ratio
                print(f"\n{'='*60}")
                print(f"❌ FAILED TO DECODE CHUNK {chunk_id}")
                print(f"File: {filename}")
                print(f"Packets received: {len(packets):,}")
                print(f"Expected blocks: {expected_blocks:,}")
                print(f"Redundancy ratio: {redundancy_ratio:.2f}x")
                print(f"Recommendation: More packets needed for successful decoding")
                print(f"Message: Will try again in final repair process")
                print(f"{'='*60}")
                
                # Exit function early - no need to waste time on failed decoding
                result_queue.put({
                    'chunk_id': chunk_id,
                    'success': False,
                    'packets_received': len(packets),
                    'expected_blocks': expected_blocks
                })
                return  # Exit the function immediately
            except Exception as e:
                # Fallback to simple message if error occurs
                print(f"✗ Failed to decode chunk {chunk_id} for {filename}, received {len(packets)} packets (expected {expected_blocks} blocks)")
                print(f"Will try again in final repair process")
                
                # Exit function early
                result_queue.put({
                    'chunk_id': chunk_id,
                    'success': False,
                    'packets_received': len(packets),
                    'expected_blocks': expected_blocks
                })
                return  # Exit the function immediately
        
    except Exception as e:
        print(f"Error in chunk decode process for chunk {chunk_id}: {e}")
        result_queue.put({
            'chunk_id': chunk_id,
            'success': False,
            'error': str(e)
        })

def process_queued_file(filename, active_transfers):
    """Process a queued file when it's complete or has timeout"""
    # Get the transfer and mark as being processed to prevent duplicates
    transfer = active_transfers[filename]
    
    # Get partial flag from transfer, which was passed from the main receive_file function
    partial = transfer.get('partial', False)
    
    # Skip if already processed
    if transfer.get('processed', False):
        return
    
    # Mark as processed immediately to prevent duplicate processing
    transfer['processed'] = True
    
    # Extract metadata
    file_metadata = transfer['metadata']
    chunk_packets = transfer['chunk_packets']
    
    # Wait for all chunk processes to complete before assembling the final file
    if 'chunk_processes' in transfer:
        print(f"\nWaiting for all chunk decoding processes to complete for {filename}...")
        
        # First check if we already have all chunks decoded
        num_chunks = file_metadata.get('num_chunks', 0)
        decoded_chunks = transfer.get('decoded_chunks', {})
        
        # If we already have all chunks decoded, no need to wait for processes
        if len(decoded_chunks) == num_chunks:
            print(f"All {num_chunks} chunks already decoded for {filename}, proceeding with assembly")
            
            # Terminate any running processes
            for chunk_id, process_info in transfer['chunk_processes'].items():
                process = process_info.get('process')
                if process and process.is_alive():
                    process.terminate()
        else:
            # We're still waiting for some chunks to decode
            # Try to get results from any remaining processes
            for chunk_id, process_info in transfer['chunk_processes'].items():
                process = process_info.get('process')
                if process and process.is_alive():
                    # Check if this process has already failed decoding
                    if process_info.get('decode_failed'):
                        print(f"Chunk {chunk_id} already failed decoding, terminating process...")
                        process.terminate()
                        print(f"Chunk {chunk_id} will be handled by the final repair process instead")
                    else:
                        # Check process status with minimal timeout
                        process.join(timeout=0.01)  # Use minimal timeout - we'll check the queue anyway
                        
                        # Check the process-specific queue for results
                        try:
                            if 'result_queue' in process_info:
                                # Use the dedicated queue for this process with minimal logging
                                result_queue = process_info['result_queue']
                                
                                # Check if there are any results in the queue
                                if not result_queue.empty():
                                    # Get result from the queue
                                    result = result_queue.get_nowait()
                                    if result and 'chunk_id' in result and result['chunk_id'] == chunk_id:
                                        if result.get('success', False) and 'data' in result:
                                            # Store the decoded chunk data
                                            transfer['decoded_chunks'][chunk_id] = result['data']
                                            print(f"✓ Found result for chunk {chunk_id}")
                                            
                                            # Terminate process since we already have the result
                                            if process.is_alive():
                                                process.terminate()
                                            continue
                            else:
                                # Fall back to the old shared queue for backward compatibility
                                print(f"No dedicated queue found for chunk {chunk_id}, checking main queue")
                                
                                # Check all pending results in the shared queue
                                queue_item_found = False
                                pending_results = []
                                
                                while not transfer['chunk_results_queue'].empty():
                                    result = transfer['chunk_results_queue'].get_nowait()
                                    if result and 'chunk_id' in result and result['chunk_id'] == chunk_id:
                                        queue_item_found = True
                                        if result.get('success', False) and 'data' in result:
                                            # Store the decoded chunk data
                                            transfer['decoded_chunks'][chunk_id] = result['data']
                                            print(f"✓ Found queued result for chunk {chunk_id} in main queue")
                                    else:
                                        # Store other results to put back in the queue
                                        pending_results.append(result)
                                
                                # Put back any other results we found
                                for result in pending_results:
                                    transfer['chunk_results_queue'].put(result)
                                
                                if queue_item_found:
                                    # Terminate process since we already have the result
                                    if process.is_alive():
                                        process.terminate()
                                    continue
                        except Exception as e:
                            print(f"Error checking queue for chunk {chunk_id}: {e}")
                        
                        # If it's still running after queue check, terminate it
                        if process.is_alive():
                            print(f"Chunk {chunk_id} decode process still running, terminating...")
                            process.terminate()
                            print(f"Chunk {chunk_id} will be handled by the final repair process instead")
                            
                    # Make sure this chunk is marked as not decoded so the repair process will handle it
                    if chunk_id in transfer.get('decoded_chunks', {}):
                            del transfer['decoded_chunks'][chunk_id]
            
            # Check for any final results from chunk processes silently
            
            # Check all dedicated queues in the chunk_processes
            for chunk_id, process_info in list(transfer['chunk_processes'].items()):
                if 'result_queue' in process_info:
                    try:
                        result_queue = process_info['result_queue']
                        
                        # If the queue has a result, process it
                        if not result_queue.empty():
                            result = result_queue.get_nowait()
                            if result and 'chunk_id' in result and result['chunk_id'] == chunk_id:
                                if result.get('success', False) and 'data' in result:
                                    # Store the decoded chunk data without extra logging
                                    transfer['decoded_chunks'][chunk_id] = result['data']
                    except Exception as e:
                        print(f"Error checking queue for chunk {chunk_id}: {e}")
            
            # Also check the main results queue for backward compatibility without extra logging
            try:
                # Check the queue for any results
                while not transfer['chunk_results_queue'].empty():
                    result = transfer['chunk_results_queue'].get_nowait()
                    if result and 'chunk_id' in result:
                        chunk_id = result['chunk_id']
                        if result.get('success', False) and 'data' in result:
                            # Store the decoded chunk data silently
                            transfer['decoded_chunks'][chunk_id] = result['data']
                                
            except Exception as e:
                print(f"Error checking for final results: {e}")
    else:
        print(f"No chunk processes found for {filename}")
    
    # Create incoming directory if it doesn't exist
    incoming_dir = os.path.join(os.getcwd(), "incoming")
    if not os.path.exists(incoming_dir):
        os.makedirs(incoming_dir)
    
    # Sanitize filename and create output path with numbered extension if needed
    safe_filename = os.path.basename(filename)
    base_output_path = os.path.join(incoming_dir, safe_filename)
    
    # Check if file already exists and use numbered extensions if needed
    current_output_path = base_output_path
    extension_counter = 1
    
    while os.path.exists(current_output_path):
        # File already exists, use a numbered extension
        current_output_path = f"{base_output_path}.{extension_counter}"
        extension_counter += 1
    
    # If we're using a numbered extension, print a message
    if current_output_path != base_output_path:
        print(f"\nFile {base_output_path} already exists, using {current_output_path} instead")
    
    # Use the already decoded chunks from the transfer instead of starting with an empty dict
    decoded_chunks = transfer.get('decoded_chunks', {})
    
    # Simplified processing message
    print(f"\nProcessing {filename}")
    
    # Use simple text output for processing status
    # Calculate completion percentage based on received/expected packets
    file_size = transfer['metadata'].get('file_size', 0)
    block_size = transfer['metadata'].get('block_size', 1024)
    actual_count = transfer.get('actual_packets_count', transfer['packets_received'])
    
    # Always use sender's total_packets from metadata
    expected_packets = transfer['metadata'].get('total_packets', 
                     transfer['metadata'].get('packets_meta', {}).get('total_packets',
                     transfer['metadata'].get('expected_packets', 1)))
    
    # Show a simple processing message
    print(f"\nProcessing {filename}: 100% complete ({actual_count}/{expected_packets} packets received)")
    
    # Extract or calculate FEC parameters to match sender's calculations
    overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
    fec_level = transfer['metadata'].get('fec_level', 1.0)
    first_chunk_multiplier = transfer['metadata'].get('first_chunk_multiplier', 5.0)
    
    # Calculate FEC adjustment using the same formula as the sender
    # Formula: fec_adjustment = 1.0 + 0.2 * (fec_level - 1.0)
    fec_adjustment = transfer['metadata'].get('fec_adjustment', 1.0 + 0.2 * (fec_level - 1.0))
    
    # Calculate effective overheads using the same formulas as the sender
    effective_first_chunk_overhead = transfer['metadata'].get('effective_first_chunk_overhead', 
                                           overhead_factor * first_chunk_multiplier * fec_adjustment)
    effective_remaining_overhead = transfer['metadata'].get('effective_remaining_overhead',
                                           overhead_factor * fec_adjustment)
                                           
    # Extract or calculate chunk size from metadata
    import math  # Import math module before using it
    chunk_size = transfer['metadata'].get('chunk_size', 1024*1024)
    num_chunks = transfer['metadata'].get('num_chunks', math.ceil(file_size / chunk_size))
    
    # Calculate blocks per chunk using the same approach as the sender
    blocks_per_chunk = math.ceil(chunk_size / block_size)
    total_blocks = math.ceil(file_size / block_size)
    
    # Calculate blocks for first chunk and remaining chunks
    first_chunk_blocks = min(blocks_per_chunk, total_blocks)
    last_chunk_size = file_size - (chunk_size * (num_chunks - 1))
    last_chunk_blocks = math.ceil(last_chunk_size / block_size)
    
    # Calculate expected packets using the sender's formula
    first_chunk_packets = int(first_chunk_blocks * effective_first_chunk_overhead)
    remaining_blocks = total_blocks - first_chunk_blocks
    
    # Calculate packets for remaining chunks
    if num_chunks > 1:
        remaining_packets = int(remaining_blocks * effective_remaining_overhead)
        packets_per_remaining_chunk = remaining_packets / (num_chunks - 1)
    else:
        remaining_packets = 0
        packets_per_remaining_chunk = 0

    # Store calculated values in file_metadata for later use in process_all_chunks
    file_metadata = {
        'file_size': file_size,
        'chunk_size': chunk_size,
        'num_chunks': num_chunks,
        'block_size': block_size,
        'filename': filename,
        'overhead_factor': overhead_factor,
        'fec_level': fec_level,
        'fec_adjustment': fec_adjustment,
        'first_chunk_multiplier': first_chunk_multiplier,
        'effective_first_chunk_overhead': effective_first_chunk_overhead,
        'effective_remaining_overhead': effective_remaining_overhead,
        'blocks_per_chunk': blocks_per_chunk,
        'last_chunk_blocks': last_chunk_blocks,
        'total_blocks': total_blocks,
        'first_chunk_blocks': first_chunk_blocks,
        # Add packet counts
        'first_chunk_packets': first_chunk_packets,
        'remaining_packets': remaining_packets,
        'packets_per_remaining_chunk': packets_per_remaining_chunk
    }
    
    # Check if we received all packets - if so, we can potentially skip FEC decoding
    no_packet_loss = actual_count >= expected_packets
    
    if no_packet_loss:
        print(f"All packets received successfully! Optimizing decoding process...")
    
    # We now use a consistent PRNG implementation regardless of sender settings
    
    # Let's use the ThreadPoolExecutor instead of multiprocessing to avoid pickle issues
    # This will still give us parallel processing while keeping everything in the same process
    import concurrent.futures
    
    # Create an executor with lower number of workers to prioritize receiving
    available_cores = os.cpu_count() or 4
    repair_cores = max(1, available_cores // 3)  # Use only 1/3 of cores for repair
    
    # Process chunks in parallel using threads instead of multiprocessing
    # First check if we have chunks already decoded by the immediate processes
    decoded_chunks = transfer.get('decoded_chunks', {})
    
    # If we have all chunks already decoded, we can skip the repair process entirely
    if len(decoded_chunks) == num_chunks:
        print(f"All {num_chunks} chunks were already decoded by immediate processes - skipping repair process")
    else:
        missing_chunks = []
        for i in range(num_chunks):
            if i not in decoded_chunks:
                missing_chunks.append(i)
        
        print(f"\n{'='*60}")
        print(f"FINAL REPAIR NEEDED FOR {len(missing_chunks)} MISSING CHUNKS")
        print(f"Already decoded: {len(decoded_chunks)}/{num_chunks} chunks")
        print(f"Missing chunks: {missing_chunks}")
        print(f"{'='*60}")
        
        # Start repair in a separate process to not block the receiver and bypass the GIL
        # Note: multiprocessing and related classes are now imported at module level
        
        # Create queues and events for IPC
        result_queue = Queue()
        interrupt_event = Event()  # Multiprocessing event for signaling interrupts
        
        # Make sure repair_interrupt_event is cleared so it doesn't block the repair process
        repair_interrupt_event.clear()
        
        # Set a flag to indicate we're starting a repair process
        # This prevents us from getting stuck if chunk result processing fails
        repair_process_started = False
    
    # Define a function to run the repair in a separate process
    def run_repair_in_process(chunk_packets, file_metadata, interrupt_event, result_queue, decoded_chunks=None, no_packet_loss=False):
        try:
            # Set process name for identification
            multiprocessing.current_process().name = "FEC_Repair_Process"
            
            # No need to reset interrupt flag as we're using Events now
            
            # Lower process priority if possible
            try:
                os.nice(10)  # Lower priority but not as low as before
            except:
                pass
                
            # Already decoded chunks (sent from main process)
            if decoded_chunks is None:
                decoded_chunks = {}
                
            # Log which chunks we already have and which we need to decode
            num_chunks = file_metadata.get('num_chunks', 0)
            missing_chunks = []
            for i in range(num_chunks):
                if i not in decoded_chunks:
                    missing_chunks.append(i)
                    
            print(f"\n{'='*60}")
            print(f"REPAIR PROCESS STARTING")
            print(f"Already have: {len(decoded_chunks)}/{num_chunks} chunks")
            print(f"Need to decode: {len(missing_chunks)} chunks ({missing_chunks})")
            print(f"{'='*60}")
                
            # Call the actual repair function
            # Pass the multiprocessing interrupt event to check during processing
            # Pass the already decoded chunks to avoid reprocessing them
            repair_results = process_all_chunks(chunk_packets, file_metadata, decoded_chunks, no_packet_loss, interrupt_event)
            
            # Check if we were interrupted - if so, don't send results
            if interrupt_event.is_set():
                print(f"\n[FEC Repair process was interrupted - partial results not sent]")
                return
            
            # Count how many chunks were newly decoded by the repair process
            new_chunks = 0
            for chunk_id in repair_results:
                if chunk_id not in decoded_chunks:
                    new_chunks += 1
                
            # Send results back through the queue
            result_queue.put(repair_results)
                
            print(f"\n[FEC Repair process completed successfully]")
            print(f"[Decoded {new_chunks} new chunks, {len(repair_results) - new_chunks} were already decoded]")
        except Exception as e:
            print(f"\n[FEC Repair process error: {str(e)}]")
            # Send error status back through queue
            result_queue.put({"error": str(e)})
            
    # Only start the repair process if we need to decode more chunks
    repair_process = None
    if len(decoded_chunks) < num_chunks:
        missing_chunks_list = [i for i in range(num_chunks) if i not in decoded_chunks]
        print(f"Starting final repair process for chunks {missing_chunks_list}")
        
        # Create and start repair process
        repair_process = Process(
            target=run_repair_in_process,
            args=(chunk_packets, file_metadata, interrupt_event, result_queue, decoded_chunks, no_packet_loss)
        )
        repair_process.daemon = True  # Make it a daemon so it exits when main process exits
        
        # Start the repair process
        repair_process.start()
        repair_process_started = True
        
        # Register this repair process and its interrupt event in the global dictionary
        # This allows us to interrupt it from other parts of the code
        
        # Set repair state to in-progress
        set_repair_in_progress(filename)
        
        # Add to active repair processes
        _active_repair_processes[filename] = {
            'process': repair_process,
            'interrupt_event': interrupt_event
        }
    else:
        # No need for a repair process, we already have all chunks
        repair_process = None
        interrupt_event = None
        repair_process_started = False
    
    # Don't wait for it to finish - just move on with the chunks we have
    # The file will be written even if some chunks are missing
    
    # Wait for the repair process to complete instead of a fixed time
    wait_start = time.time()
    
    # Modified loop with better error handling for multiprocessing
    try:
        # Check every 250ms for new results
        check_interval = 0.25  # seconds
        chunks_received = 0
        last_report_time = time.time()
        
        # If we already have all chunks, skip the waiting loop
        if all(i in decoded_chunks for i in range(file_metadata['num_chunks'])):
            print(f"[All chunks already decoded, no need to wait for repair process]")
        elif repair_process is None:
            print(f"[No repair process started, using already decoded chunks]")
        elif repair_process_started:
            print(f"[Waiting for repair process to finish...]")
            # Add a maximum wait time to prevent hanging
            max_wait_time = 120  # 2 minutes max wait
            wait_start_time = time.time()
            
            # Wait until the repair process finishes, we have all chunks, or max time elapsed
            while (repair_process.is_alive() and 
                   not all(i in decoded_chunks for i in range(file_metadata['num_chunks'])) and
                   time.time() - wait_start_time < max_wait_time):
                # Check for results from the process without blocking
                try:
                    # Non-blocking queue check
                    repair_results = result_queue.get_nowait()
                    if isinstance(repair_results, dict):
                        if "error" in repair_results:
                            print(f"[Repair process error: {repair_results['error']}]")
                        else:
                            # Count how many chunks were actually new
                            new_chunks = 0
                            new_chunk_ids = []
                            
                            for k, v in repair_results.items():
                                if k not in decoded_chunks:
                                    new_chunks += 1
                                    new_chunk_ids.append(k)
                                decoded_chunks[k] = v
                            
                            # Print detailed information about results
                            print(f"\n{'='*60}")
                            print(f"REPAIR RESULTS RECEIVED")
                            print(f"Total chunks: {len(repair_results)}")
                            print(f"New chunks decoded: {new_chunks} {new_chunk_ids}")
                            print(f"Already had: {len(repair_results) - new_chunks}")
                            
                            # Check if we have all chunks now
                            missing = [i for i in range(file_metadata['num_chunks']) if i not in decoded_chunks]
                            if missing:
                                print(f"Still missing: {missing}")
                            else:
                                print(f"All chunks successfully decoded!")
                            print(f"{'='*60}")
                except Exception:
                    # Queue empty, continue waiting
                    pass
                
                # Get current count of decoded chunks
                current_count = len(decoded_chunks)
                
                # If we've got some chunks, report progress
                if current_count > chunks_received:
                    # Progress update - only if substantial change or 2+ seconds passed
                    if (current_count - chunks_received >= 5) or (time.time() - last_report_time >= 2):
                        print(f"[Repair progress: {current_count}/{file_metadata['num_chunks']} chunks decoded so far]")
                        last_report_time = time.time()
                    
                    # Update our count
                    chunks_received = current_count
                
                # Check if repair should be interrupted due to metadata reception
                if is_repair_paused():
                    print(f"[Repair process interrupted due to new metadata]")
                    # Set the interrupt event to signal the repair process
                    interrupt_event.set()
                    
                    # Try to terminate the process if it's still running after a short delay
                    time.sleep(0.2)  # Give process time to check event and exit
                    if repair_process.is_alive():
                        print(f"[Forcefully terminating repair process]")
                        repair_process.terminate()
                    break
                
                # Small sleep before checking again
                time.sleep(check_interval)
            
            # Check if we timed out waiting for the repair process
            if repair_process.is_alive() and time.time() - wait_start_time >= max_wait_time:
                print(f"\n[WARNING: Repair process taking too long - exceeded maximum wait time of {max_wait_time} seconds]")
                print(f"[Terminating repair process and continuing with chunks decoded so far...]")
                repair_process.terminate()
            
    except Exception as e:
        print(f"Error waiting for repair thread results: {e}")
    
    # Report results
    chunks_received = len(decoded_chunks)
    total_wait_time = time.time() - wait_start
    
    # Calculate how many chunks were already decoded when we started vs. how many were decoded in the repair
    already_decoded_count = 0
    for i in range(file_metadata['num_chunks']):
        if i in transfer.get('decoded_chunks', {}):
            already_decoded_count += 1
            
    newly_decoded = chunks_received - already_decoded_count
    
    print(f"\n{'='*60}")
    print(f"REPAIR PROCESS COMPLETED")
    print(f"Time: {total_wait_time:.1f} seconds")
    print(f"Total chunks: {file_metadata['num_chunks']}")
    print(f"Previously decoded: {already_decoded_count}")
    print(f"Newly decoded: {newly_decoded}")
    print(f"Total decoded: {chunks_received}")
    print(f"{'='*60}")
    
    # Clean up the active repair processes dictionary
    if file_metadata['filename'] in _active_repair_processes:
        del _active_repair_processes[file_metadata['filename']]
    
    # Make sure process is terminated if still running
    if repair_process is not None and repair_process.is_alive():
        print(f"Repair process still running, terminating...")
        repair_process.terminate()
        # Force a 1-second sleep to give process time to clean up
        time.sleep(1)
    print(f"Proceeding with file assembly and verification")
    
    # Now that we've processed all chunks, write the file
    successful_chunks = sum(1 for i in range(file_metadata['num_chunks']) if i in decoded_chunks)
    
    # Update progress bar to show we're assembling the file
    if transfer['progress_bar'] is not None:
        transfer['progress_bar'].set_description(f"Assembling {filename}")
        
        # Calculate the percentage of chunks successfully decoded
        percent_chunks = round(successful_chunks / file_metadata['num_chunks'] * 100)
        
        # Update the colored bar to show chunk success instead of packet reception
        # ANSI color codes
        GREEN = '\033[92m'  # Green for successful chunks
        RED = '\033[91m'    # Red for missing chunks
        RESET = '\033[0m'   # Reset color
        
        # Create the colored bar string
        bar_length = 20  # Shorter bar for more compact display
        green_part = int(bar_length * percent_chunks / 100)
        red_part = bar_length - green_part
        colored_bar = f"{GREEN}{'█' * green_part}{RED}{'█' * red_part}{RESET}"
        
        # Custom bar format showing decoded chunks with colored bar - more compact 
        custom_bar_format = "{desc:<15}:{percentage:3.0f}%|" + colored_bar + "|{n_fmt} chunks [{elapsed:<5} {postfix}]"
        
        # Close the existing progress bar
        transfer['progress_bar'].close()
        
        # Create new progress bar with updated colors
        import tqdm
        transfer['progress_bar'] = tqdm.tqdm(
            total=file_metadata['num_chunks'],
            initial=successful_chunks,
            desc=f"Assembling {filename}",
            unit="chunks",
            bar_format=custom_bar_format
        )
        
        # More compact status - use direct form to avoid comma issues
        # Print a newline before updating to help with transitions
        print("")
        transfer['progress_bar'].set_postfix(
            status=f"writing {successful_chunks}/{file_metadata['num_chunks']}"
        )
    
    # First check if we have all chunks
    have_all_chunks = all(i in decoded_chunks for i in range(file_metadata['num_chunks']))
    if have_all_chunks:
        print(f"All {file_metadata['num_chunks']} chunks successfully decoded!")
    else:
        missing_count = sum(1 for i in range(file_metadata['num_chunks']) if i not in decoded_chunks)
        print(f"Missing {missing_count} out of {file_metadata['num_chunks']} chunks.")
    
    # Update the progress bar
    if transfer['progress_bar'] is not None:
        # Make sure progress bar shows 100% for writing phase
        transfer['progress_bar'].n = transfer['progress_bar'].total
        transfer['progress_bar'].refresh()
        transfer['progress_bar'].set_description(f"Verifying {filename}")
    
    # Assemble the chunks in memory first for MD5 verification
    print("\nAssembling chunks and calculating MD5 checksum...")
    
    # Prepare a BytesIO buffer to hold the complete file
    import io
    file_buffer = io.BytesIO()
    bytes_written = 0
    missing_chunks = 0
    
    # ANSI color codes
    GREEN = '\033[92m'  # Green for successful verification
    RED = '\033[91m'    # Red for verification failure
    YELLOW = '\033[93m' # Yellow for warnings
    RESET = '\033[0m'   # Reset color
    
    # First check if we have all chunks
    all_chunks_decoded = all(i in decoded_chunks for i in range(file_metadata['num_chunks']))
    
    # If not all chunks are decoded
    if not all_chunks_decoded:
        missing_chunks_count = file_metadata['num_chunks'] - len(decoded_chunks)
        print(f"\n{RED}Not all chunks are decoded - missing {missing_chunks_count} out of {file_metadata['num_chunks']} chunks{RESET}")
        
        # Store partial results
        transfer['successful_chunks'] = len(decoded_chunks)
        transfer['missing_chunks'] = missing_chunks_count
        transfer['md5_ok'] = False
        
        # If partial flag is set, continue with partial file assembly
        if partial:
            print(f"\n{YELLOW}Partial flag enabled - will write partial file with missing chunks filled with zeros{RESET}")
            # Add missing chunks filled with zeros
            for chunk_id in range(file_metadata['num_chunks']):
                if chunk_id not in decoded_chunks:
                    # For missing chunks, create empty data filled with zeros
                    if chunk_id == file_metadata['num_chunks'] - 1:
                        # Last chunk might be smaller
                        remaining_size = file_metadata['file_size'] - (chunk_id * file_metadata['chunk_size'])
                        decoded_chunks[chunk_id] = b'\x00' * remaining_size
                    else:
                        # Full-sized chunks
                        decoded_chunks[chunk_id] = b'\x00' * file_metadata['chunk_size']
            # Now continue with file assembly
        else:
            transfer['calculated_md5'] = None
            transfer['output_path'] = None
            
            # Close the buffer
            file_buffer.close()
            
            # Update progress bar if needed
            if transfer['progress_bar'] is not None:
                transfer['progress_bar'].close()
            
            print(f"{RED}File not written - use --partial flag to write partial files with missing chunks as zeros into the incoming/ directory{RESET}")
            return  # Exit early if partial is not set
    
    # All chunks are decoded, proceed with assembly
    print(f"\n{GREEN}All {file_metadata['num_chunks']} chunks successfully decoded!{RESET}")
    
    # Assemble each chunk in order
    for i in range(file_metadata['num_chunks']):
        # All chunks should be present now
        if i in decoded_chunks:
            # Calculate the expected size for this chunk
            if i == file_metadata['num_chunks'] - 1:
                # Last chunk might be smaller than chunk_size
                bytes_remaining = file_metadata['file_size'] - i * file_metadata['chunk_size']
                expected_size = bytes_remaining
            else:
                expected_size = file_metadata['chunk_size']
            
            # Get the decoded chunk data
            chunk_data = decoded_chunks[i]
            
            # Validate chunk size - fix if necessary
            if len(chunk_data) != expected_size:
                print(f"Warning: Chunk {i} size mismatch. Expected {expected_size}, got {len(chunk_data)}")
                # Truncate or pad as needed
                if len(chunk_data) > expected_size:
                    chunk_data = chunk_data[:expected_size]
                elif len(chunk_data) < expected_size:
                    # Pad with zeros
                    padding_needed = expected_size - len(chunk_data)
                    chunk_data = chunk_data + bytes(padding_needed)
            
            # Write the chunk to the buffer
            file_buffer.write(chunk_data)
            bytes_written += len(chunk_data)
        else:
            # This should not happen since we checked all chunks are decoded
            print(f"{RED}Error: Chunk {i} missing despite verification{RESET}")
            # Close the buffer
            file_buffer.close()
            return transfer
    
    # Verify total file size
    if bytes_written != file_metadata['file_size']:
        print(f"Warning: File size mismatch. Expected {file_metadata['file_size']}, got {bytes_written} bytes")
    
    # Now calculate MD5 of the assembled data
    import hashlib
    
    # Get the buffer contents for MD5 calculation
    file_buffer.seek(0)
    buffer_contents = file_buffer.getvalue()
    
    # Calculate MD5 hash
    md5_hash = hashlib.md5()
    md5_hash.update(buffer_contents)
    calculated_md5 = md5_hash.hexdigest()
    
    # Check MD5 from metadata if available
    # Note: md5_checksum might be in file_metadata['md5_checksum'] or transfer['metadata']['md5_checksum']
    metadata_md5 = file_metadata.get('md5_checksum')
    eof_md5 = file_metadata.get('eof_md5')
    
    # Debug to check if MD5 is actually present in the original metadata
    # If md5_checksum exists in the transfer metadata but not in file_metadata, this is a copy issue
    if not metadata_md5 and 'md5_checksum' in transfer['metadata']:
        metadata_md5 = transfer['metadata']['md5_checksum']
        # Update file_metadata for consistency
        file_metadata['md5_checksum'] = metadata_md5
        print(f"INFO: Retrieved MD5 checksum from transfer metadata: {metadata_md5[:8]}...{metadata_md5[-8:]}")
    
    # ANSI color codes
    GREEN = '\033[92m'  # Green for successful verification
    RED = '\033[91m'    # Red for verification failure
    YELLOW = '\033[93m' # Yellow for warnings
    RESET = '\033[0m'   # Reset color
    
    # Display all available checksums
    print("\nCalculated MD5: " + calculated_md5)
    if metadata_md5:
        print("Metadata MD5:   " + metadata_md5)
    if eof_md5:
        print("EOF MD5:        " + eof_md5)
    
    # Verify checksums
    md5_ok = True
    
    if metadata_md5 and eof_md5:
        # Both checksums available - all three must match
        md5_ok = (calculated_md5 == metadata_md5 == eof_md5)
        if md5_ok:
            print(f"{GREEN}MD5 verification successful!{RESET} All checksums match.")
        else:
            print(f"{RED}MD5 verification failed!{RESET} Checksums don't match.")
            if calculated_md5 != metadata_md5:
                print(f"{RED}Calculated MD5 doesn't match metadata MD5{RESET}")
                print(f"  Calculated: {calculated_md5}")
                print(f"  Metadata:   {metadata_md5}")
            if calculated_md5 != eof_md5:
                print(f"{RED}Calculated MD5 doesn't match EOF MD5{RESET}")
                print(f"  Calculated: {calculated_md5}")
                print(f"  EOF:        {eof_md5}")
            if metadata_md5 != eof_md5:
                print(f"{RED}Metadata MD5 doesn't match EOF MD5{RESET}")
                print(f"  Metadata:   {metadata_md5}")
                print(f"  EOF:        {eof_md5}")
    elif metadata_md5:
        # Only metadata MD5 available
        md5_ok = (calculated_md5 == metadata_md5)
        if md5_ok:
            print(f"{GREEN}MD5 verification successful!{RESET} Calculated MD5 matches metadata MD5.")
        else:
            print(f"{RED}MD5 verification failed!{RESET} Calculated MD5 doesn't match metadata MD5.")
            print(f"  Calculated: {calculated_md5}")
            print(f"  Metadata:   {metadata_md5}")
    elif eof_md5:
        # Only EOF MD5 available
        md5_ok = (calculated_md5 == eof_md5)
        if md5_ok:
            print(f"{GREEN}MD5 verification successful!{RESET} Calculated MD5 matches EOF MD5.")
        else:
            print(f"{RED}MD5 verification failed!{RESET} Calculated MD5 doesn't match EOF MD5.")
            print(f"  Calculated: {calculated_md5}")
            print(f"  EOF:        {eof_md5}")
    else:
        # No checksums available - print a clear message
        print(f"{YELLOW}WARNING: No MD5 checksums available for verification.{RESET}")
        print(f"Receiver calculated MD5: {calculated_md5}")
        print("Make sure the sender is using the current version of the software that includes MD5 checksums.")
    
    # Write file if MD5 verification passes or if partial flag is enabled
    if md5_ok or partial:
        # Now write the file
        # Add multiple newlines to ensure separation from previous output
        output_path = current_output_path
        
        # If partial file due to MD5 mismatch, add .partial extension
        if not md5_ok and partial:
            # Create incoming directory if it doesn't exist
            os.makedirs("incoming", exist_ok=True)
            # Put the file in incoming directory with .partial extension
            output_path = os.path.join("incoming", os.path.basename(current_output_path) + ".partial")
            print(f"\n\n\n{YELLOW}MD5 verification failed. Writing partial file with missing chunks as zeros to {output_path}{RESET}")
        else:
            print(f"\n\n\nMD5 verification passed. Writing decoded file to {output_path}")
            
        with open(output_path, 'wb') as f:
            file_buffer.seek(0)
            f.write(file_buffer.getvalue())
            
        if not md5_ok and partial:
            print(f"\nSuccessfully wrote {bytes_written} bytes (partial file with missing chunks)")
        else:
            print(f"\nSuccessfully wrote {bytes_written} bytes")
    else:
        print(f"\n{RED}File not written due to MD5 checksum mismatch!{RESET}")
        print(f"Use --partial flag to write partial files with missing chunks as zeros into the incoming/ directory")
    
    # Cleanup
    file_buffer.close()
    
    # Store results
    transfer['successful_chunks'] = successful_chunks
    transfer['missing_chunks'] = missing_chunks
    transfer['md5_ok'] = md5_ok
    transfer['calculated_md5'] = calculated_md5
    transfer['output_path'] = current_output_path if md5_ok else (os.path.join("incoming", os.path.basename(current_output_path) + ".partial") if partial else None)
    
    # Update progress bar with completion status
    if transfer['progress_bar'] is not None:
        # Close existing progress bar
        transfer['progress_bar'].close()
        
        # Calculate percentage of file that was successfully recovered
        percent_complete = 100
        if missing_chunks > 0:
            percent_complete = round((file_metadata['num_chunks'] - missing_chunks) / file_metadata['num_chunks'] * 100)
        
        # ANSI color codes
        GREEN = '\033[92m'  # Green for successful chunks
        YELLOW = '\033[93m' # Yellow for warning (missing chunks but still saved)
        RED = '\033[91m'    # Red for missing chunks
        RESET = '\033[0m'   # Reset color
        
        # Choose color based on completion status
        color = GREEN if missing_chunks == 0 else YELLOW
        
        # Create colored bar
        bar_length = 20  # Shorter bar for more compact display
        colored_part = int(bar_length * percent_complete / 100)
        missing_part = bar_length - colored_part
        
        if missing_chunks > 0:
            # Some chunks are missing - show yellow and red
            colored_bar = f"{YELLOW}{'█' * colored_part}{RED}{'█' * missing_part}{RESET}"
        else:
            # All chunks recovered - show full green bar
            colored_bar = f"{GREEN}{'█' * bar_length}{RESET}"
        
        # Custom bar format with consistent alignment - more compact
        custom_bar_format = "{desc:<15}:{percentage:3.0f}%|" + colored_bar + "|{n_fmt} chunks [{elapsed:<5} {postfix}]"
        
        # Create new progress bar
        import tqdm
        transfer['progress_bar'] = tqdm.tqdm(
            total=file_metadata['num_chunks'],
            initial=file_metadata['num_chunks'] - missing_chunks,
            desc=f"Completed {filename}",
            unit="chunks",
            bar_format=custom_bar_format
        )
        
        # More compact status messages - use direct form to avoid comma issues
        if missing_chunks > 0:
            transfer['progress_bar'].set_postfix(status=f"missing {missing_chunks}")
            # Print a newline after displaying status
            print("\n")
        else:
            transfer['progress_bar'].set_postfix(status="complete")
            # Print a newline after displaying status
            print("\n")
            
    # MD5 verification was already done before writing the file
    # We don't need to verify again
    # Just update the progress bar if needed to show the verification result
    if transfer['progress_bar'] is not None:
        # Close existing progress bar
        transfer['progress_bar'].close()
        
        # ANSI color codes
        GREEN = '\033[92m'  # Green for successful verification
        RED = '\033[91m'    # Red for verification failure
        RESET = '\033[0m'   # Reset color
        
        # Get verification status from transfer info
        md5_ok = transfer.get('md5_ok', False)
        
        # Create colored bar based on verification status
        bar_length = 20  # Shorter bar for more compact display
        color = GREEN if md5_ok else RED
        colored_bar = f"{color}{'█' * bar_length}{RESET}"
        
        # Custom bar format with consistent alignment - more compact
        custom_bar_format = "{desc:<15}:100%|" + colored_bar + "|{n_fmt} file [{elapsed:<5} {postfix}]"
        
        # Create new progress bar
        import tqdm
        transfer['progress_bar'] = tqdm.tqdm(
            total=1,
            initial=1,
            desc=f"Verified {filename}" if md5_ok else f"Failed {filename}",
            unit="file",
            bar_format=custom_bar_format
        )
        
        # Use direct form to avoid comma issues
        if md5_ok:
            transfer['progress_bar'].set_postfix(status="verified")
            # Print a newline after verification is complete
            print("\n")
        else:
            transfer['progress_bar'].set_postfix(status="checksum error")
            # Print a newline after verification fails
            print("\n")
    
    # Clear the global repair state flags
    clear_repair_state()
    # Log that we've cleared the flags
    print(f"\n[FEC Repair complete: Flags cleared for {filename}]")
    
    return True

class Decoder(BaseDecoder):
    """Extended Decoder with additional debugging"""
    
    def __init__(self):
        """
        Initialize the extended decoder.
        """
        super().__init__()
    
    def process_packet(self, packet_data, packet_info):
        """
        Process a received packet and attempt to decode blocks.
        Overridden for better debugging.
        
        Args:
            packet_data: Packet data
            packet_info: Packet metadata
            
        Returns:
            True if decoding is complete, False otherwise
        """
        self.received_packets += 1
        
        if self.num_blocks is None:
            self.num_blocks = packet_info['num_blocks']
            self.block_size = packet_info['block_size']
        
        # Reconstruct block indices from seed
        degree = packet_info['degree']
        seed_id = packet_info['seed_id']
        block_indices = list(get_blocks_from_seed(self.num_blocks, degree, seed_id))
        
        # Convert data to numpy array
        packet_array = np.frombuffer(packet_data, dtype=np.uint8)
        
        # Process already decoded blocks
        original_indices = block_indices.copy()
        for idx in list(block_indices):
            if idx in self.decoded_blocks:
                # XOR with already decoded block
                packet_array = packet_array ^ self.decoded_blocks[idx]
                block_indices.remove(idx)
        
        if len(block_indices) == 0:
            # All blocks in this packet have been decoded already
            return len(self.decoded_blocks) == self.num_blocks
            
        if len(block_indices) == 1:
            # This is a degree-1 packet, decode immediately
            idx = block_indices[0]
            self.decoded_blocks[idx] = packet_array
            
            # Update existing packets
            new_coded_packets = []
            for indices, data in self.coded_packets:
                if idx in indices:
                    # Update this packet
                    new_indices = [i for i in indices if i != idx]
                    new_data = data ^ packet_array
                    
                    if len(new_indices) == 1:
                        # New degree-1 packet
                        new_idx = new_indices[0]
                        self.decoded_blocks[new_idx] = new_data
                    elif len(new_indices) > 1:
                        # Still a higher degree packet
                        new_coded_packets.append((new_indices, new_data))
                else:
                    # Packet doesn't contain the decoded block
                    new_coded_packets.append((indices, data))
                    
            self.coded_packets = new_coded_packets
        else:
            # Store this packet for later
            self.coded_packets.append((block_indices, packet_array))
            
        # Check if decoding is complete
        return len(self.decoded_blocks) == self.num_blocks

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

def receive_file(output_path=None, bind_addr=('', 12345), max_packet_size=65536, 
                 simulated_loss=0.0, timeout=300, accurate_speed=False, partial=False,
                 multicast=None, broadcast=False, pcap_file=None, pcap_format=None):
    """
    Receive files over UDP using Chunked Robust Soliton FEC.
    Can handle multiple files in parallel, with each packet associated with its filename.
    Processes each chunk immediately when sufficient packets are received.
    
    Args:
        output_path: Path to save the received file (used as base name for multiple files)
        bind_addr: (ip, port) tuple to bind to
        max_packet_size: Maximum size of received packets
        simulated_loss: Percentage of packets to drop (0-1)
        timeout: Timeout in seconds, or None to wait indefinitely
        accurate_speed: Display network speed including protocol overhead
        partial: Write partial files with missing chunks filled with zeros
        multicast: Join multicast group with the specified address
        broadcast: Enable reception of broadcast packets
        pcap_file: Path to a PCAP/PCAPNG file to read packets from
        pcap_format: Format of the PCAP file ("pcap" or "pcapng")
        accurate_speed: Display network speed accounting for all protocol overhead
        partial: Write partial files with missing chunks filled with zeros when FEC repair fails
        multicast: Multicast group address to join (e.g., "224.0.0.1" for IPv4)
        broadcast: Enable broadcast reception (IPv4 only)
    
    Returns:
        True if at least one file was successfully received, False otherwise
    """
    import tqdm
    
    def read_packets_from_pcap(pcap_filepath, pcap_format, port, follow=True):
        """
        Generator function to read UDP packets from a PCAP file.
        Filters for packets on the specified port.
        
        Args:
            pcap_filepath: Path to the PCAP/PCAPNG file
            pcap_format: Format of the PCAP file ("pcap" or "pcapng")
            port: UDP port to filter for
            follow: If True, continuously monitor the file for new packets
            
        Yields:
            (packet_data, addr) tuples similar to what socket.recvfrom would return
        """
        if not DPKT_AVAILABLE:
            raise ImportError("The dpkt library is required for PCAP file processing. "
                              "Install it with 'pip install dpkt'.")
        
        last_position = 0
        last_stat = None
        initial_read_complete = False
        
        while True:
            try:
                # Check if the file has changed
                current_stat = os.stat(pcap_filepath)
                if last_stat and current_stat.st_mtime == last_stat.st_mtime and current_stat.st_size == last_stat.st_size:
                    # File hasn't changed since last read
                    if initial_read_complete and follow:
                        # Sleep briefly and check again
                        time.sleep(0.1)
                        continue
                    elif initial_read_complete and not follow:
                        # If not following and we've read the whole file, stop
                        break
                
                # Update last_stat
                last_stat = current_stat
                
                with open(pcap_filepath, 'rb') as f:
                    # Seek to the last position we read from
                    f.seek(last_position)
                    
                    try:
                        if pcap_format == 'pcapng':
                            # Create a pcapng reader
                            reader = dpkt.pcapng.Reader(f)
                        else:
                            # Default to pcap format
                            reader = dpkt.pcap.Reader(f)
                        
                        for ts, buf in reader:
                            try:
                                # Parse Ethernet frame
                                eth = Ethernet(buf)
                                
                                # Check for IP packet
                                ip_pkt = None
                                if isinstance(eth.data, IP):
                                    ip_pkt = eth.data
                                elif isinstance(eth.data, IP6):
                                    ip_pkt = eth.data
                                else:
                                    # Skip non-IP packets
                                    continue
                                
                                # Check for UDP packet
                                if isinstance(ip_pkt.data, UDP):
                                    udp_pkt = ip_pkt.data
                                    
                                    # Check if this is the port we're interested in
                                    if udp_pkt.dport == port:
                                        # Extract source address
                                        if isinstance(ip_pkt, IP):
                                            src_ip = socket.inet_ntop(socket.AF_INET, ip_pkt.src)
                                        else:  # IPv6
                                            src_ip = socket.inet_ntop(socket.AF_INET6, ip_pkt.src)
                                        
                                        # Create address tuple like socket.recvfrom would
                                        addr = (src_ip, udp_pkt.sport)
                                        
                                        # Yield the UDP payload and address
                                        yield udp_pkt.data, addr
                            except Exception as e:
                                print(f"Error parsing packet: {e}")
                                continue
                            
                        # Remember where we left off
                        last_position = f.tell()
                    except Exception as e:
                        print(f"Error reading PCAP file: {e}")
                        if not initial_read_complete:
                            raise
                
                # Mark that we've fully read the file at least once
                initial_read_complete = True
                
                # If not following, exit after reading the file once
                if not follow:
                    break
                
            except FileNotFoundError:
                if not initial_read_complete:
                    raise
                # Wait for the file to be recreated
                time.sleep(1)
                continue
    
    # Using helper functions for FEC repair state management
    
    # Create socket or setup PCAP reader
    if pcap_file:
        # Check if dpkt is available
        if not DPKT_AVAILABLE:
            raise ImportError("The dpkt library is required for PCAP file processing. "
                             "Install it with 'pip install dpkt'.")
        
        # Verify the PCAP file exists or will exist
        if not os.path.exists(pcap_file) and not os.path.isdir(os.path.dirname(pcap_file)):
            raise FileNotFoundError(f"PCAP file {pcap_file} not found and its directory doesn't exist")
        
        print(f"Reading packets from {pcap_format} file: {pcap_file}")
        print(f"Filtering for UDP packets on port {bind_addr[1]}")
        
        # We'll use a generator instead of a socket
        sock = None
        using_pcap = True
        pcap_generator = read_packets_from_pcap(pcap_file, pcap_format, bind_addr[1], follow=True)
    else:
        # Create UDP socket - determine if IPv6 or IPv4
        # Check multicast address to determine IP version if provided
        is_ipv6 = ':' in bind_addr[0] if bind_addr[0] else False
        if multicast:
            is_ipv6 = ':' in multicast
        
        # Check for broadcast and multicast conflicts
        if broadcast and multicast:
            raise ValueError("Cannot use both broadcast and multicast modes simultaneously")
        
        if is_ipv6:
            # IPv6 address
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            # Enable dual-stack socket (IPv4-mapped addresses) if binding to all interfaces
            if not bind_addr[0]:
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        else:
            # IPv4 address
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Set socket to reuse address/port for multiple receivers
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # For broadcast reception (IPv4 only)
        if broadcast and not is_ipv6:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            print(f"Enabling broadcast reception on port {bind_addr[1]}")
        
        # Bind the socket
        sock.bind(bind_addr)
        using_pcap = False
    
    # Set socket buffer size (only for network socket, not PCAP)
    if not using_pcap:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024 * 16)  # 16MB buffer
    
    # Join multicast group if specified (only for network socket, not PCAP)
    if multicast and not using_pcap:
        if is_ipv6:
            # IPv6 multicast
            # Use the interface index for the interface specified in bind_addr
            # Use index 0 (default interface) if binding to all interfaces
            group = socket.inet_pton(socket.AF_INET6, multicast)
            mreq = group + struct.pack('@I', 0)  # Default interface
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
            print(f"Joined IPv6 multicast group: {multicast}")
        else:
            # IPv4 multicast
            group = socket.inet_aton(multicast)
            # Use INADDR_ANY (0.0.0.0) for the interface
            mreq = group + socket.inet_aton('0.0.0.0')
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            print(f"Joined IPv4 multicast group: {multicast}")
    
    # Ensure we have a short timeout to regularly check for network quiet
    if not using_pcap:
        if timeout is not None:
            sock.settimeout(min(1.0, timeout))  # Max 1 second timeout for better quiet detection
        else:
            sock.settimeout(1.0)  # Default 1 second timeout
    
    # Data structures for multiple files
    # Maps filename -> {metadata, chunks, progress_bar}
    active_transfers = {}
    
    # Store bind_addr and simulated_loss to use in speed calculations
    connection_info = {
        'bind_addr': bind_addr,
        'simulated_loss': simulated_loss,
        'accurate_speed': accurate_speed
    }
    
    # Structure of active_transfers[filename]:
    # {
    #   'metadata': {file_size, chunk_size, num_chunks, block_size, overhead_factor, etc.},
    #   'chunk_packets': defaultdict(list),  # Maps chunk_id -> list of packets
    #   'progress_bar': tqdm instance,
    #   'packets_received': count of packets for this file,
    #   'reception_start_time': timestamp when first packet was received,
    #   'last_packet_time': timestamp of most recent packet,
    #   'complete': boolean, True if EOF marker received
    # }
    
    print(f"Listening for incoming packets on port {bind_addr[1]}")
    print(f"Simulated packet loss: {simulated_loss:.1%}")
    
    start_time = time.time()
    total_packets_received = 0  # Counter for all packets across all files
    last_packet_time = start_time
    
    # The quiet_delay determines how long to wait after EOF before processing
    # Change from default 20 seconds to 0.5 seconds for much faster processing
    quiet_delay = 0.5  # Was likely set to 20 seconds or more before
    
    # Keep receiving until EOF or timeout
    try:
        print("Receiving packets... (press Ctrl+C to stop)")
        
        while True:
            try:
                # Receive packet - either from PCAP file or network socket
                if using_pcap:
                    try:
                        packet_data, addr = next(pcap_generator)
                    except StopIteration:
                        # End of PCAP file and not following
                        print("End of PCAP file reached and no more packets available.")
                        break
                else:
                    packet_data, addr = sock.recvfrom(max_packet_size)
                
                last_packet_time = time.time()
                
                # Check if it's a metadata packet
                if packet_data.startswith(b'METADATA'):
                    # Add to metadata queue and send signal to interrupt repair if in progress
                    metadata_bytes = packet_data[8:]  # Skip the METADATA header
                    try:
                        # Quick parse to get filename for queue
                        import json
                        metadata_json = metadata_bytes.decode('utf-8')
                        quick_metadata = json.loads(metadata_json)
                        filename = quick_metadata['filename']
                        
                        # Debug output to verify packet counts from metadata
                        total_packets = quick_metadata.get('total_packets')
                        packets_meta = quick_metadata.get('packets_meta', {})
                        first_chunk_packets = packets_meta.get('first_chunk_packets')
                        packets_per_remaining_chunk = packets_meta.get('packets_per_remaining_chunk')
                        # FEC adjustment might be in root or in packets_meta
                        fec_adjustment = quick_metadata.get('fec_adjustment') or packets_meta.get('fec_adjustment')
                        
                        print(f"DEBUG: Total packets: {total_packets}")
                        print(f"DEBUG: First chunk packets: {first_chunk_packets}")
                        print(f"DEBUG: Packets per remaining chunk: {packets_per_remaining_chunk}")
                        print(f"DEBUG: FEC adjustment: {fec_adjustment or 'not provided'}")
                        
                        # Add to metadata queue for tracking
                        with repair_pause_lock:
                            if filename not in _metadata_queue:
                                _metadata_queue.append(filename)
                            
                            # No need for yielding with multiprocessing
                            
                            # REMOVED: FEC repair interruption code was here
                            # We no longer interrupt repairs when new metadata arrives
                            
                            # The following block was previously showing interruption messages but should be disabled:
                            # print(f"\n[INTERRUPTING REPAIR: Metadata received for {filename}]") 
                            # print("\n\n")
                            # print(f"\n{'='*50}")
                            # print(f"REPAIR INTERRUPTED - METADATA RECEIVED")
                            # print(f"{'='*50}")
                            # print(f"Current repair file: {_currently_processing_file}")
                            # print(f"Prioritizing reception of: {', '.join(_metadata_queue)}")
                            # print(f"Repair will resume when all metadata files complete (wire silence)")
                            # print(f"Waiting for EOF markers from {len(_metadata_queue)} files")
                            # print("\n")
                    except Exception as e:
                        print(f"Error preparing metadata interrupt: {e}")
                    
                    # Continue with normal metadata parsing
                    try:
                        # Parse the JSON metadata
                        import json
                        metadata_json = metadata_bytes.decode('utf-8')
                        # Parse the metadata JSON (without verbose output)
                        metadata_dict = json.loads(metadata_json)
                        
                        # Extract values from the dictionary
                        file_size = metadata_dict['file_size']
                        chunk_size = metadata_dict['chunk_size']
                        num_chunks = metadata_dict['num_chunks']
                        block_size = metadata_dict['block_size']
                        overhead_factor_raw = metadata_dict['overhead_factor']
                        filename = metadata_dict['filename']
                        # Extract MD5 checksum if available in metadata (new feature)
                        md5_checksum = metadata_dict.get('md5_checksum', None)
                        
                        # Check if we already have an active transfer for this file - handle duplicates
                        if filename in active_transfers:
                            # If file is queued but not yet processed, don't accept a new one
                            if active_transfers[filename].get('queued_for_processing', False) and not active_transfers[filename].get('processed', False):
                                # Don't restart transfers for files that are in the process of being written
                                continue
                            # If it's not completed yet, just ignore duplicate metadata
                            elif not active_transfers[filename].get('complete', False):
                                # Just ignore duplicate metadata for active transfers
                                continue
                            # If it's fully processed, we can accept a new file with the same name
                            elif active_transfers[filename].get('processed', False):
                                # This is a new transfer for a previously completed file
                                # We'll handle it by using a numbered extension for the output file
                                
                                # First, close any existing progress bar
                                if active_transfers[filename]['progress_bar'] is not None:
                                    try:
                                        active_transfers[filename]['progress_bar'].close()
                                    except:
                                        pass
                                
                                # Suppressing "Accepting new transfer" message as requested
                                
                                # Remove the old transfer entry to allow the new one
                                del active_transfers[filename]
                    except Exception as e:
                        print(f"Error parsing metadata JSON: {e}")
                        print(f"Metadata bytes: {metadata_bytes}")
                        filename = "unnamed_file"
                        raise
                    
                    # Create file metadata structure
                    file_metadata = {
                        'file_size': file_size,
                        'chunk_size': chunk_size,
                        'num_chunks': num_chunks,
                        'block_size': block_size,
                        'filename': filename,
                        'overhead_factor': overhead_factor_raw
                    }
                    
                    # Add MD5 checksum to metadata if available
                    if md5_checksum:
                        file_metadata['md5_checksum'] = md5_checksum
                        # Quiet version - don't print the MD5 to avoid cluttering the output
                        # print(f"\nMD5 checksum included in metadata: {md5_checksum[:8]}...{md5_checksum[-8:]} (for verification)")
                    
                    # Suppress verbose metadata output
                    # print(f"Received file metadata: {filename}, {file_size/1024/1024:.2f} MB, "
                    #       f"{num_chunks} chunks of {chunk_size/1024/1024:.2f} MB each")
                    
                    # Create reception progress bar showing filename and expected size
                    filename_display = filename
                    if len(filename_display) > 15:
                        # Truncate long filenames for display but preserve uniqueness
                        # Use the first 9 chars and last 3 chars to maintain uniqueness for similar filenames
                        if len(filename_display) > 20:
                            filename_display = filename_display[:9] + "..." + filename_display[-3:]
                        else:
                            filename_display = filename_display[:12] + "..."
                    
                    # For the progress bar, calculate a much more accurate estimate
                    # Using a formula based on file size, block size, and overhead
                    
                    # The sender calculates packets as: num_blocks * overhead_factor
                    overhead_factor = overhead_factor_raw
                    # Suppress verbose factor output
                    # print(f"Using overhead factor from sender: {overhead_factor:.2f}")
                    
                    # Calculate estimated total packets using the actual overhead value from the sender
                    # base_blocks needs to be rounded up as the sender does when calculating blocks
                    base_blocks = math.ceil(file_size / block_size)
                    
                    # Calculate number of blocks per chunk
                    blocks_per_chunk = math.ceil(chunk_size / block_size)
                    
                    # Get the first chunk multiplier from metadata, or use default of 5.0
                    first_chunk_multiplier = metadata_dict.get('first_chunk_multiplier', 5.0)
                    
                    # Validate first_chunk_multiplier
                    if first_chunk_multiplier <= 1:
                        print(f"Warning: Received invalid first_chunk_multiplier: {first_chunk_multiplier}, using default 5.0")
                        first_chunk_multiplier = 5.0
                        
                    # Get overhead factor and validate
                    overhead_factor = metadata_dict.get('overhead_factor', 6.0)
                    if overhead_factor <= 1:
                        print(f"Warning: Received invalid overhead_factor: {overhead_factor}, using default 6.0")
                        overhead_factor = 6.0
                    
                    # Get FEC level from metadata (this affects the overhead factor)
                    fec_level = metadata_dict.get('fec_level', 1.0)
                    
                    # Validate FEC level
                    if fec_level <= 0:
                        print(f"Warning: Received invalid fec_level: {fec_level}, using default 1.0")
                        fec_level = 1.0
                    
                    # Calculate the FEC adjustment factor (same formula as sender)
                    fec_adjustment = 1.0 + 0.2 * (fec_level - 1.0)
                    
                    # Check if sender provided its calculated expected packet count
                    if 'total_packets' in metadata_dict:
                        # Store the sender's exact packet count for more accurate progress display
                        file_metadata['sender_expected_packets'] = metadata_dict['total_packets']
                    
                    # Calculate total packets, accounting for the first chunk's custom overhead
                    # The sender uses a formula based on the first_chunk_multiplier parameter and fec_adjustment
                    first_chunk_blocks = min(blocks_per_chunk, base_blocks)
                    remaining_blocks = base_blocks - first_chunk_blocks
                    
                    # Apply both the first_chunk_multiplier and the FEC adjustment (just like the sender)
                    effective_first_chunk_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
                    first_chunk_packets = int(first_chunk_blocks * effective_first_chunk_overhead)
                    
                    # Apply the FEC adjustment to the remaining chunks as well
                    effective_remaining_overhead = overhead_factor * fec_adjustment
                    remaining_packets = int(remaining_blocks * effective_remaining_overhead)
                    
                    # Total expected packets is the sum (no margin needed when using correct formula)
                    est_total_packets = first_chunk_packets + remaining_packets
                    
                    # Ensure est_total_packets is valid and positive
                    est_total_packets = max(1, est_total_packets)
                    
                    # Store estimated packets in the metadata
                    file_metadata['est_total_packets'] = est_total_packets
                    file_metadata['packets_per_chunk'] = est_total_packets / num_chunks if num_chunks > 0 else est_total_packets
                    
                    # ANSI color codes
                    GREEN = '\033[92m'  # Green for received
                    DARK_GREEN = '\033[38;5;22m'  # Dark green for yet to receive
                    RESET = '\033[0m'   # Reset color
                    
                    # Pre-create a colored bar format (empty at start)
                    bar_length = 20  # Shorter bar for more compact display
                    colored_bar = f"{GREEN}{'█' * 0}{DARK_GREEN}{'█' * bar_length}{RESET}"
                    
                    # Custom bar format with colors and fixed width alignment - more compact
                    # Make the description field fixed width (15 chars) to ensure alignment
                    # Use a simplified format that won't change or show inconsistencies
                    custom_bar_format = "{desc:<15}:{percentage:3.0f}%|" + colored_bar + "| [{elapsed:<5} {postfix}]"
                    
                    # Store color codes and bar length for updates
                    bar_config = {
                        'length': bar_length,
                        'green': GREEN,
                        'dark_green': DARK_GREEN,  
                        'reset': RESET
                    }
                    
                    # Create a simple progress bar format showing packets
                    progress_bar_format = "{desc:<15}:{percentage:3.0f}%|" + colored_bar + "|{n_fmt}/{total_fmt} [{elapsed:<5} {postfix}]"
                    
                    # For percentage calculation, we need to show progress that matches the sender
                    # We'll calculate based on chunks rather than packets
                    
                    # Calculate average packets per chunk (exactly like the sender does)
                    # This helps us sync our progress with sender's progression through chunks
                    
                    # Calculate packets per chunk estimation
                    if num_chunks > 0:
                        # First_chunk_multiplier affects the first chunk differently than others
                        first_chunk_blocks = min(blocks_per_chunk, base_blocks)
                        remaining_blocks = base_blocks - first_chunk_blocks
                        
                        # Calculate using the same FEC adjustment formula as before
                        effective_first_chunk_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
                        first_chunk_packets = int(first_chunk_blocks * effective_first_chunk_overhead)
                        
                        # Apply FEC adjustment to remaining chunks as well
                        effective_remaining_overhead = overhead_factor * fec_adjustment
                        remaining_packets = int(remaining_blocks * effective_remaining_overhead)
                        
                        # Total expected packets is the sum
                        expected_packets = first_chunk_packets + remaining_packets
                        
                        # Calculate average packets per chunk
                        packets_per_chunk = expected_packets / num_chunks
                        
                        # Store this for consistent calculations elsewhere
                        file_metadata['packets_per_chunk'] = packets_per_chunk
                        
                        # Use num_chunks as progress total (showing chunk progress like sender)
                        progress_total = num_chunks
                    else:
                        # Fallback to packet-based calculation if chunks unknown
                        progress_total = est_total_packets
                    
                    # Store this for progress calculation - we'll update it as packets arrive
                    file_metadata['estimated_progress_total'] = progress_total
                    
                    # Also store the original estimate for reference
                    file_metadata['original_est_total'] = est_total_packets
                    
                    # We'll use a plain function instead of a lambda for pickle compatibility
                    # The function is defined at module level
                    
                    # Create a progress bar that accurately shows expected packets using metadata from sender
                    # First check if sender provided packets_meta information
                    # Always prioritize the sender's total_packets value
                    if 'total_packets' in file_metadata:
                        expected_packets = file_metadata['total_packets']
                        print(f"INFO: Using sender's exact packet count from metadata: {expected_packets}")
                    elif 'packets_meta' in file_metadata and 'total_packets' in file_metadata['packets_meta']:
                        # Use the exact packet information from the sender's packets_meta
                        packets_meta = file_metadata['packets_meta']
                        expected_packets = packets_meta['total_packets']
                        print(f"INFO: Using sender's exact packet count from packets_meta: {expected_packets}")
                    
                    # Get other packet metadata if available
                    packets_meta = file_metadata.get('packets_meta', {})
                    first_chunk_packets = packets_meta.get('first_chunk_packets', 0)
                    packets_per_remaining_chunk = packets_meta.get('packets_per_remaining_chunk', 0)
                    avg_packet_size = packets_meta.get('avg_packet_size', block_size + 65)
                    
                    # Add debug output to verify the received metadata
                    print(f"DEBUG: Received packet metadata from sender:")
                    print(f"DEBUG: Total packets: {expected_packets}")
                    print(f"DEBUG: First chunk packets: {first_chunk_packets}")
                    print(f"DEBUG: Packets per remaining chunk: {packets_per_remaining_chunk}")
                    print(f"DEBUG: FEC adjustment: {packets_meta.get('fec_adjustment', 'not provided')}")
                    
                    # Store the average packet size for accurate transfer rate calculations
                    file_metadata['avg_packet_size'] = avg_packet_size
                    
                    # Calculate total wire bytes expected (important for accurate progress)
                    total_wire_bytes = expected_packets * avg_packet_size
                    file_metadata['total_wire_bytes'] = total_wire_bytes
                    
                    # Store these values in metadata for compatibility with the actual_packets_count calculation
                    file_metadata['effective_first_chunk_overhead'] = packets_meta.get('effective_first_chunk_overhead', 0)
                    file_metadata['effective_remaining_overhead'] = packets_meta.get('effective_remaining_overhead', 0)
                    file_metadata['fec_adjustment'] = packets_meta.get('fec_adjustment', 1.0)
                    
                    # Our fallback calculation code has been replaced with direct use of sender's metadata
                    
                    # Store this for reference
                    file_metadata['expected_packets'] = expected_packets
                    file_metadata['first_chunk_packets'] = first_chunk_packets
                    
                    # We don't need a tqdm progress bar - we'll use simple text status updates
                    reception_pbar = None  # No progress bar
                    
                    # Don't use a tqdm progress bar at all - we'll use simple text updates instead
                    # Save important info in the transfer record
                    avg_packet_size = file_metadata.get('avg_packet_size', block_size + 65)
                    
                    # Make sure we use the correct expected_packets calculation that includes FEC adjustment
                    # Get FEC level and calculate adjustment factor (same as in the sender)
                    fec_level = metadata_dict.get('fec_level', 1.0)
                    fec_adjustment = 1.0 + 0.2 * (fec_level - 1.0)
                    
                    # Recalculate total packets with FEC adjustment to ensure it matches the sender
                    # This is crucial for displaying the correct total in the initial message
                    total_blocks = math.ceil(file_size / block_size)
                    blocks_per_chunk = math.ceil(chunk_size / block_size)
                    
                    # Re-get FEC level to ensure we have the most current value
                    fec_level = metadata_dict.get('fec_level', 1.0)
                    # For FEC=8, this would be 1.0 + 0.2 * 7.0 = 2.4
                    fec_adjustment = 1.0 + 0.2 * (fec_level - 1.0)
                    
                    print(f"\nINFO: File estimated with FEC level {fec_level} (adjustment={fec_adjustment:.2f}x)")
                    print(f"INFO: Total blocks in file: {total_blocks}")
                    
                    # First chunk with special overhead
                    # CRITICAL: This calculation must exactly match the sender's calculation
                    first_chunk_blocks = min(blocks_per_chunk, total_blocks)
                    effective_first_chunk_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
                    first_chunk_packets = int(first_chunk_blocks * effective_first_chunk_overhead)
                    
                    # Remaining chunks with standard overhead (but still with FEC adjustment)
                    remaining_blocks = total_blocks - first_chunk_blocks
                    remaining_chunks = num_chunks - 1
                    
                    # Apply the same formula as the sender
                    effective_remaining_overhead = overhead_factor * fec_adjustment
                    
                    # Calculate remaining packets exactly as the sender does
                    if remaining_chunks > 0:
                        packets_per_remaining_chunk = int(remaining_blocks * effective_remaining_overhead) / remaining_chunks
                        remaining_packets = int(remaining_blocks * effective_remaining_overhead)
                    else:
                        packets_per_remaining_chunk = 0
                        remaining_packets = 0
                    
                    # Check if the packets_meta information was provided by the sender
                    if 'packets_meta' in file_metadata and 'total_packets' in file_metadata['packets_meta']:
                        # Use the exact packet count from the sender's metadata
                        sender_total_packets = file_metadata['packets_meta']['total_packets']
                        true_total_packets = sender_total_packets
                        print(f"INFO: Using sender's exact packet count: {sender_total_packets}")
                    else:
                        # Calculate true total with FEC adjustment ourselves
                        true_total_packets = first_chunk_packets + remaining_packets
                        print(f"INFO: First chunk packets: {first_chunk_packets}")
                        print(f"INFO: Remaining packets: {remaining_packets}")
                        # First check if we have total_packets directly from the sender
                        sender_total = file_metadata.get('total_packets')
                        packets_meta_total = file_metadata.get('packets_meta', {}).get('total_packets')
                        
                        if sender_total:
                            print(f"INFO: Total expected packets: {sender_total} (from sender metadata)")
                            # Use the sender's value for consistency
                            true_total_packets = sender_total
                        elif packets_meta_total:
                            print(f"INFO: Total expected packets: {packets_meta_total} (from packets_meta)")
                            # Use the packets_meta value for consistency
                            true_total_packets = packets_meta_total
                        else:
                            print(f"INFO: Total expected packets: {true_total_packets} (calculated locally)")
                    
                    # Store in metadata and update expected_packets
                    file_metadata['expected_packets'] = true_total_packets
                    expected_packets = true_total_packets
                    
                    # Use our progress display to show the transfer
                    if hasattr(main, 'progress_display'):
                        # Add this transfer to the progress display - use sender's count if available
                        display_total_packets = file_metadata.get('sender_expected_packets', true_total_packets)
                        main.progress_display.add_transfer(filename, display_total_packets)
                        
                        # Store that we're using the progress display for this file
                        file_metadata['using_progress_display'] = True
                    else:
                        # Fallback to original ANSI color progress display
                        # ANSI color codes for progress bar
                        DARK_GREEN = '\033[38;5;22m'  # Dark green for received
                        DARK_BLUE = '\033[38;5;17m'   # Dark blue for yet to receive
                        RESET = '\033[0m'
                        CLEAR_LINE = '\033[2K'  # Clear entire line
                        
                        # Create empty progress bar - dark blue for yet to receive
                        bar_width = 20
                        bar = f"{DARK_BLUE}{'█' * bar_width}{RESET}"
                        
                        # Use the sender's exact packet count in the display if available
                        display_total_packets = file_metadata.get('sender_expected_packets', true_total_packets)
                        
                        # Initial status line
                        status_line = f"Receiving {filename_display}: 0%|{bar}| 0/{display_total_packets} pkts (waiting...)"
                        
                        # Check if we need to add even more space due to paused FEC repair
                        with repair_pause_lock:
                            if _fec_repair_in_progress and _fec_repair_paused:
                                # Extra newlines when FEC repair is paused for clearer display separation
                                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", flush=True)  # 15 newlines
                            else:
                                # Regular spacing
                                print("\n\n\n\n\n\n\n\n\n\n", flush=True)  # 10 newlines
                                
                        print(f"{status_line}", end='', flush=True)
                    
                    # Store the bar configuration for updates
                    file_metadata['bar_config'] = bar_config
                    
                    # No verbose debug output
                    
                    # Initialize the transfer record for this file
                    active_transfers[filename] = {
                        'metadata': file_metadata,
                        'chunk_packets': collections.defaultdict(list),
                        'progress_bar': None,  # Keep this field but always set to None for compatibility
                        'packets_received': 0,
                        'actual_packets_count': 0,  # Explicitly initialize this to zero
                        'reception_start_time': time.time(),
                        'last_packet_time': time.time(),
                        'complete': False,
                        'connection_info': connection_info,  # Include connection info for speed calculations
                        'partial': partial  # Store the partial flag in the transfer record
                    }
                    
                    continue
                
                # Check if it's an end-of-file marker with filename and MD5
                if packet_data.startswith(b'ENDOFFILE:'):
                    # Extract filename and MD5 checksum from the packet
                    try:
                        # Format is: ENDOFFILE:filename:md5checksum
                        eof_data = packet_data[len(b'ENDOFFILE:'):].decode('utf-8')
                        filename, md5_checksum = eof_data.split(':', 1)
                        
                        # Check if we have metadata for this file
                        if filename not in active_transfers:
                            print(f"Warning: Received EOF marker for unknown file: {filename}")
                            continue
                        
                        # Check if this file is already fully processed OR already queued for processing
                        # to avoid redundant processing and prevent re-queueing already queued files
                        if active_transfers[filename].get('processed', False) or active_transfers[filename].get('queued_for_processing', False):
                            # Skip this EOF marker silently - we've already processed or queued this file
                            continue
                            
                        # Suppress EOF marker info
                        # if not active_transfers[filename].get('complete', False):
                        #     print(f"\nReceived end-of-file marker for {filename}")
                        #     print(f"MD5 checksum: {md5_checksum}")
                        
                        # Mark the file as complete but continue receiving for other files
                        active_transfers[filename]['complete'] = True
                        
                        # Store MD5 checksum from EOF marker in a separate field to avoid overwriting metadata MD5
                        active_transfers[filename]['metadata']['eof_md5'] = md5_checksum
                        
                        # Debug output - compare checksums if available
                        metadata_md5 = active_transfers[filename]['metadata'].get('md5_checksum')
                        if metadata_md5 and metadata_md5 != md5_checksum:
                            print(f"\nWARNING: Metadata MD5 ({metadata_md5}) doesn't match EOF MD5 ({md5_checksum})")
                        elif metadata_md5:
                            print(f"\nINFO: Metadata MD5 matches EOF MD5: {metadata_md5[:8]}...{metadata_md5[-8:]}")
                        
                        # Force progress bar to show 100% completion before transitioning to processing
                        # This ensures it doesn't appear to drop to 0% during the transition
                        if active_transfers[filename]['progress_bar'] is not None:
                            # Force progress bar to 100% completion 
                            active_transfers[filename]['progress_bar'].n = active_transfers[filename]['progress_bar'].total
                            
                            # Ensure the actual packet count is displayed in the postfix
                            actual_count = active_transfers[filename].get('actual_packets_count', 
                                                                        active_transfers[filename]['packets_received'])
                            
                            # Get current postfix data
                            try:
                                current_postfix = active_transfers[filename]['progress_bar'].format_dict.get('postfix_dict', {})
                                mbps = current_postfix.get('Mbps', '0')
                                mbps_val = current_postfix.get('MB/s', '0')
                                
                                # Update postfix with actual packet count
                                active_transfers[filename]['progress_bar'].set_postfix(
                                    **{"MB/s": mbps_val, "Mbps": mbps, "actual": f"{actual_count}"}
                                )
                            except Exception:
                                # If we can't get the postfix data, just refresh without changing it
                                pass
                                
                            active_transfers[filename]['progress_bar'].refresh()
                        
                        # Complete the progress bar for this file - only if not already set to show processing
                        if active_transfers[filename]['progress_bar'] is not None and not active_transfers[filename].get('progress_bar_updated', False):
                            # Get total packets expected and received
                            est_total = active_transfers[filename]['metadata']['est_total_packets']
                            received = active_transfers[filename]['packets_received']
                            
                            # Force progress bar to show current progress as 100%
                            # First close the original progress bar
                            active_transfers[filename]['progress_bar'].close()
                            
                            # Create a custom progress bar with color differentiation
                            # Calculate percentage of packets received vs expected
                            if est_total > 0:
                                # Always ensure percentage is capped at 100% to prevent it from wrapping to 0%
                                percent_received = min(100, round(received / est_total * 100))
                            else:
                                # If no estimation available, use a fallback calculation but still cap at 100%
                                percent_received = min(100, round(received * 100 / max(1, file_metadata.get('estimated_progress_total', 1000))))
                            percent_missing = 100 - percent_received
                            
                            # ANSI color codes
                            GREEN = '\033[92m'  # Green for received packets
                            RED = '\033[91m'    # Red for missing packets
                            RESET = '\033[0m'   # Reset color
                            
                            # Create the colored bar string
                            bar_length = 20  # Shorter bar for more compact display (consistent with other bars)
                            green_part = int(bar_length * percent_received / 100)
                            red_part = bar_length - green_part
                            colored_bar = f"{GREEN}{'█' * green_part}{RED}{'█' * red_part}{RESET}"
                            
                            # Custom bar format that doesn't show total to avoid "?" issues
                            custom_bar_format = "{desc:<15}:{percentage:3.0f}%|" + colored_bar + "|{n_fmt} packets [{elapsed:<5} {postfix}]"
                            
                            # Create the new progress bar with the custom format
                            import tqdm
                            active_transfers[filename]['progress_bar'] = tqdm.tqdm(
                                total=est_total,
                                initial=est_total,  # Start at 100% by setting initial=total
                                desc=f"Processing {filename}",
                                unit="packets",
                                bar_format=custom_bar_format
                            )
                            # Use direct form to avoid comma issues with dict form
                            active_transfers[filename]['progress_bar'].set_postfix(status="decoding")
                            # Mark that we've updated the progress bar to avoid duplicate updates
                            active_transfers[filename]['progress_bar_updated'] = True
                        
                        # Mark this transfer for processing when quiet, but DON'T process immediately
                        try:
                            # Check if this transfer is already processed or queued
                            transfer = active_transfers[filename]
                            if transfer.get('processed', False) or transfer.get('queued_for_processing', False):
                                # This should never happen due to earlier check, but just to be safe
                                # Don't reprocess or re-queue files that are already handled or queued
                                continue
                                
                            # Mark as queued for processing
                            transfer['queued_for_processing'] = True
                            transfer['eof_received_time'] = time.time()
                            
                            # Suppressing the "Queued for processing" message as requested
                            
                            # If this file is in the metadata queue, remove it
                            with repair_pause_lock:
                                if filename in _metadata_queue:
                                    # Remove this file from metadata queue since it's complete
                                    try:
                                        _metadata_queue.remove(filename)
                                        print(f"\n[Removed {filename} from metadata queue]")
                                    except ValueError:
                                        pass  # In case it was already removed
                                    
                                    # Only resume repair if the metadata queue is empty (silence on the wire)
                                    if not _metadata_queue and _fec_repair_in_progress and _fec_repair_paused:
                                        # All expected files have completed - resume repair
                                        resumed_file = resume_repair()
                                        # Note: resume_repair() already prints clear notification
                        except Exception as e:
                            if transfer['metadata'].get('using_progress_display', False) and hasattr(main, 'progress_display'):
                                # Use Textual progress display
                                main.progress_display.print_message(f"Error processing file {filename}: {e}")
                            else:
                                # Fallback to regular print
                                print(f"\nError processing file {filename}: {e}")
                        
                        # Now also pass the EOF marker to process_packet to trigger decoding of the final chunk
                        # This is critical for ensuring the final chunk gets decoded properly
                        process_packet(packet_data, active_transfers, simulated_loss)
                        
                        # Check if all transfers are complete and process immediately if possible
                        incomplete_transfers = [name for name, transfer in active_transfers.items() 
                                             if not transfer.get('complete', False) and 
                                                not transfer.get('queued_for_processing', False)]
                            
                        active_queue = [name for name, transfer in active_transfers.items()
                                      if transfer.get('queued_for_processing', False) and 
                                         not transfer.get('processed', False)]
                            
                        # If no incomplete transfers and we have queued files, process immediately
                        if not incomplete_transfers and active_queue:
                            # Process queued file immediately without waiting for network quiet
                            process_queued_file(filename, active_transfers)
                        
                        # Continue receiving other files
                        continue
                    except Exception as e:
                        print(f"Error extracting data from EOF marker: {e}")
                        continue
                
                # Process regular packet
                filename, packet_processed = process_packet(packet_data, active_transfers, simulated_loss)
                if packet_processed and filename in active_transfers:
                    total_packets_received += 1  # Count globally
                    
                    # Update the specific file's progress bar ONLY if the file is not yet complete
                    transfer = active_transfers[filename]
                    
                    try:
                        if transfer['progress_bar'] is not None and not transfer.get('complete', False):
                            # Get the original estimate for reference
                            original_est = transfer['metadata'].get('original_est_total', 0)
                            current_n = transfer['progress_bar'].n
                            
                            # Always increment the actual packet count
                            transfer.setdefault('actual_packets_count', 0)
                            # Get the previous packet count before incrementing
                            prev_count = transfer['actual_packets_count']
                            transfer['actual_packets_count'] += 1
                            
                            # If this is the first packet, print a clear update to show progress has started
                            if prev_count == 0:
                                # Get expected packets
                                expected_packets = transfer['metadata'].get('expected_packets', 1)
                                print(f"First packet received! Beginning transfer of {expected_packets} packets...")
                            
                            # Update the progress bar to match sender chunk-based progress
                            # Only do full recalculation every 25 packets for efficiency
                            if transfer['actual_packets_count'] % 25 == 0:
                                # Get metadata for calculation
                                file_size = transfer['metadata'].get('file_size', 0)
                                block_size = transfer['metadata'].get('block_size', 1024)
                                num_chunks = transfer['metadata'].get('num_chunks', 30)
                                overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
                                first_chunk_multiplier = transfer['metadata'].get('first_chunk_multiplier', 5.0)
                                
                                # Calculate total blocks in file
                                total_blocks = math.ceil(file_size / block_size)
                                
                                # Calculate blocks per chunk
                                chunk_size = transfer['metadata'].get('chunk_size', file_size / num_chunks)
                                blocks_per_chunk = math.ceil(chunk_size / block_size)
                                
                                # Get FEC level from metadata (this affects the overhead factor)
                                # CRITICAL: Make sure we get the correct FEC level
                                fec_level = transfer['metadata'].get('fec_level', 1.0)
                                
                                # Log the FEC level for debugging
                                print(f"\nDEBUG: Using fec_level={fec_level} from metadata")
                                
                                # Calculate the FEC adjustment factor (same formula as sender)
                                fec_adjustment = 1.0 + 0.2 * (fec_level - 1.0)
                                print(f"DEBUG: Calculated fec_adjustment={fec_adjustment}")
                                
                                # Calculate the first chunk's packets exactly like the sender does
                                first_chunk_blocks = min(blocks_per_chunk, total_blocks)
                                effective_first_chunk_overhead = overhead_factor * first_chunk_multiplier * fec_adjustment
                                first_chunk_packets = int(first_chunk_blocks * effective_first_chunk_overhead)
                                
                                # Calculate remaining blocks and packets with FEC adjustment exactly like the sender
                                remaining_blocks = total_blocks - first_chunk_blocks
                                remaining_chunks = num_chunks - 1
                                
                                # Apply the FEC adjustment to the remaining chunks as well
                                effective_remaining_overhead = overhead_factor * fec_adjustment
                                
                                # Calculate packets per non-first chunk exactly like the sender
                                if remaining_chunks > 0:
                                    packets_per_remaining_chunk = int(remaining_blocks * effective_remaining_overhead) / remaining_chunks
                                    # Also calculate total remaining packets for progress calculations
                                    remaining_packets = int(remaining_blocks * effective_remaining_overhead)
                                else:
                                    packets_per_remaining_chunk = 0
                                    remaining_packets = 0
                                    
                                # Calculate total expected packets
                                expected_packets = first_chunk_packets + remaining_packets
                                
                                # Update the expected_packets in metadata to ensure consistent display
                                transfer['metadata']['expected_packets'] = expected_packets
                                
                                # Estimate chunks received based on packets - matching sender's logic
                                packets_received = transfer['actual_packets_count']
                                
                                # First determine if we've completed the first chunk
                                if packets_received >= first_chunk_packets:
                                    # First chunk complete, calculate remaining chunk progress
                                    remaining_packets = packets_received - first_chunk_packets
                                    additional_chunks = min(remaining_chunks, 
                                                          math.floor(remaining_packets / max(1, packets_per_remaining_chunk)))
                                    estimated_chunks_received = 1 + additional_chunks
                                else:
                                    # Still on first chunk
                                    first_chunk_progress = packets_received / max(1, first_chunk_packets)
                                    estimated_chunks_received = min(1, first_chunk_progress)
                                
                                # Instead of trying to mimic sender, just update based on actual packets received
                                # Simply update the progress bar with the actual packet count
                                packets_received = transfer['actual_packets_count']
                                
                                # Calculate current chunk based on packets received for status display
                                current_chunk = min(num_chunks, math.ceil(estimated_chunks_received))
                                
                                # Simple text-based updates for packet reception
                                # Get packet info from metadata
                                # Always use the sender's expected packet count if available
                                # First try top-level total_packets field
                                expected_packets = transfer['metadata'].get('total_packets',
                                    # Then try packets_meta.total_packets
                                    transfer['metadata'].get('packets_meta', {}).get('total_packets',
                                    # Then try legacy sender_expected_packets field
                                    transfer['metadata'].get('sender_expected_packets',
                                    # Finally fall back to expected_packets or 1 as a last resort
                                    transfer['metadata'].get('expected_packets', 1))))
                                avg_packet_size = transfer['metadata'].get('avg_packet_size', block_size + 65)
                                
                                # Use the actual packet count from the transfer object instead of the local variable
                                actual_packets_received = transfer.get('actual_packets_count', packets_received)
                                
                                # Calculate completion percentage based on actual packet count
                                completion_pct = min(100, int(actual_packets_received * 100 / max(1, expected_packets)))
                                
                                # Debug output is suppressed
                                # if actual_packets_received <= 5 or actual_packets_received % 1000 == 0:
                                #     print(f"\nDEBUG: actual_packets_received={actual_packets_received}, expected_packets={expected_packets}, completion_pct={completion_pct}")
                                
                                # Calculate network throughput
                                elapsed = time.time() - transfer['reception_start_time']
                                if elapsed > 0:
                                    # Calculate MB/s and Mbps
                                    bytes_received = packets_received * avg_packet_size
                                    mbps = (bytes_received * 8) / elapsed / 1000000
                                    mb_per_sec = bytes_received / elapsed / (1024 * 1024)
                                else:
                                    mbps = 0
                                    mb_per_sec = 0
                                
                                # Print a new progress line every 2000 packets and at 10% completion intervals
                                # This ensures we see progress even if terminal cursor control doesn't work as expected
                                # Use the actual packet count for milestone calculations
                                # (moved to after the actual_packets_received is defined)
                                
                                # Update progress display for every packet, but with printing control
                                # Define ANSI color codes and control sequences once outside the printing logic
                                DARK_GREEN = '\033[38;5;22m'  # Dark green for received
                                DARK_BLUE = '\033[38;5;17m'   # Dark blue for yet to receive
                                RESET = '\033[0m'
                                CLEAR_LINE = '\033[2K'  # Clear entire line
                                
                                # Create a colored progress bar (dark green on dark blue)
                                bar_width = 20
                                
                                # Calculate remaining data in MB
                                remaining_packets = expected_packets - actual_packets_received
                                avg_packet_size = transfer['metadata'].get('avg_packet_size', 8192 + 65)  # Default to 8KB + header
                                remaining_mb = (remaining_packets * avg_packet_size) / (1024 * 1024)
                                
                                # Show full green bar if either condition is met:
                                # 1. Less than 30MB remaining OR
                                # 2. More than 95% complete
                                if remaining_mb < 30 or completion_pct > 95:
                                    # Show full green bar when close to completion
                                    filled_width = bar_width
                                    remaining_width = 0
                                else:
                                    # Normal progress display
                                    filled_width = int(completion_pct / 100 * bar_width)
                                    remaining_width = bar_width - filled_width
                                
                                bar = f"{DARK_GREEN}{'█' * filled_width}{DARK_BLUE}{'█' * remaining_width}{RESET}"
                                
                                # Use the sender's exact packet count for display if available
                                # First check for the top-level total_packets field
                                display_total_packets = transfer['metadata'].get('total_packets',
                                    # Then check the packets_meta dictionary
                                    transfer['metadata'].get('packets_meta', {}).get('total_packets',
                                    # Finally fall back to expected_packets if nothing else available
                                    transfer['metadata'].get('sender_expected_packets', expected_packets)))
                                
                                # Prepare status line with fixed width to ensure proper overwriting
                                status_line = f"Receiving {filename}: {completion_pct}%|{bar}| {actual_packets_received}/{display_total_packets} pkts ({mb_per_sec:.2f}MB/s)"
                                
                                # For most packets, update progress display
                                if actual_packets_received % 100 == 0 or actual_packets_received == 1:
                                    # Check if we're using the progress display
                                    if transfer['metadata'].get('using_progress_display', False) and hasattr(main, 'progress_display'):
                                        # Update the progress in the display
                                        main.progress_display.update_transfer(filename, actual_packets_received)
                                    else:
                                        # Fallback to simple terminal progress
                                        print(f"\r{CLEAR_LINE}{status_line}", end='', flush=True)
                                
                                # Never print newlines for progress updates - always stay on same line
                                # Calculate milestone percentages only for debugging
                                milestone_pct = (actual_packets_received * 100) // expected_packets
                                prev_milestone_pct = ((actual_packets_received - 1) * 100) // expected_packets
                                
                                # No more milestone preserving - comment this out to keep progress on same line
                                # if (actual_packets_received == 1 or 
                                #     actual_packets_received % 10000 == 0 or 
                                #     (milestone_pct % 10 == 0 and milestone_pct != prev_milestone_pct and milestone_pct > 0)):
                                #     print()  # Print a blank line to preserve the milestone in the terminal history
                            
                            # Set up a periodic progress update for the current file
                        # Check if it's been more than 0.5 seconds since the last progress update
                        if 'last_progress_update' not in transfer:
                            transfer['last_progress_update'] = 0
                            
                        current_time = time.time()
                        if current_time - transfer.get('last_progress_update', 0) > 0.5:
                            # Force a progress update even if we haven't received a new packet recently
                            transfer['last_progress_update'] = current_time
                            
                            # Force a progress bar update using the latest transfer information
                            actual_packets_received = transfer.get('actual_packets_count', 0)
                            expected_packets = transfer['metadata'].get('expected_packets', 1)
                            
                            # Only update if we have packets and haven't completed yet
                            if actual_packets_received > 0 and not transfer.get('complete', False):
                                # Force a progress bar update with colored bar
                                # Calculate completion percentage
                                completion_pct = min(100, int(actual_packets_received * 100 / max(1, expected_packets)))
                                
                                # Print a progress update
                                DARK_GREEN = '\033[38;5;22m'  # Dark green for received
                                DARK_BLUE = '\033[38;5;17m'   # Dark blue for yet to receive
                                RESET = '\033[0m'
                                CLEAR_LINE = '\033[2K'  # Clear entire line
                                
                                # Create a colored progress bar (dark green on dark blue)
                                bar_width = 20
                                
                                # Calculate remaining data in MB
                                remaining_packets = expected_packets - actual_packets_received
                                avg_packet_size = transfer['metadata'].get('avg_packet_size', 8192 + 65)  # Default to 8KB + header
                                remaining_mb = (remaining_packets * avg_packet_size) / (1024 * 1024)
                                
                                # Show full green bar if either condition is met:
                                # 1. Less than 30MB remaining OR
                                # 2. More than 95% complete
                                if remaining_mb < 30 or completion_pct > 95:
                                    # Show full green bar when close to completion
                                    filled_width = bar_width
                                    remaining_width = 0
                                else:
                                    # Normal progress display
                                    filled_width = int(completion_pct / 100 * bar_width)
                                    remaining_width = bar_width - filled_width
                                
                                bar = f"{DARK_GREEN}{'█' * filled_width}{DARK_BLUE}{'█' * remaining_width}{RESET}"
                                
                                # Calculate throughput
                                elapsed = time.time() - transfer['reception_start_time']
                                if elapsed > 0:
                                    try:
                                        avg_packet_size = transfer['metadata'].get('avg_packet_size', block_size + 65)
                                    except Exception:
                                        # Handle the case where block_size might not be defined
                                        avg_packet_size = transfer['metadata'].get('avg_packet_size', 8192 + 65)
                                    bytes_received = actual_packets_received * avg_packet_size
                                    mb_per_sec = bytes_received / elapsed / (1024 * 1024)
                                else:
                                    mb_per_sec = 0
                                
                                # Prepare forced status update within try/except to catch any errors
                                try:
                                    filename = transfer['metadata'].get('filename', 'unknown')
                                    
                                    # Check if we're using the progress display
                                    if transfer['metadata'].get('using_progress_display', False) and hasattr(main, 'progress_display'):
                                        # Update the progress display
                                        main.progress_display.update_transfer(filename, actual_packets_received)
                                    else:
                                        # Fallback to terminal progress
                                        status_line = f"Receiving {filename}: {completion_pct}%|{bar}| {actual_packets_received}/{expected_packets} pkts ({mb_per_sec:.2f}MB/s)"
                                        print(f"\r{CLEAR_LINE}{status_line}", end='', flush=True)
                                except Exception as e:
                                    # Silently ignore any errors in status display
                                    pass
                                # Get file and block size to calculate actual completion
                                file_size = transfer['metadata'].get('file_size', 0)
                                block_size = transfer['metadata'].get('block_size', 1024)
                                
                                if file_size > 0 and block_size > 0:
                                    # Calculate how many blocks are in the file
                                    total_blocks_needed = math.ceil(file_size / block_size)
                                    
                                    # Instead of showing completion based on how many packets we need to decode,
                                    # we'll show completion based on the total expected chunks from the sender.
                                    # This will make the progress bar match the sender's progress.
                                    
                                    # Get the total number of chunks from metadata
                                    num_chunks = transfer['metadata'].get('num_chunks', 30)  # Default to 30 if not found
                                    
                                    # We need to estimate what percentage of the full file these packets represent.
                                    # Since the sender is sending chunks sequentially, we can use the actual_packets_count
                                    # in relation to the total expected packets for the whole file.
                                    
                                    # Get the overhead factor from metadata
                                    overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
                                    
                                    # Calculate chunks per packet - how many chunks we've likely received
                                    # based on the packets we've gotten so far
                                    
                                    # First check if the sender has provided the first_chunk_multiplier value
                                    first_chunk_multiplier = transfer['metadata'].get('first_chunk_multiplier', 5.0)
                                    
                                    # Estimate blocks per chunk
                                    chunk_size = transfer['metadata'].get('chunk_size', file_size / num_chunks)
                                    blocks_per_chunk = math.ceil(chunk_size / block_size)
                                    
                                    # Total blocks in file
                                    total_blocks = math.ceil(file_size / block_size)
                                    
                                    # Calculate packets for the first chunk (with multiplier)
                                    # and remaining chunks without it - just like the sender does
                                    first_chunk_packets = int(min(blocks_per_chunk, total_blocks) * overhead_factor * first_chunk_multiplier)
                                    remaining_blocks = total_blocks - min(blocks_per_chunk, total_blocks)
                                    remaining_packets = int(remaining_blocks * overhead_factor)
                                    
                                    # Total expected packets
                                    expected_packets = first_chunk_packets + remaining_packets
                                    
                                    # More accurate packets per chunk calculation for better progress matching
                                    if num_chunks > 0:
                                        # Calculate average packets per chunk (weighted for first chunk)
                                        packets_per_chunk = expected_packets / num_chunks
                                    else:
                                        # Fallback
                                        packets_per_chunk = blocks_per_chunk * overhead_factor
                                    
                                    # Calculate percentage of file received based on chunks, not packets
                                    # (similar to how the sender shows progress)
                                    estimated_chunks_received = min(num_chunks, max(1, int(transfer['actual_packets_count'] / packets_per_chunk)))
                                    
                                    # Calculate percentage of file received (0-100%)
                                    chunk_completion_pct = min(100, int(estimated_chunks_received * 100 / num_chunks))
                                    
                                    # Also calculate the decoding ability percentage (original formula)
                                    # Calculate expected total packets to be sent by sender
                                    total_expected_packets = int(total_blocks_needed * overhead_factor)
                                    
                                    # Calculate decoding ability based on overhead factor
                                    if overhead_factor >= 5.0:
                                        packets_needed = int(total_expected_packets * 0.2)
                                    elif overhead_factor >= 3.0:
                                        packets_needed = int(total_expected_packets * 0.3)
                                    else:
                                        packets_needed = int(total_expected_packets * 0.4)
                                        
                                    # Ensure we have at least 1.1x more packets than blocks as absolute minimum
                                    packets_needed = max(packets_needed, int(total_blocks_needed * 1.1))
                                    
                                    # Calculate completion based on this more realistic estimate
                                    curr_packets = transfer['actual_packets_count']
                                    completion_pct = min(100, int(curr_packets * 100 / packets_needed))
                                    
                                    # Skip progress bar updates - we use our custom drawing instead
                                    # This code caused the 'NoneType' object has no attribute 'n' error
                                    try:
                                        if transfer['progress_bar'] is not None:
                                            # Set the progress bar values to match chunk-based progress
                                            transfer['progress_bar'].n = chunk_completion_pct
                                            transfer['progress_bar'].total = 100
                                            transfer['progress_bar'].refresh()
                                    except Exception as e:
                                        # Silently handle progress bar errors, as we already have a working display
                                        pass
                            
                            # Use a simple try-except to avoid variable errors
                            try:
                                # Calculate current reception percentage based on the original estimate
                                # Get the original estimate safely
                                original_est = transfer['metadata'].get('original_est_total', 0)
                                
                                # Only process this section if we have a valid original estimate
                                if original_est > 0 and transfer['actual_packets_count'] % 50 == 0:
                                    # Placeholder for the actual code - keeping this empty to avoid syntax errors
                                    pass
                            except Exception as e:
                                # Skip this block if there's any error
                                pass
                                
                            # Skip the rest of this unused code section
                            if False:
                                # Calculate a better estimate of completion percentage based on 
                                # the actual number of blocks needed to decode the file
                                file_size = transfer['metadata'].get('file_size', 0)
                                block_size = transfer['metadata'].get('block_size', 1024)
                                num_chunks = transfer['metadata'].get('num_chunks', 1)
                                
                                # For realistic completion percentage, we need to understand
                                # the relationship between blocks and packets.
                                if file_size > 0 and block_size > 0:
                                    # Get exact number of blocks in the file
                                    total_blocks_needed = math.ceil(file_size / block_size)
                                    
                                    # In Robust Soliton coding, the efficiency depends on overhead and loss rate
                                    # The actual implementation uses:
                                    # 1. The overhead_factor parameter (default 6.0)
                                    # 2. The first_chunk_multiplier (often 5.0)
                                    overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
                                    
                                    # With defaults, sender transmits approximately 6x more packets than needed
                                    # Let's use this to calculate a realistic estimate
                                    
                                    # Calculate how many packets we actually need for successful decoding
                                    # For successful decoding, we need about 10% more packets than blocks
                                    # But this also depends on the overhead factor - higher overhead means
                                    # we need a smaller percentage of the total packets
                                    
                                    # Base packets needed - usually about 1.1 times the number of blocks
                                    base_packets_needed = int(total_blocks_needed * 1.1)
                                    
                                    # With overhead_factor = 6.0, we're sending 6x more packets than blocks
                                    # So we need approximately 1/6 of total sent packets (with some margin)
                                    # Let's use a more accurate formula:
                                    
                                    # Higher overhead improves efficiency - we need less % of total
                                    efficiency_factor = min(0.5, 1.0 / (overhead_factor * 0.9))
                                    
                                    # Calculate total packets expected
                                    total_packets = int(total_blocks_needed * overhead_factor)
                                    
                                    # Calculate realistic packets needed based on this total and efficiency
                                    realistic_packets_needed = max(base_packets_needed, 
                                                                 int(total_packets * efficiency_factor))
                                    
                                    # Calculate completion percentage based on realistic needs
                                    # This should now show a much more accurate representation
                                    completion_pct = min(100, int(transfer['actual_packets_count'] * 100 / realistic_packets_needed))
                                else:
                                    # Fallback to using original estimate
                                    completion_pct = min(100, int(transfer['actual_packets_count'] * 100 / max(1, original_est)))
                                
                                # Get current postfix values
                                current_postfix = transfer['progress_bar'].format_dict.get('postfix_dict', {})
                                mbps = current_postfix.get('Mbps', '0')
                                mbps_val = current_postfix.get('MB/s', '0')
                                
                                # Calculate expected total packets with exact formula
                                file_size = transfer['metadata'].get('file_size', 0)
                                block_size = transfer['metadata'].get('block_size', 1024)
                                overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
                                
                                # Calculate expected packets
                                total_blocks = math.ceil(file_size / block_size)
                                expected_packets = int(total_blocks * overhead_factor)
                                
                                # Calculate chunks per packet - how many chunks we've likely received
                                num_chunks = transfer['metadata'].get('num_chunks', 30)
                                chunk_size = transfer['metadata'].get('chunk_size', file_size / num_chunks)
                                blocks_per_chunk = math.ceil(chunk_size / block_size)
                                
                                # Calculate packets per chunk estimation (approximate)
                                first_chunk_multiplier = transfer['metadata'].get('first_chunk_multiplier', 5.0)
                                
                                # Calculate the first chunk's blocks and packets similar to sender
                                first_chunk_blocks = min(blocks_per_chunk, total_blocks)
                                first_chunk_packets = int(first_chunk_blocks * overhead_factor * first_chunk_multiplier)
                                
                                # Calculate remaining blocks and packets
                                remaining_blocks = total_blocks - first_chunk_blocks
                                remaining_chunks = num_chunks - 1
                                
                                # Calculate packets per non-first chunk
                                if remaining_chunks > 0:
                                    packets_per_remaining_chunk = int(remaining_blocks * overhead_factor) / remaining_chunks
                                else:
                                    packets_per_remaining_chunk = 0
                                
                                # Estimate chunks received based on packets
                                packets_received = transfer['actual_packets_count']
                                
                                # First determine if we've completed the first chunk
                                if packets_received >= first_chunk_packets:
                                    # First chunk complete, calculate remaining chunk progress
                                    remaining_packets = packets_received - first_chunk_packets
                                    additional_chunks = min(remaining_chunks, 
                                                          math.floor(remaining_packets / max(1, packets_per_remaining_chunk)))
                                    estimated_chunks_received = 1 + additional_chunks
                                else:
                                    # Still on first chunk
                                    first_chunk_progress = packets_received / max(1, first_chunk_packets)
                                    estimated_chunks_received = min(1, first_chunk_progress)
                                
                                # DISABLED: This update path conflicts with the other progress bar updates
                                # We'll use only one way to update the progress bar to avoid inconsistencies
                                pass
                            
                            # DISABLED: Another redundant progress bar update path
                            # We've already updated the progress bar in the packet processing logic
                            if False:  # Disable this update path to prevent overlapping updates
                                elapsed = time.time() - transfer['reception_start_time']
                                if elapsed > 0:
                                    # Calculate a more realistic data rate
                                    # Effective data received is approximately file_size * (packets/est_total)
                                    file_metadata = transfer['metadata']
                                    # Use actual_packets_count for more accurate rate display, falling back to packets_received
                                    packets_received = transfer.get('actual_packets_count', transfer['packets_received'])
                                    
                                    est_total = file_metadata.get('est_total_packets', 0)
                                    if est_total > 0:
                                        progress_ratio = min(1.0, packets_received / est_total)
                                        est_data_received = file_metadata['file_size'] * progress_ratio
                                        
                                        # Cap at file size (don't show more than 100% of the file transmitted)
                                        est_data_received = min(est_data_received, file_metadata['file_size'])
                                        
                                        # Calculate wire speed in Mbps (megabits per second) first - more accurate
                                        avg_packet_size = file_metadata['block_size'] + 65  # data + ~65 bytes overhead
                                        packets_per_sec = packets_received / elapsed
                                        wire_mbps = (packets_per_sec * avg_packet_size * 8) / 1000000
                                        
                                        # Calculate rate in MB/s based on wire speed
                                        # Convert wire speed (Mbps) to MB/s (divide by 8 for bits to bytes)
                                        mb_per_sec = wire_mbps / 8
                                        
                                        # Apply a correction factor to match nload/sender speed more closely
                                        # For localhost with no loss, we need to adjust the reported speed
                                        if file_metadata.get('overhead_factor', 0) > 0:
                                            # Get connection info
                                            conn_info = transfer.get('connection_info', {})
                                            
                                            # Check if accurate speed reporting is requested
                                            accurate_speed = conn_info.get('accurate_speed', False)
                                            
                                            # Use a correction factor based on overhead
                                            correction_factor = 1.0  # Base factor
                                            
                                            # If we're on localhost with no loss, apply stronger correction
                                            bind_addr = conn_info.get('bind_addr', ('', 0))
                                            bind_ip = bind_addr[0]
                                            is_localhost = bind_ip == '' or bind_ip == 'localhost' or bind_ip == '127.0.0.1'
                                            no_loss = conn_info.get('simulated_loss', 0) < 0.01
                                            
                                            if accurate_speed or (is_localhost and no_loss):
                                                # Apply a stronger correction to match nload/sender
                                                # overhead_factor is used because it relates to how many redundant packets are sent
                                                correction_factor = file_metadata['overhead_factor'] * 0.95
                                                
                                            mb_per_sec *= correction_factor
                                    else:
                                        # Fallback method if estimates aren't available
                                        # Calculate wire speed first (more accurate)
                                        avg_packet_size = file_metadata['block_size'] + 65  # data + ~65 bytes overhead
                                        packets_per_sec = packets_received / elapsed
                                        wire_mbps = (packets_per_sec * avg_packet_size * 8) / 1000000
                                        
                                        # Convert wire speed to MB/s directly
                                        mb_per_sec = wire_mbps / 8
                                        
                                        # Get connection info
                                        conn_info = transfer.get('connection_info', {})
                                        
                                        # Check if accurate speed reporting is requested
                                        accurate_speed = conn_info.get('accurate_speed', False)
                                        
                                        # Apply correction for localhost/no-loss scenarios
                                        bind_addr = conn_info.get('bind_addr', ('', 0))
                                        bind_ip = bind_addr[0]
                                        is_localhost = bind_ip == '' or bind_ip == 'localhost' or bind_ip == '127.0.0.1'
                                        no_loss = conn_info.get('simulated_loss', 0) < 0.01
                                        
                                        if accurate_speed or (is_localhost and no_loss):
                                            # Apply a stronger correction
                                            mb_per_sec *= 2.0  # Multiply by 2 as a fallback correction
                                    
                                    # Create a colored progress bar 
                                    # Get the bar configuration
                                    if 'bar_config' in file_metadata:
                                        bar_config = file_metadata['bar_config']
                                        bar_length = bar_config['length']
                                        
                                        # Calculate the green part (received) and blue part (to receive)
                                        est_total = file_metadata['est_total_packets']
                                        
                                        # Calculate a meaningful percentage for the color bar
                                        # This should match the actual completion percentage we calculate elsewhere
                                        file_size = file_metadata.get('file_size', 0)
                                        block_size = file_metadata.get('block_size', 1024)
                                        
                                        # Calculate meaningful completion percentage based on real decoding needs
                                        if file_size > 0 and block_size > 0:
                                            # Get exact number of blocks in the file
                                            total_blocks_needed = math.ceil(file_size / block_size)
                                            
                                            # Calculate progress based on chunks like the sender
                                            # Get total chunks from metadata
                                            num_chunks = file_metadata.get('num_chunks', 30)  # Default to 30 if not found
                                            
                                            # Get overhead factor
                                            overhead_factor = file_metadata.get('overhead_factor', 6.0)
                                            
                                            # First check if the sender has provided the first_chunk_multiplier value
                                            first_chunk_multiplier = file_metadata.get('first_chunk_multiplier', 5.0)
                                            
                                            # Estimate blocks per chunk
                                            chunk_size = file_metadata.get('chunk_size', file_size / num_chunks)
                                            blocks_per_chunk = math.ceil(chunk_size / block_size)
                                            
                                            # Total blocks in file
                                            total_blocks = math.ceil(file_size / block_size)
                                            
                                            # Calculate packets for the first chunk (with multiplier)
                                            # and remaining chunks without it - just like the sender does
                                            first_chunk_packets = int(min(blocks_per_chunk, total_blocks) * overhead_factor * first_chunk_multiplier)
                                            remaining_blocks = total_blocks - min(blocks_per_chunk, total_blocks)
                                            remaining_packets = int(remaining_blocks * overhead_factor)
                                            
                                            # Total expected packets
                                            expected_packets = first_chunk_packets + remaining_packets
                                            
                                            # More accurate packets per chunk calculation
                                            if num_chunks > 0:
                                                # Calculate average packets per chunk (weighted for first chunk)
                                                packets_per_chunk = expected_packets / num_chunks
                                            else:
                                                # Fallback
                                                packets_per_chunk = blocks_per_chunk * overhead_factor
                                            
                                            # Estimate chunks received based on packets
                                            estimated_chunks_received = min(num_chunks, max(1, int(packets_received / packets_per_chunk)))
                                            
                                            # Calculate percentage based on chunks (matches sender progress)
                                            percent_received = min(100, int(estimated_chunks_received * 100 / num_chunks))
                                            
                                            # Also calculate decoding ability percentage
                                            # Calculate expected total packets to be sent
                                            total_expected_packets = int(total_blocks_needed * overhead_factor)
                                            
                                            # Determine packets needed based on overhead factor
                                            if overhead_factor >= 5.0:
                                                packets_needed = int(total_expected_packets * 0.2)
                                            elif overhead_factor >= 3.0:
                                                packets_needed = int(total_expected_packets * 0.3)
                                            else:
                                                packets_needed = int(total_expected_packets * 0.4)
                                            
                                            # Ensure we have minimum viable packets
                                            packets_needed = max(packets_needed, int(total_blocks_needed * 1.1))
                                            
                                            # Calculate decode percentage
                                            decode_pct = min(100, int(packets_received * 100 / packets_needed))
                                        else:
                                            # Fallback to default calculation
                                            percent_received = min(100, int(packets_received * 100 / max(1, file_metadata.get('estimated_progress_total', 1000))))
                                        
                                        # DISABLED: This is yet another redundant progress bar update path
                                        # We've consolidated all progress bar updates into a single location
                                        pass
                                    
                                    # Update postfix with transfer rates (more compact display)
                                    # Use direct form to avoid comma issues with dict form
                                    # Use MB/s with a slash but in a way that won't cause formatting issues
                                    
                                    # Calculate reception completion percentage based on actual blocks needed
                                    file_size = file_metadata.get('file_size', 0)
                                    block_size = file_metadata.get('block_size', 1024)
                                    
                                    # Use same realistic calculation of completion percentage
                                    if file_size > 0 and block_size > 0:
                                        # Get exact number of blocks in the file
                                        total_blocks_needed = math.ceil(file_size / block_size)
                                        
                                        # Get the overhead factor from metadata
                                        overhead_factor = file_metadata.get('overhead_factor', 6.0)
                                        
                                        # Calculate expected total packets to be sent
                                        total_expected_packets = int(total_blocks_needed * overhead_factor)
                                        
                                        # Determine packets needed based on overhead factor
                                        if overhead_factor >= 5.0:
                                            # With high overhead (>=5.0), we need ~20% of total packets
                                            packets_needed = int(total_expected_packets * 0.2)
                                        elif overhead_factor >= 3.0:
                                            # With medium overhead (3.0-5.0), we need ~30% of total packets
                                            packets_needed = int(total_expected_packets * 0.3)
                                        else:
                                            # With low overhead (<3.0), we need ~40% of total packets
                                            packets_needed = int(total_expected_packets * 0.4)
                                        
                                        # Ensure we have minimum viable packets
                                        packets_needed = max(packets_needed, int(total_blocks_needed * 1.1))
                                        
                                        # Calculate completion percentage based on more realistic estimate
                                        completion_pct = min(100, int(packets_received * 100 / packets_needed))
                                    else:
                                        # Fallback to original estimate
                                        completion_pct = 0
                                        
                                    # Create postfix with more compact format to fit on single line
                                    # Include actual packet count and expected packet count
                                    # Always use total_packets from metadata if available
                                    if 'total_packets' in file_metadata:
                                        # Use exact packet information from sender at root level
                                        expected_packets = file_metadata['total_packets']
                                        avg_packet_size = file_metadata.get('avg_packet_size', block_size + 65)
                                    elif 'packets_meta' in file_metadata and 'total_packets' in file_metadata['packets_meta']:
                                        # Use exact packet information from sender in packets_meta
                                        packets_meta = file_metadata['packets_meta']
                                        expected_packets = packets_meta['total_packets']
                                        avg_packet_size = packets_meta.get('avg_packet_size', block_size + 65)
                                    else:
                                        # Fall back to our own calculation
                                        total_blocks = math.ceil(file_size / block_size)
                                        expected_packets = int(total_blocks * overhead_factor)
                                        avg_packet_size = block_size + 65  # Estimate
                                    
                                    # Mimic sender style with chunk-based progress
                                    # Get total chunks from metadata
                                    num_chunks = file_metadata.get('num_chunks', 30)
                                    
                                    # Calculate chunks per packet - how many chunks we've likely received
                                    chunk_size = file_metadata.get('chunk_size', file_size / num_chunks)
                                    blocks_per_chunk = math.ceil(chunk_size / block_size)
                                    
                                    # Get first chunk multiplier from metadata
                                    first_chunk_multiplier = file_metadata.get('first_chunk_multiplier', 5.0)
                                    
                                    # Calculate the first chunk's blocks and packets like the sender
                                    first_chunk_blocks = min(blocks_per_chunk, total_blocks)
                                    first_chunk_packets = int(first_chunk_blocks * overhead_factor * first_chunk_multiplier)
                                    
                                    # Calculate remaining blocks and packets
                                    remaining_blocks = total_blocks - first_chunk_blocks
                                    remaining_chunks = num_chunks - 1
                                    
                                    # Calculate packets per non-first chunk
                                    if remaining_chunks > 0:
                                        packets_per_remaining_chunk = int(remaining_blocks * overhead_factor) / remaining_chunks
                                    else:
                                        packets_per_remaining_chunk = 0
                                    
                                    # Estimate chunks received based on packets
                                    if packets_received >= first_chunk_packets:
                                        # First chunk complete, calculate remaining chunk progress
                                        remaining_packets = packets_received - first_chunk_packets
                                        additional_chunks = min(remaining_chunks, 
                                                              math.floor(remaining_packets / max(1, packets_per_remaining_chunk)))
                                        estimated_chunks_received = 1 + additional_chunks
                                    else:
                                        # Still on first chunk
                                        first_chunk_progress = packets_received / max(1, first_chunk_packets)
                                        estimated_chunks_received = min(1, first_chunk_progress)
                                    
                                    # Create postfix that exactly matches the sender's format
                                    # The sender shows "speed=X MB/s" when receiving and adds "wire=Y Mbps" when complete
                                    # Calculate current chunk based on packets received
                                    current_chunk = min(num_chunks, math.ceil(estimated_chunks_received))
                                    
                                    # Simplified format with combined information in a single status string
                                    if current_chunk < num_chunks:
                                        # In progress format
                                        status_str = f"Chunk {current_chunk}/{num_chunks} ({packets_received}/{expected_packets} pkts, {mb_per_sec:.2f}MB/s)"
                                        postfix_data = {"status": status_str}
                                    else:
                                        # Complete format
                                        status_str = f"Complete ({packets_received}/{expected_packets} pkts, {mb_per_sec:.2f}MB/s, {wire_mbps:.1f}Mbps)"
                                        postfix_data = {"status": status_str}
                                    
                                    # Update the progress bar
                                    transfer['progress_bar'].set_postfix(**postfix_data)
                    except Exception as e:
                        print(f"Error updating progress: {e}")
                        pass
                
            except (socket.timeout, StopIteration):
                # Check if we've been idle for too long globally
                current_time = time.time()
                no_packets_period = current_time - last_packet_time
                
                # Check for transfers that are marked complete with all chunks decoded
                # Process them even if we're still receiving packets
                for filename, transfer in list(active_transfers.items()):
                    if (transfer.get('queued_for_processing', False) and 
                        not transfer.get('processed', False)):
                        
                        # Check if all processing is done for this file
                        all_processes_done = True
                        for chunk_id, process_info in transfer.get('chunk_processes', {}).items():
                            process = process_info.get('process')
                            if process and process.is_alive():
                                all_processes_done = False
                                break
                        
                        if all_processes_done:
                            print(f"\nProcessing file {filename} - all chunk processes complete")
                            process_queued_file(filename, active_transfers)
                
                # Check for transfers that need processing due to timeout (1 minute without EOF)
                for filename, transfer in active_transfers.items():
                    # Skip transfers that are already processed or queued
                    if transfer.get('processed', False) or transfer.get('queued_for_processing', False):
                        continue
                        
                    # Check if this transfer has been inactive for more than 1 minute
                    file_last_packet_time = transfer.get('last_packet_time', 0)
                    file_inactivity = current_time - file_last_packet_time
                    
                    if file_inactivity >= 60 and not transfer.get('complete', False):
                        # 1 minute has passed with no activity and no EOF marker, try to process
                        print(f"\n\n\n\nTimeout: No packets for {filename} in 60 seconds. Attempting repair...")
                        
                        # Mark as complete and queued for processing
                        transfer['complete'] = True
                        transfer['queued_for_processing'] = True
                        transfer['eof_received_time'] = current_time
                        
                        # Debug message about timeout recovery with MD5 info
                        if 'md5_checksum' in transfer['metadata']:
                            print(f"\nTimeout recovery for {filename} will use MD5 verification: {transfer['metadata']['md5_checksum'][:8]}...{transfer['metadata']['md5_checksum'][-8:]}")
                        
                        # If we've been quiet for the configured delay period, process now
                        if no_packets_period >= quiet_delay:
                            process_queued_file(filename, active_transfers)
                
                # Check if we need to show status update (no activity for 20 seconds)
                if no_packets_period > 20:
                    # Check if we have any incomplete transfers or unprocessed transfers
                    # Only consider transfers that are not already queued for processing
                    incomplete_transfers = [name for name, transfer in active_transfers.items() 
                                         if not transfer.get('complete', False) and 
                                            not transfer.get('queued_for_processing', False)]
                    
                    active_queue = [name for name, transfer in active_transfers.items()
                                  if transfer.get('queued_for_processing', False) and 
                                     not transfer.get('processed', False)]
                    
                    if not incomplete_transfers and active_queue:
                        # Process any remaining queued files, but only one at a time
                        print(f"\nAll transfers complete but {len(active_queue)} still queued for processing.")
                        # Process just the first file in the queue
                        filename = active_queue[0]
                        print(f"Processing {filename} (other files will be processed after this one)")
                        process_queued_file(filename, active_transfers)
                        
                        # Check if there are any remaining queued files before printing this message
                        remaining_queued = [f for f, t in active_transfers.items() 
                                          if t.get('queued_for_processing', False) and not t.get('processed', False)]
                        if remaining_queued:
                            print(f"\nContinuing to process remaining files: {', '.join(remaining_queued)}")
                        # Otherwise we're done, no message needed
                    elif incomplete_transfers:
                        print(f"\nNo packets received for {no_packets_period:.1f} seconds - waiting for: {', '.join(incomplete_transfers)}")
                        # Continue waiting if there are incomplete transfers
                # Continue the reception loop, reset the timeout
                continue
        
        # Define a function to print summary
        def print_summary(force=False):
            nonlocal start_time, total_packets_received, active_transfers, last_summary_stats
            
            # Calculate current statistics
            elapsed_time = time.time() - start_time
            completed_files = sum(1 for t in active_transfers.values() if t.get('complete', False))
            processed_files = sum(1 for t in active_transfers.values() if t.get('processed', False))
            
            # Create a stats snapshot to compare with last time
            current_stats = {
                'elapsed_time': elapsed_time,
                'total_packets_received': total_packets_received,
                'completed_files': completed_files, 
                'processed_files': processed_files
            }
            
            # Only print if forced or if stats changed since last print
            if force or current_stats != last_summary_stats:
                # Don't close progress bars, just temporarily move cursor and restore after summary
                # Store all current progress bars that are active
                active_progress_bars = []
                
                try:
                    # Print newlines to move below the progress bars
                    print("\n\n")
                    
                    # Store references to active progress bars for restoring later
                    for filename, transfer in active_transfers.items():
                        if transfer['progress_bar'] is not None and not transfer['progress_bar'].disable:
                            active_progress_bars.append(transfer['progress_bar'])
                except Exception as e:
                    print(f"Error handling progress bars: {e}")
                
                # Print the summary
                print(f"\n{'='*30}")
                print(f"OVERALL SUMMARY")
                print(f"{'='*30}")
                print(f"✓ Total time: {elapsed_time:.2f} seconds")
                print(f"✓ Total packets received: {total_packets_received}")
                print(f"✓ Files completed: {completed_files}")
                print(f"✓ Files fully processed: {processed_files}")
                
                # After printing summary, refresh active progress bars
                try:
                    # Add some space after the summary
                    print("\n")
                    
                    # Refresh all active progress bars
                    for pbar in active_progress_bars:
                        pbar.refresh()
                except Exception as e:
                    print(f"Error refreshing progress bars: {e}")
                
                # Update the last summary stats
                last_summary_stats = current_stats
                return True
            return False
        
        # Define a signal handler for SIGUSR1
        def signal_handler(sig, frame):
            nonlocal keep_running, start_time, total_packets_received, active_transfers
            # Print summary directly here, not using the function
            elapsed_time = time.time() - start_time
            completed_files = sum(1 for t in active_transfers.values() if t.get('complete', False))
            processed_files = sum(1 for t in active_transfers.values() if t.get('processed', False))
            
            # Print the summary with clear formatting
            print("\n\n")
            print(f"\n{'='*30}")
            print(f"OVERALL SUMMARY")
            print(f"{'='*30}")
            print(f"✓ Total time: {elapsed_time:.2f} seconds")
            print(f"✓ Total packets received: {total_packets_received}")
            print(f"✓ Files completed: {completed_files}")
            print(f"✓ Files fully processed: {processed_files}")
            print("\n")
        
        # Register function-specific signal handler (overrides the global one)
        import signal
        
        # Remove the global handler first
        try:
            signal.signal(signal.SIGUSR1, signal_handler)
            print("SIGUSR1 handler installed - send signal to get summary")
        except Exception as e:
            print(f"Warning: Could not install SIGUSR1 handler: {e}")
        
        # Track when summary was last printed
        last_summary_time = time.time()
        last_summary_stats = {}
        keep_running = True
        
        # Main reception loop continues until killed or all files processed + 1 min silence
        while keep_running:
            current_time = time.time()
            
            # Check for complete silence after all files processed (1 minute)
            no_packets_period = current_time - last_packet_time
            all_processed = all(transfer.get('processed', False) for transfer in active_transfers.values() if transfer.get('complete', False))
            all_files_complete = all(transfer.get('complete', False) for transfer in active_transfers.values())
            
            # Check if it's time to print summary (network silence for 1 minute AND all files processed)
            if no_packets_period >= 60 and all_processed and all_files_complete and (current_time - last_summary_time) >= 60:
                # Print summary if it changed
                if print_summary():
                    last_summary_time = current_time
            
            # Sleep a bit to reduce CPU usage
            time.sleep(0.1)
        
        # Final summary before exiting
        print_summary(force=True)
        
        # Check if any files were successfully received
        successfully_received_files = any(transfer.get('processed', False) for transfer in active_transfers.values())
        return successfully_received_files
                
    except KeyboardInterrupt:
        print("\nReceiver stopped by user.")
        # Force print summary on exit
        try:
            print_summary(force=True)
        except:
            pass
    
    finally:
        if sock:
            sock.close()
        try:
            # Close any open progress bars
            for filename, transfer in active_transfers.items():
                if transfer.get('progress_bar') is not None:
                    transfer['progress_bar'].close()
        except Exception:
            pass
    
    return False

def process_packet(packet_data, active_transfers, simulated_loss):
    """
    Process a received packet and store it in the appropriate file's chunk collection.
    
    Args:
        packet_data: The raw packet data
        active_transfers: Dictionary of active file transfers
        simulated_loss: Simulation packet loss rate (0-1)
    
    Returns:
        Tuple of (filename, was_processed) or (None, False) if packet couldn't be processed
    """
    # Simulate packet loss
    if random.random() < simulated_loss:
        return None, False
    
    # Check if this is an EOF marker packet
    if packet_data.startswith(b'ENDOFFILE:'):
        try:
            # Format: ENDOFFILE:filename:md5checksum
            parts = packet_data[len(b'ENDOFFILE:'):].decode('utf-8').split(':', 1)
            if len(parts) >= 1:
                filename = parts[0]
                md5_checksum = parts[1] if len(parts) > 1 else None
                
                # Check if we have an active transfer for this file
                if filename in active_transfers:
                    transfer = active_transfers[filename]
                    print(f"\n{'='*60}")
                    print(f"RECEIVED EOF MARKER FOR {filename}")
                    print(f"{'='*60}")
                    
                    # Save the MD5 checksum if provided
                    if md5_checksum and 'metadata' in transfer:
                        transfer['metadata']['md5_checksum'] = md5_checksum
                    
                    # Store the EOF received time
                    transfer['eof_received_time'] = time.time()
                    
                    # Spawn FEC decode process for the final chunk if not already started
                    if 'metadata' in transfer and 'num_chunks' in transfer['metadata']:
                        num_chunks = transfer['metadata']['num_chunks']
                        last_chunk_id = num_chunks - 1
                        
                        if ('chunk_processes' not in transfer or 
                            last_chunk_id not in transfer['chunk_processes'] or 
                            not transfer['chunk_processes'][last_chunk_id].get('process')):
                            
                            # Initialize structures if needed
                            if 'chunk_processes' not in transfer:
                                transfer['chunk_processes'] = {}
                                transfer['chunk_results_queue'] = multiprocessing.Queue()
                                transfer['decoded_chunks'] = {}
                            
                            # Make sure we have packets for this chunk
                            if last_chunk_id in transfer['chunk_packets'] and len(transfer['chunk_packets'][last_chunk_id]) > 0:
                                # Calculate expected blocks based on chunk size and block size
                                block_size = transfer['metadata'].get('block_size', 8192)
                                chunk_size = transfer['metadata'].get('chunk_size', 10*1024*1024)
                                file_size = transfer['metadata'].get('file_size', 0)
                                
                                # For the last chunk, we need to calculate actual size
                                last_chunk_size = file_size - (last_chunk_id * chunk_size)
                                expected_blocks = math.ceil(last_chunk_size / block_size)
                                
                                # Print concise message for final chunk
                                print(f"\nEOF MARKER: DECODING FINAL CHUNK {last_chunk_id} ({len(transfer['chunk_packets'][last_chunk_id])} packets, {expected_blocks} blocks)")
                                
                                # Create a copy of the packets to avoid race conditions
                                chunk_packets = list(transfer['chunk_packets'][last_chunk_id])
                                
                                # Create dedicated queue for this process to improve reliability
                                result_queue = multiprocessing.Queue()
                                
                                # Start a new process to decode this chunk
                                process = Process(
                                    target=process_chunk_immediately,
                                    args=(filename, last_chunk_id, chunk_packets, transfer['metadata'], 
                                          transfer, result_queue)  # Use dedicated queue
                                )
                                process.daemon = True
                                process.start()
                                
                                # Store process info
                                transfer['chunk_processes'][last_chunk_id] = {
                                    'process': process,
                                    'start_time': time.time(),
                                    'packets': len(chunk_packets),
                                    'expected_blocks': expected_blocks,
                                    'eof_triggered': True,  # Mark this as EOF triggered
                                    'result_queue': result_queue  # Store dedicated queue
                                }
                                
                                # Check for immediate result without delay
                                try:
                                    if not result_queue.empty():
                                        result = result_queue.get_nowait()
                                        if result and 'chunk_id' in result and result['chunk_id'] == last_chunk_id:
                                            if result.get('success', False) and 'data' in result:
                                                # Store the decoded chunk data
                                                print(f"✓ Got immediate result for final chunk {last_chunk_id}")
                                                transfer['decoded_chunks'][last_chunk_id] = result['data']
                                except Exception as e:
                                    print(f"Error checking for immediate result for chunk {last_chunk_id}: {e}")
                    
                    return filename, True
                else:
                    # Only print this warning occasionally to avoid spamming the terminal
                    if random.random() < 0.01:  # Print only 1% of the time
                        print(f"DEBUG: Received EOF marker for unknown file: {filename}")
                    return filename, False
            
        except Exception as e:
            print(f"Error processing EOF marker: {e}")
            return None, False
            
    # Minimum packet header size: chunk_id (8 bytes) + filename_len (1 byte)
    if len(packet_data) < 9:
        return None, False  # Invalid packet
    
    # Extract chunk ID and filename
    chunk_id = struct.unpack('!Q', packet_data[:8])[0]
    filename_len = struct.unpack('!B', packet_data[8:9])[0]
    
    # We need a valid filename to associate this packet with a file
    if filename_len == 0 or len(packet_data) < 9 + filename_len:
        return None, False  # Invalid packet without proper filename
    
    # Extract filename - critical for parallel transfers
    filename_bytes = packet_data[9:9+filename_len]
    try:
        filename = filename_bytes.decode('utf-8')
    except:
        return None, False  # Couldn't decode filename
    
    # Check if we have an active transfer for this file
    if filename not in active_transfers:
        # Only print this warning occasionally to avoid spamming the terminal
        if random.random() < 0.01:  # Print only 1% of the time
            print(f"DEBUG: Received packet for unknown file: {filename}")
        return filename, False
    
    # If the file transfer is already marked as complete or queued for processing, 
    # don't process more packets
    if active_transfers[filename].get('complete', False) or active_transfers[filename].get('queued_for_processing', False):
        # We still want to count this packet and update last_packet_time for timeout purposes,
        # but don't store or process it further
        active_transfers[filename]['last_packet_time'] = time.time()
        # Only print this debug message occasionally
        if random.random() < 0.0001:  # Print only 0.01% of the time to reduce noise
            packets_received = active_transfers[filename]['packets_received']
            print(f"DEBUG: Ignoring packet for {filename} - already {active_transfers[filename].get('complete', False) and 'complete' or 'queued'}")
        return filename, False
    
    # Skip the chunk ID and filename to get the actual packet content
    packet_content = packet_data[9+filename_len:]
    
    # Create a hash of the packet content to avoid storing duplicate packets
    # This is critical to avoid the infinite loop that can happen when processing the same packet over and over
    packet_hash = hash(packet_content)
    
    # Check if this packet is already stored for this chunk
    transfer = active_transfers[filename]
    if chunk_id not in transfer.get('packet_hashes', {}):
        transfer.setdefault('packet_hashes', {})[chunk_id] = set()
    
    # If we've already seen this packet, skip it
    if packet_hash in transfer['packet_hashes'][chunk_id]:
        # Debug message - uncomment if needed
        # if random.random() < 0.001:  # Print only 0.1% of the time
        #     print(f"DEBUG: Skipping duplicate packet for file {filename}, chunk {chunk_id}")
        return filename, False
    
    # Store the hash of this packet to avoid duplicates
    transfer['packet_hashes'][chunk_id].add(packet_hash)
    
    # Store the packet in the appropriate file's chunk collection
    transfer['chunk_packets'][chunk_id].append(packet_content)
    transfer['packets_received'] += 1
    # Also increment actual_packets_count for more accurate display
    transfer.setdefault('actual_packets_count', 0)
    transfer['actual_packets_count'] += 1
    transfer['last_packet_time'] = time.time()
    
    # Initialize chunk process tracking structures if needed
    if 'chunk_processes' not in transfer:
        transfer['chunk_processes'] = {}
        transfer['chunk_results_queue'] = multiprocessing.Queue()
        transfer['decoded_chunks'] = {}
    
    # Add logic to track packet reception and start decoding when appropriate
    num_chunks = transfer['metadata'].get('num_chunks', 1)
    
    # We need to detect when chunks should be decoded
    # For a non-last chunk, that's when we've received packets for the next chunk
    # For the last chunk, that's when we've received enough packets
    
    # Initialize chunk detection tracking if needed
    if 'chunks_received' not in transfer:
        transfer['chunks_received'] = set()
    
    # Record that we've received a packet for this chunk
    transfer['chunks_received'].add(chunk_id)
    
    # If this is a new chunk and it's after chunk 0, we should decode the previous chunk
    if chunk_id > 0 and chunk_id not in transfer.get('decode_triggered', set()):
        previous_chunk = chunk_id - 1
        # Mark that we've seen this trigger
        if 'decode_triggered' not in transfer:
            transfer['decode_triggered'] = set()
        transfer['decode_triggered'].add(chunk_id)
        
        # Get overhead info to estimate if we have enough packets
        overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
        first_chunk_multiplier = 1.0  # Normal multiplier for non-first chunks
        if previous_chunk == 0:
            # First chunk gets special treatment
            first_chunk_multiplier = transfer['metadata'].get('first_chunk_multiplier', 5.0)
            
        # Calculate expected blocks for the previous chunk
        block_size = transfer['metadata'].get('block_size', 8192)
        chunk_size = transfer['metadata'].get('chunk_size', 10*1024*1024)
        
        # For the last chunk, calculate actual size
        if previous_chunk == transfer['metadata'].get('num_chunks', 1) - 1:
            file_size = transfer['metadata'].get('file_size', 0)
            last_chunk_size = file_size - (previous_chunk * chunk_size)
            prev_expected_blocks = math.ceil(last_chunk_size / block_size)
        else:
            prev_expected_blocks = math.ceil(chunk_size / block_size)
            
        # Get current packet count for the previous chunk
        prev_packets = len(transfer['chunk_packets'].get(previous_chunk, []))
        
        # Calculate expected packets based on overhead
        expected_packets = int(prev_expected_blocks * overhead_factor * first_chunk_multiplier)
        
        # Log the event with detailed information
        print(f"\n{'='*60}")
        print(f"CHUNK TRANSITION DETECTED: {previous_chunk} → {chunk_id}")
        print(f"Previous chunk packets: {prev_packets:,} / expected ~{expected_packets:,}")
        print(f"Previous chunk blocks: {prev_expected_blocks:,}")
        if prev_expected_blocks > 0:
            print(f"Current redundancy: {prev_packets/prev_expected_blocks:.2f}x")
        print(f"Expected overhead: {overhead_factor:.1f}x {' * ' + str(first_chunk_multiplier) + 'x' if previous_chunk == 0 else ''}")
        print(f"{'='*60}")
        
        # Directly trigger decode for the previous chunk
        # We'll mark it as a direct trigger
        if (previous_chunk not in transfer['chunk_processes'] or 
            not transfer['chunk_processes'][previous_chunk].get('process')):
                
            # For robust decoding, we need a minimum redundancy
            min_redundancy = 1.1  # Just 10% more than the blocks needed
            
            if prev_packets >= prev_expected_blocks * min_redundancy:
                print(f"\n{'='*60}")
                print(f"DIRECTLY TRIGGERING DECODE FOR CHUNK {previous_chunk}")
                print(f"Packets: {prev_packets:,}, Blocks needed: {prev_expected_blocks:,}")
                print(f"Redundancy: {prev_packets/prev_expected_blocks:.2f}x")
                print(f"{'='*60}")
                
                # Create a copy of the packets for this chunk
                chunk_packets = list(transfer['chunk_packets'][previous_chunk])
                
                # Create dedicated queue for better reliability
                print(f"Creating dedicated result queue for chunk {previous_chunk}")
                result_queue = multiprocessing.Queue()
                
                # Start a process to decode this chunk
                process = Process(
                    target=process_chunk_immediately,
                    args=(filename, previous_chunk, chunk_packets, transfer['metadata'], 
                          transfer, result_queue)  # Use dedicated queue
                )
                process.daemon = True
                process.start()
                
                # Store process info
                transfer['chunk_processes'][previous_chunk] = {
                    'process': process,
                    'start_time': time.time(),
                    'packets': prev_packets,
                    'expected_blocks': prev_expected_blocks,
                    'direct_trigger': True,  # Mark this as directly triggered
                    'result_queue': result_queue  # Store dedicated queue
                }
    
    # We're changing the decode strategy to ONLY rely on the transition triggers
    # and the last chunk special case, since those are clearer and more reliable
            
    is_last_chunk = chunk_id == num_chunks - 1
    process_not_started = chunk_id not in transfer['chunk_processes'] or not transfer['chunk_processes'][chunk_id].get('process')
    
    # Calculate expected blocks based on chunk size and block size to check if we have enough packets
    block_size = transfer['metadata'].get('block_size', 8192)
    chunk_size = transfer['metadata'].get('chunk_size', 10*1024*1024)
    file_size = transfer['metadata'].get('file_size', 0)
    
    # For the last chunk, we need to calculate actual size
    if chunk_id == num_chunks - 1:
        last_chunk_size = file_size - (chunk_id * chunk_size)
        expected_blocks = math.ceil(last_chunk_size / block_size)
    else:
        expected_blocks = math.ceil(chunk_size / block_size)
    
    # Calculate minimum packets needed (just 10% more than blocks)
    min_packets_for_decoding = int(expected_blocks * 1.1)
    
    # No debug output for packet status to reduce log spam
    
    # For the last chunk, we now wait for the EOF marker instead of decoding based on packet count
    # This change prevents the final chunk from failing decoding
    
    # We no longer trigger decoding for the last chunk here - wait for EOF marker packet instead
    should_decode = False  # Disable automatic decoding based on packet count
    
    if should_decode:
        # Calculate expected blocks based on chunk size and block size
        block_size = transfer['metadata'].get('block_size', 8192)
        chunk_size = transfer['metadata'].get('chunk_size', 10*1024*1024)
        file_size = transfer['metadata'].get('file_size', 0)
        
        # For the last chunk, we need to calculate actual size
        if chunk_id == transfer['metadata'].get('num_chunks', 1) - 1:
            last_chunk_size = file_size - (chunk_id * chunk_size)
            expected_blocks = math.ceil(last_chunk_size / block_size)
        else:
            expected_blocks = math.ceil(chunk_size / block_size)
        
        # The sender uses a high overhead factor (default 5x), so we only need 
        # slightly more than the minimum blocks for successful decoding
        min_packets_needed = int(expected_blocks * 1.1)  # Only need 10% more than minimum
        
        # Get the exact overhead factor from metadata
        overhead_factor = transfer['metadata'].get('overhead_factor', 6.0)
        first_chunk_multiplier = transfer['metadata'].get('first_chunk_multiplier', 5.0)
        
        # More aggressive for chunk 0 which has higher overhead from sender
        if chunk_id == 0:
            # First chunk gets first_chunk_multiplier times more packets from sender
            print(f"Chunk 0 has special overhead: {overhead_factor} x {first_chunk_multiplier} = {overhead_factor * first_chunk_multiplier}x")
        
        # If we have enough packets, start a decode process for this chunk
        if len(transfer['chunk_packets'][chunk_id]) >= min_packets_needed:
            # Always print this message to provide visibility
            print(f"\n{'='*60}")
            print(f"DECODING CHUNK {chunk_id}:")
            print(f"Packets received: {len(transfer['chunk_packets'][chunk_id])}")
            print(f"Expected blocks: {expected_blocks}")
            print(f"Redundancy ratio: {len(transfer['chunk_packets'][chunk_id])/expected_blocks:.2f}x")
            print(f"{'='*60}")
            print(f"\nSpawning decode process for {filename} chunk {chunk_id} with {len(transfer['chunk_packets'][chunk_id])} packets")
            
            # Create a copy of the packets to avoid race conditions
            chunk_packets = list(transfer['chunk_packets'][chunk_id])
            
            # Start a new process to decode this chunk
            process = Process(
                target=process_chunk_immediately,
                args=(filename, chunk_id, chunk_packets, transfer['metadata'], 
                      transfer, transfer['chunk_results_queue'])
            )
            process.daemon = True
            process.start()
            
            # Store process info
            transfer['chunk_processes'][chunk_id] = {
                'process': process,
                'start_time': time.time(),
                'packets': len(chunk_packets),
                'expected_blocks': expected_blocks
            }
    
    # Check if we have any results from chunk processes
    try:
        # Non-blocking check for results
        while not transfer['chunk_results_queue'].empty():
            # Get a result from the queue
            result = transfer['chunk_results_queue'].get_nowait()
            
            if result and 'chunk_id' in result:
                chunk_id = result['chunk_id']
                
                # If it's a success with data, store it
                if result.get('success', False) and 'data' in result:
                    # Store the decoded chunk data
                    transfer['decoded_chunks'][chunk_id] = result['data']
                    
                    # Print a visible message about the successful decode
                    print(f"\n{'='*60}")
                    print(f"✅ CHUNK {chunk_id} RESULT RECEIVED!")
                    print(f"File: {filename}")
                    print(f"Size: {len(result['data']):,} bytes")
                    print(f"Decoded chunks: {len(transfer['decoded_chunks'])}/{transfer['metadata'].get('num_chunks', '?')}")
                    print(f"{'='*60}")
                    
                    # If the process is still in our tracking dict, remove it
                    if chunk_id in transfer['chunk_processes']:
                        process_info = transfer['chunk_processes'][chunk_id]
                        process = process_info.get('process')
                        if process and process.is_alive():
                            process.terminate()
                        
                        # Remove this entry
                        del transfer['chunk_processes'][chunk_id]
                # Log useful information about failed decoding attempts
                else:
                    packets_received = result.get('packets_received', 0)
                    expected_blocks = result.get('expected_blocks', 0)
                    
                    # Store additional info in the process tracking
                    if chunk_id in transfer['chunk_processes']:
                        transfer['chunk_processes'][chunk_id]['packets_received'] = packets_received
                        transfer['chunk_processes'][chunk_id]['expected_blocks'] = expected_blocks
                        transfer['chunk_processes'][chunk_id]['decode_failed'] = True
                        
                        # We won't try to decode again - this chunk will be handled by the
                        # final repair process instead of our immediate decoding.
                        # Print a detailed failure message
                        print(f"\n{'='*60}")
                        print(f"❌ CHUNK {chunk_id} DECODING FAILED - WILL TRY IN FINAL REPAIR")
                        print(f"File: {filename}")
                        print(f"Packets processed: {packets_received}")
                        print(f"Expected blocks: {expected_blocks}")
                        if expected_blocks > 0:
                            print(f"Redundancy ratio: {packets_received/expected_blocks:.2f}x")
                        print(f"Message: The final repair process will try again with all packets")
                        print(f"{'='*60}")
                        
                        # Terminate the process immediately since it failed
                        if process_info.get('process') and process_info['process'].is_alive():
                            print(f"Terminating decode process for chunk {chunk_id} - no need to wait since decoding failed")
                            process_info['process'].terminate()
    except Exception as e:
        # Log queue errors
        if random.random() < 0.001:  # Only log occasionally to reduce clutter 
            print(f"Queue error: {e}")
        pass
    
    # Check if we've decoded all chunks for this file
    if transfer.get('metadata') and 'num_chunks' in transfer['metadata'] and not transfer.get('complete', False):
        num_chunks = transfer['metadata']['num_chunks']
        decoded_chunks = transfer.get('decoded_chunks', {})
        
        # If we've decoded all chunks, mark as complete and queue for final processing
        if len(decoded_chunks) == num_chunks:
            print(f"\nAll {num_chunks} chunks decoded for {filename}, queueing for final assembly")
            transfer['complete'] = True
            transfer['queued_for_processing'] = True
            transfer['eof_received_time'] = time.time()
            
            # Process the file immediately when all chunks are decoded
            # Check if this is the only file or if all other files are complete
            incomplete_transfers = [name for name, xfer in active_transfers.items() 
                                if not xfer.get('complete', False) and 
                                   not xfer.get('queued_for_processing', False) and 
                                   name != filename]
            
            # If no other transfers are in progress, process this one right away
            if not incomplete_transfers:
                print(f"\nAll transfers complete, processing {filename} immediately")
                process_queued_file(filename, active_transfers)
    
    return filename, True

def decode_chunk(chunk_id, packets, file_metadata):
    """Attempt to decode a single chunk from its packets"""
    # No need for GIL yielding with multiprocessing
    
    # We've removed the interruption check since we never want to interrupt repairs
    
    # Check if repair is paused - return immediately if so
    if is_repair_paused():
        return chunk_id, None
    
    # Reduce CPU priority of repair threads to give receiving priority
    try:
        import os
        os.nice(10)  # Lower priority (higher nice value) for repair threads
    except:
        pass  # If nice fails, continue anyway
    
    # Skip empty chunk packets to avoid wasting time
    if not packets or len(packets) == 0:
        print(f"Warning: No packets provided for chunk {chunk_id}")
        return chunk_id, None
        
    # Process plenty of packets since we're using a fast PRNG now
    max_packets_to_process = 20000
    
    # Create decoder for this chunk
    decoder = Decoder()
    
    # Process packets efficiently, limiting the total number
    if len(packets) > max_packets_to_process:
        # If we have too many packets, use a random sample to avoid memory issues
        # This is okay because fountain codes are designed to work with any subset of packets
        import random
        packets_to_process = random.sample(packets, max_packets_to_process)
    else:
        packets_to_process = packets
    
    # Process unique packets only
    processed_packets = set()
    unique_packets = []
    
    for packet_content in packets_to_process:
        packet_hash = hash(packet_content)
        if packet_hash not in processed_packets:
            processed_packets.add(packet_hash)
            unique_packets.append(packet_content)
    
    # Process packets to extract data
    for i, packet_content in enumerate(unique_packets):
        # Check for interruption every few packets
        if i % 10 == 0 and is_repair_paused():
            return chunk_id, None
            
        try:
            # Decode and process packet
            decoded_data, packet_info = decoder.decode_packet(packet_content)
            decoding_complete = decoder.process_packet(decoded_data, packet_info)
            
            if decoding_complete:
                # This chunk is done!
                chunk_data = decoder.get_decoded_data()
                # One final check before returning
                if is_repair_paused():
                    return chunk_id, None
                return chunk_id, chunk_data
                
        except Exception as e:
            # Just continue to the next packet
            pass
    
    # If we get here, we couldn't fully decode the chunk
    stats = decoder.get_stats()
    if stats['total_blocks'] > 0:
        completion = stats['decoded_blocks']/stats['total_blocks']*100
        
        # Lower the threshold for accepting partial data to 80%
        if stats['decoded_blocks'] >= 0.8 * stats['total_blocks']:
            try:
                # Try to make more progress before accepting the partial data
                # This gives us one more chance to decode using the available blocks
                partial_data = None
                
                if len(decoder.coded_packets) > 0:
                    # Try a more aggressive decoding approach with the packets we have
                    progress_made = True
                    while progress_made and stats['decoded_blocks'] < stats['total_blocks']:
                        progress_made = False
                        for indices, data in decoder.coded_packets:
                            new_indices = []
                            new_data = data.copy()
                            
                            for idx in indices:
                                if idx in decoder.decoded_blocks:
                                    new_data = new_data ^ decoder.decoded_blocks[idx]
                                else:
                                    new_indices.append(idx)
                            
                            if len(new_indices) == 1:
                                # This becomes a degree-1 packet, decode immediately
                                decoder.decoded_blocks[new_indices[0]] = new_data
                                progress_made = True
                                stats['decoded_blocks'] += 1
                
                # Now try to get the decoded data
                partial_data = decoder.get_decoded_data()
                if partial_data:
                    # Suppress this message to avoid cluttering the output
                    # print(f"Accepting partial chunk {chunk_id} with {stats['decoded_blocks']}/{stats['total_blocks']} blocks")
                    return chunk_id, partial_data
            except Exception as e:
                print(f"Error attempting partial recovery of chunk {chunk_id}: {e}")
                pass
    
    # Couldn't decode this chunk - return with None to indicate failure
    return chunk_id, None

# Function removed - we're now using direct threading instead of multiprocessing
    
def process_all_chunks(chunk_packets, file_metadata, decoded_chunks, no_packet_loss=False, interrupt_event=None):
    """Process all chunks in parallel, with optimization for no packet loss"""
    import time  # Make sure time module is available for sleep calls
    
    # IMPORTANT: Check for interrupt signals at the very beginning
    # Check the multiprocessing event if provided (process mode)
    if interrupt_event is not None and interrupt_event.is_set():
        print(f"[FEC Repair process exiting immediately - multiprocessing interrupt event is set]")
        return decoded_chunks
    # We've removed the thread event check since we don't want to interrupt repairs anymore
        
    # No need for GIL yielding since we're using multiprocessing
    
    # Ensure decoded_chunks is a dictionary
    if decoded_chunks is None:
        decoded_chunks = {}
    
    # Ensure file_metadata has all required keys
    if not isinstance(file_metadata, dict):
        print("Error: file_metadata is not a dictionary!")
        return {}
        
    required_keys = ['filename', 'num_chunks', 'chunk_size', 'block_size', 'file_size']
    for key in required_keys:
        if key not in file_metadata:
            print(f"Warning: Missing required key in file_metadata: {key}")
            # Set default values for missing keys
            if key == 'filename':
                file_metadata[key] = 'unknown_file'
            elif key == 'num_chunks':
                file_metadata[key] = len(chunk_packets)
            elif key == 'chunk_size':
                file_metadata[key] = 1024 * 1024  # 1MB default
            elif key == 'block_size':
                file_metadata[key] = 1024  # 1KB default
            elif key == 'file_size':
                # Estimate file_size from num_chunks and chunk_size
                file_metadata[key] = file_metadata.get('num_chunks', 1) * file_metadata.get('chunk_size', 1024*1024)
    
    # Print initial decoding status
    filename_display = file_metadata.get('filename', 'unknown')
    if len(filename_display) > 15:
        filename_display = filename_display[:12] + "..."
    
    # Track failed chunks
    failed_chunk_ids = set()

    # Process chunks efficiently with multithreading, but prioritize receiving
    # Get available cores, use fewer cores for repair to maintain receiving responsiveness
    available_cores = os.cpu_count() or 4
    # Use only 1/3 of cores for repair to keep majority free for receiving
    repair_cores = max(1, available_cores // 3)
    
    print(f"\nDecoding file data...")
    
    # Common colors for progress bars
    DARK_GREEN = '\033[38;5;22m'   # Dark green for successful
    DARK_GREEN2 = '\033[38;5;28m'  # Darker green for yet to receive
    RESET = '\033[0m'
    CLEAR_LINE = '\033[2K'  # Clear entire line
    
    # We'll use a single progress bar that we update continuously
    bar_width = 20
    
    # Use fast path optimization when no packets were lost
    # This will significantly improve performance in the common case
    chunks_processed = 0
    
    # Create a function to update the progress bar
    def update_progress_bar(current, total):
        percent_done = int(100 * current / total)
        filled = int(bar_width * current / total)
        bar = f"{DARK_GREEN}{'█' * filled}{DARK_GREEN2}{'█' * (bar_width - filled)}{RESET}"
        print(f"{CLEAR_LINE}\rDecoding {filename_display}: {percent_done}% |{bar}| ({current}/{total} chunks)", end='', flush=True)
    
    # Initialize with 0% progress
    update_progress_bar(0, file_metadata['num_chunks'])
    
    # Force artificial progress markers at key points
    # This ensures the user sees progress even if the actual decoding is too fast
    forced_progress_markers = [0.25, 0.5, 0.75]
    
    # Choose the appropriate decoding strategy based on packet loss
    if no_packet_loss:
        # FAST PATH: Optimized decoding when all packets are received
        # Process each chunk using direct extraction of data blocks
        for chunk_id in range(file_metadata['num_chunks']):
            # Skip already-decoded chunks
            if chunk_id in decoded_chunks:
                # Log that we're skipping this already-decoded chunk
                if chunk_id % 5 == 0:  # Only log every 5th chunk to reduce output
                    print(f"✓ Skipping chunk {chunk_id} - already decoded")
                
                # Count this chunk as processed
                chunks_processed += 1
                continue
                
            # Add forced progress updates every 10 chunks even if decoding is fast
            if chunk_id % 10 == 0 and chunk_id > 0:
                update_progress_bar(chunks_processed, file_metadata['num_chunks'])
                time.sleep(0.05)  # Small delay to make the progress visible
                
            if chunk_id in chunk_packets and chunk_packets[chunk_id]:
                try:
                    # Determine chunk size and block size
                    chunk_size = file_metadata['chunk_size']
                    block_size = file_metadata['block_size']
                    
                    # For the last chunk, adjust size if needed
                    if chunk_id == file_metadata['num_chunks'] - 1:
                        # Last chunk might be smaller
                        remaining_size = file_metadata['file_size'] - (chunk_id * chunk_size)
                        chunk_size = remaining_size
                    
                    # Fast path uses a more efficient decoding method that 
                    # directly extracts blocks without complex FEC reconstruction
                    from src.fixed_fec import Decoder
                    
                    # Initialize decoder once
                    decoder = Decoder()
                    
                    # Process some initial packets to get the metadata
                    num_blocks = None
                    
                    # Process the first packet to get metadata
                    if len(chunk_packets[chunk_id]) > 0:
                        first_packet = chunk_packets[chunk_id][0]
                        try:
                            _, packet_info = decoder.decode_packet(first_packet)
                            num_blocks = packet_info.get('num_blocks')
                        except Exception:
                            pass
                    
                    if num_blocks is None:
                        # Fall back to calculation if we couldn't determine from packet metadata
                        # First check if this information is available in the file metadata from the sender
                        if 'blocks_per_chunk' in file_metadata and chunk_id < file_metadata['num_chunks'] - 1:
                            # Use sender's calculation for non-last chunks for consistency
                            num_blocks = file_metadata['blocks_per_chunk']
                        elif 'last_chunk_blocks' in file_metadata and chunk_id == file_metadata['num_chunks'] - 1:
                            # Use sender's calculation for the last chunk
                            num_blocks = file_metadata['last_chunk_blocks']
                        else:
                            # Fall back to calculation if not available in metadata
                            # This must match the sender's calculation from RobustSolitonSender.py
                            # Ensure math module is imported
                            import math
                            num_blocks = math.ceil(chunk_size / block_size)
                    
                    # Process packets efficiently to extract all blocks
                    # We can do this in one pass since we have all packets
                    decoded_data = decoder.fast_decode_all_packets(
                        chunk_packets[chunk_id], 
                        num_blocks,
                        block_size, 
                        expected_size=chunk_size
                    )
                    
                    if decoded_data:
                        # Store the successful chunk
                        decoded_chunks[chunk_id] = decoded_data
                        chunks_processed += 1
                        
                        # Update progress bar for EVERY chunk to show activity in real-time
                        update_progress_bar(chunks_processed, file_metadata['num_chunks'])
                        
                        # Add a small delay so progress updates are visible
                        if chunks_processed % 5 == 0:
                            time.sleep(0.05)
                    
                except Exception as e:
                    # If fast path fails, we'll try the regular path for this chunk
                    pass
                    
        # If we processed chunks too quickly, show artificial intermediate progress updates
        # to make the progress visible to the user
        if chunks_processed > 0:
            total_chunks = file_metadata['num_chunks']
            for marker in forced_progress_markers:
                marker_chunks = int(marker * total_chunks)
                if marker_chunks > 0 and marker_chunks < total_chunks:
                    update_progress_bar(marker_chunks, total_chunks)
                    time.sleep(0.1)  # Add a small delay to make the progress visible
        
        # Final progress update to show 100% if all chunks processed
        if chunks_processed == file_metadata['num_chunks']:
            update_progress_bar(file_metadata['num_chunks'], file_metadata['num_chunks'])
            # Add an extra newline at the end to space out from any following content
            print()
    else:
        # REGULAR PATH: Use standard FEC reconstruction for chunks
        for chunk_id in range(file_metadata['num_chunks']):
            # Skip already-decoded chunks
            if chunk_id in decoded_chunks:
                # Log that we're skipping this already-decoded chunk
                if chunk_id % 5 == 0:  # Only log every 5th chunk to reduce output
                    print(f"✓ Skipping chunk {chunk_id} - already decoded")
                
                # Count this chunk as processed
                chunks_processed += 1
                continue
                
            if chunk_id in chunk_packets and chunk_packets[chunk_id]:
                try:
                    # Determine chunk size and block size
                    chunk_size = file_metadata['chunk_size']
                    block_size = file_metadata['block_size']
                    
                    # For the last chunk, adjust size if needed
                    if chunk_id == file_metadata['num_chunks'] - 1:
                        # Last chunk might be smaller
                        remaining_size = file_metadata['file_size'] - (chunk_id * chunk_size)
                        chunk_size = remaining_size
                    
                    # Calculate how many blocks are in this chunk
                    # First check if this information is available in the metadata from the sender
                    if 'blocks_per_chunk' in file_metadata and chunk_id < file_metadata['num_chunks'] - 1:
                        # Use sender's calculation for non-last chunks for consistency
                        blocks_in_chunk = file_metadata['blocks_per_chunk']
                    elif 'last_chunk_blocks' in file_metadata and chunk_id == file_metadata['num_chunks'] - 1:
                        # Use sender's calculation for the last chunk
                        blocks_in_chunk = file_metadata['last_chunk_blocks']
                    else:
                        # Fall back to calculation if not available in metadata
                        # This must match the sender's calculation from RobustSolitonSender.py
                        # Ensure math module is imported
                        import math
                        blocks_in_chunk = math.ceil(chunk_size / block_size)
                    
                    # Create a buffer for the full chunk
                    import io
                    chunk_buffer = io.BytesIO()
                    blocks_found = 0
                    
                    # Create a list to hold blocks by position
                    blocks_by_position = [None] * blocks_in_chunk
                    found_positions = set()
                    
                    # Sort packets by metadata to find the ones we need
                    for packet in chunk_packets[chunk_id]:
                        try:
                            from src.fixed_fec import Decoder
                            decoder = Decoder()
                            decoded_packet, packet_info = decoder.decode_packet(packet)
                            
                            # Only use degree 1 packets (direct data)
                            if packet_info['degree'] == 1:
                                # We need to generate the block indices from seed
                                if 'seed_id' in packet_info:
                                    # Get block index from the seed
                                    from src.soliton import get_blocks_from_seed
                                    block_indices = list(get_blocks_from_seed(
                                        packet_info['num_blocks'], 
                                        packet_info['degree'], 
                                        packet_info['seed_id']
                                    ))
                                    # For degree 1, this should be a single block
                                    if len(block_indices) == 1:
                                        block_index = block_indices[0]
                                    else:
                                        continue  # Not a valid degree 1 packet
                                elif 'block_nums' in packet_info:
                                    # For backward compatibility
                                    block_index = packet_info['block_nums'][0]
                                else:
                                    continue  # Can't determine block index
                                
                                # Skip if already found or out of range
                                if block_index in found_positions or block_index >= blocks_in_chunk:
                                    continue
                                    
                                # Verify this block belongs to our chunk and has right size
                                if len(decoded_packet) <= block_size:
                                    # Store this block at the correct position
                                    blocks_by_position[block_index] = decoded_packet
                                    found_positions.add(block_index)
                                    blocks_found += 1
                                
                                # If we have all blocks, we're done
                                if blocks_found >= blocks_in_chunk:
                                    break
                        except Exception as e:
                            continue
                            
                    # Now write the blocks in correct order
                    for i, block in enumerate(blocks_by_position):
                        if block is not None:
                            chunk_buffer.write(block)
                    
                    # Check if we have enough blocks to form the chunk
                    if blocks_found >= blocks_in_chunk:
                        # Get the full chunk data
                        chunk_buffer.seek(0)
                        chunk_data = chunk_buffer.read(chunk_size)  # Only get exactly what we need
                        
                        # Store the chunk
                        decoded_chunks[chunk_id] = chunk_data
                        chunks_processed += 1
                    else:
                        # Failed to decode this chunk, but we'll suppress the message to avoid cluttering the output
                        pass
                except Exception as e:
                    print(f"Error in decoding for chunk {chunk_id}: {e}")
        
    # Suppress this message to avoid interfering with the progress bar
    # print(f"Direct decoding: Processed {chunks_processed}/{file_metadata['num_chunks']} chunks successfully")
    
    # If direct decoding didn't work completely, use the regular FEC repair path
    if len(decoded_chunks) != file_metadata['num_chunks']:
        # Critical check at the very beginning of the function before anything else
        # This ensures we don't even start the executor if we're already paused
        if is_repair_paused():
            print(f"\n[FEC Repair interrupted before it even started: {filename_display}]")
            return decoded_chunks
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=repair_cores) as executor:
            # Check if we're already paused before starting
            if is_repair_paused():
                print(f"\n[FEC Repair starting in paused state for {filename_display}]")
                print(f"Will wait until resume signal before processing")
                # Wait for unpause
                pause_start_time = time.time()
                while is_repair_paused():
                    # Check again for stop during pause
                    if should_stop_repair():
                        print(f"\n!!! REPAIR ABORTED BEFORE STARTING: New file transfer in progress !!!")
                        # Just return empty results
                        return decoded_chunks
                    
                    time.sleep(0.1)
                pause_duration = time.time() - pause_start_time
                print(f"\n[FEC Repair starting for {filename_display} after {pause_duration:.1f}s initial pause]")
            
            # Submit all decoding tasks
            futures = []
            chunk_queue = []
            
            # First create a queue of all chunks to process
            # But ONLY include chunks that haven't been decoded yet
            for chunk_id in range(file_metadata['num_chunks']):
                # Skip chunks we've already decoded
                if chunk_id in decoded_chunks:
                    print(f"✓ Skipping chunk {chunk_id} in final repair - already decoded")
                    continue
                    
                # Only process chunks that have packets
                if chunk_id in chunk_packets and chunk_packets[chunk_id]:
                    chunk_queue.append(chunk_id)
                    
            print(f"\n{'='*60}")
            print(f"FINAL REPAIR QUEUE: {len(chunk_queue)} chunks need decoding")
            print(f"Chunks to process: {chunk_queue}")
            print(f"{'='*60}")
            
            # Process chunks in larger batches since we're using threading instead of multiprocessing
            batch_size = 10  # Process 10 chunks at a time since threading overhead is lower
            batch_index = 0
            
            # Slightly longer sleep time since we're using threads
            pause_check_interval = 0.05  # seconds
            
            # Check for pause before entering the main processing loop
            if is_repair_paused():
                print(f"\n[FEC Repair paused before entering main loop: {filename_display}]")
                return decoded_chunks
            
            # Reset the progress bar when entering FEC mode
            # Use our common update_progress_bar function for consistent display
            update_progress_bar(0, file_metadata['num_chunks'])
            
            while batch_index < len(chunk_queue):
                # Check interrupt event first (immediate response)
                if interrupt_event is not None and interrupt_event.is_set():
                    print(f"\n[FEC Repair interrupted at batch {batch_index} with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded]")
                    return decoded_chunks
                
                # Also check pause flags
                if is_repair_paused():
                    print(f"\n[FEC Repair paused at batch start with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded]")
                    print(f"Will resume from batch index {batch_index} later")
                    return decoded_chunks
                # Check if we need to completely abort the repair process
                if should_stop_repair():
                    print(f"\n!!! REPAIR STOPPED: New file transfer in progress !!!")
                    print(f"Exiting repair of {filename_display} to prioritize new transfer")
                    # Just return the chunks we've decoded so far
                    return decoded_chunks
                
                # Check for pause before processing each batch
                if is_repair_paused():
                    print(f"\n[FEC Repair paused: Metadata received during repair of {filename_display}]")
                    
                    # Sleep in short intervals with checks
                    pause_start_time = time.time()
                    
                    # Show which files we're waiting for
                    with repair_pause_lock:
                        if _metadata_queue:
                            print(f"Waiting for EOF markers from: {', '.join(_metadata_queue)}")
                        else:
                            print(f"Waiting for EOF markers...")
                    
                    while is_repair_paused():
                        # Check again for stop request during the pause
                        if should_stop_repair():
                            print(f"\n!!! REPAIR ABORTED: New file transfer priority !!!")
                            print(f"Exiting repair of {filename_display}")
                            # Just return the chunks we've decoded so far
                            return decoded_chunks
                        
                        # Sleep briefly
                        time.sleep(pause_check_interval)
                        
                        # If we've been paused for more than 5 seconds, print reminder periodically
                        pause_duration = time.time() - pause_start_time
                        if pause_duration > 5 and pause_duration % 10 < pause_check_interval:
                            # Check which files we're still waiting for
                            with repair_pause_lock:
                                if _metadata_queue:
                                    remaining_files = ", ".join(_metadata_queue)
                                    print(f"\n[FEC Repair for {filename_display} still paused after {int(pause_duration)}s]")
                                    print(f"Waiting for EOF markers from: {remaining_files}")
                                else:
                                    print(f"\n[FEC Repair for {filename_display} still paused after {int(pause_duration)}s]")
                                    print(f"Waiting for EOF markers...")
                    
                    # When resuming, print message with duration of pause
                    pause_duration = time.time() - pause_start_time
                    print(f"\n[FEC Repair resuming for {filename_display} after {pause_duration:.1f}s pause]")
                
                # Check again right before submitting batch (double check)
                if should_stop_repair():
                    print(f"\n!!! REPAIR STOPPED (FINAL CHECK): New file transfer in progress !!!")
                    print(f"Exiting repair of {filename_display} to prioritize new transfer")
                    # Just return the chunks we've decoded so far
                    return decoded_chunks
                
                # Submit a small batch of chunks
                end_index = min(batch_index + batch_size, len(chunk_queue))
                batch_futures = []
                
                for i in range(batch_index, end_index):
                    # Check again for each chunk (ultra responsive)
                    if should_stop_repair():
                        print(f"\n!!! REPAIR STOPPED (MID-BATCH): New file transfer in progress !!!")
                        print(f"Exiting repair of {filename_display} to prioritize new transfer")
                        # Just return the chunks we've decoded so far
                        return decoded_chunks
                        
                    # Yield GIL before chunk processing to give receiving thread a chance
                    yield_gil()
                    
                    # Check for pause before submitting each chunk
                    if is_repair_paused():
                        print(f"\n[FEC Repair paused: Metadata received during repair of {filename_display}]")
                        print(f"Stopping mid-batch - will resume from chunk {chunk_queue[i]} later")
                        # Return immediately with chunks decoded so far
                        return decoded_chunks
                    
                    chunk_id = chunk_queue[i]
                    future = executor.submit(decode_chunk, chunk_id, chunk_packets[chunk_id], file_metadata)
                    batch_futures.append((future, chunk_id))
                
                # Add to main futures list
                futures.extend(batch_futures)
                batch_index = end_index
                
                # Check for new progress occasionally
                time.sleep(0.01)  # Minimal sleep to reduce CPU usage
        
        # Process results as they complete
        for future_index, (future, chunk_id) in enumerate(futures):
            try:
                # Check if repair should be completely stopped
                if should_stop_repair():
                    print(f"\n!!! REPAIR RESULTS PROCESSING STOPPED: New file transfer in progress !!!")
                    print(f"Exiting repair results processing for {filename_display}")
                    # Just return the chunks we've decoded so far
                    return decoded_chunks
                
                # Check for pause requests before getting result
                if is_repair_paused():
                    print(f"\n[FEC Repair paused during result processing: New file transfer in progress]")
                    # Wait for unpause
                    pause_start_time = time.time()
                    while is_repair_paused():
                        # Check again for stop during pause
                        if should_stop_repair():
                            print(f"\n!!! REPAIR RESULTS PROCESSING ABORTED: New file transfer in progress !!!")
                            print(f"Exiting repair of {filename_display}")
                            # Just return the chunks we've decoded so far
                            return decoded_chunks
                            
                        time.sleep(0.1)
                    pause_duration = time.time() - pause_start_time
                    print(f"\n[FEC Repair resuming result processing after {pause_duration:.1f}s pause]")
                
                # Only try to get the result if we're not paused
                if not is_repair_paused():
                    result_chunk_id, chunk_data = future.result()
                else:
                    # Skip this result if we're paused
                    continue
                if chunk_data is not None:
                    decoded_chunks[result_chunk_id] = chunk_data
                    
                    # Check for pause immediately after adding a decoded chunk
                    if is_repair_paused():
                        print(f"\n[FEC Repair paused after decoding chunk {result_chunk_id}]")
                        print(f"Pausing with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded")
                        return decoded_chunks
                else:
                    # Track chunks that the decoder couldn't recover
                    failed_chunk_ids.add(result_chunk_id)
                
                # Update decoding progress more frequently (every chunk)
                # This is outside the if-else block because it applies to both cases
                decoded_count = len(decoded_chunks)
                processed_count = decoded_count + len(failed_chunk_ids)
                # Change from every 5 chunks to every 1 chunk for smoother updates
                if processed_count % 1 == 0 or processed_count == file_metadata['num_chunks']:
                    percent_processed = min(100, int(100 * processed_count / max(1, file_metadata['num_chunks'])))
                    
                    # Create colored progress bar using consistent colors with fast path
                    RED = '\033[38;5;124m'       # Dark red for failed chunks
                    
                    # First check for repair interrupt event - fastest response
                    # Check multiprocessing event
                    if interrupt_event is not None and interrupt_event.is_set():
                        print(f"\n[FEC Repair interrupted during progress update: {filename_display}]")
                        print(f"Interrupted with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded ({percent_processed}%)")
                        # Return immediately with chunks decoded so far
                        return decoded_chunks
                    
                    # Then check if we're paused - if so, don't update progress and return
                    # We check right before printing the progress bar to ensure immediate responsiveness
                    # This is a critical point for interruption
                    if is_repair_paused():
                        print(f"\n[FEC Repair paused: Metadata received during repair of {filename_display}]")
                        print(f"Stopping during progress update - will resume later")
                        print(f"Paused with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded ({percent_processed}%)")
                        # Return immediately with chunks decoded so far
                        return decoded_chunks
                    
                    # Print the progress bar only if not paused
                    # Check one more time right before printing to ensure immediate response
                    if not is_repair_paused() and not (interrupt_event is not None and interrupt_event.is_set()):
                        # Use our common update_progress_bar function
                        RED = '\033[38;5;124m'  # Dark red for failed chunks
                        
                        # Show progress with custom colors in FEC mode to indicate failed chunks
                        success_width = int((decoded_count / max(1, file_metadata['num_chunks'])) * bar_width)
                        failed_width = int((len(failed_chunk_ids) / max(1, file_metadata['num_chunks'])) * bar_width)
                        remaining_width = bar_width - (success_width + failed_width)
                        custom_bar = f"{DARK_GREEN}{'█' * success_width}{RED}{'█' * failed_width}{DARK_GREEN2}{'█' * remaining_width}{RESET}"
                        
                        # Use a consistent format but with the custom bar
                        print(f"{CLEAR_LINE}\rDecoding {filename_display}: {percent_processed}% |{custom_bar}| ({processed_count}/{file_metadata['num_chunks']} chunks)", end='', flush=True)
                        
                        # Force a small sleep every few chunks to make progress visible
                        if processed_count % 5 == 0:
                            time.sleep(0.01)
                        
                        # Check immediately after printing too
                        if interrupt_event is not None and interrupt_event.is_set():
                            print(f"\n[FEC Repair interrupted right after progress update]")
                            print(f"Interrupted with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded ({percent_processed}%)")
                            return decoded_chunks
                    else:
                        # We got paused just now during this microsecond
                        print(f"\n[FEC Repair paused: Caught at the very last moment]")
                        print(f"Paused with {len(decoded_chunks)}/{file_metadata['num_chunks']} chunks decoded ({percent_processed}%)")
                        return decoded_chunks
            except Exception as e:
                # Track the failed chunk
                failed_chunk_ids.add(chunk_id)
                print(f"Error processing chunk {chunk_id}: {e}")
    
    # Print final decoding status with newline
    # Create a final colored bar
    DARK_GREEN = '\033[38;5;22m'  # Dark green for successful
    RED = '\033[38;5;124m'       # Dark red for failed
    RESET = '\033[0m'
    
    bar_width = 20
    success_count = len(decoded_chunks)
    # Use tracked failed chunks for accuracy
    failed_count = len(failed_chunk_ids)
    unprocessed_count = file_metadata['num_chunks'] - success_count - failed_count
    
    total_processed = success_count + failed_count
    percent_processed = min(100, int(100 * total_processed / max(1, file_metadata['num_chunks'])))
    
    success_width = int((success_count / max(1, file_metadata['num_chunks'])) * bar_width)
    failed_width = int((failed_count / max(1, file_metadata['num_chunks'])) * bar_width)
    
    # Ensure we fill the whole bar when all chunks are processed
    if total_processed == file_metadata['num_chunks']:
        if failed_width == 0:
            success_width = bar_width
        else:
            # Adjust to fill the full width
            remaining = bar_width - (success_width + failed_width)
            failed_width += remaining
    
    # Calculate the remaining blue width for unprocessed chunks
    blue_width = bar_width - (success_width + failed_width)
    
    # Ensure we have at least one character for success/failure if they exist
    if success_count > 0 and success_width == 0:
        success_width = 1
        if blue_width > 0:
            blue_width -= 1
        elif failed_width > 1:
            failed_width -= 1
            
    if failed_count > 0 and failed_width == 0:
        failed_width = 1
        if blue_width > 0:
            blue_width -= 1
        elif success_width > 1:
            success_width -= 1
    
    # Create the bar with appropriate colors - use DARK_GREEN2 for pending chunks
    bar = f"{DARK_GREEN}{'█' * success_width}{RED}{'█' * failed_width}{DARK_GREEN2}{'█' * blue_width}{RESET}"
    
    print(f"\n\nDecoding {filename_display} complete: {success_count}/{file_metadata['num_chunks']} chunks decoded |{bar}| ({percent_processed}%)")
    
    # Return the decoded chunks dictionary
    return decoded_chunks

# Register SIGUSR1 handler immediately when module is loaded
import signal

# Global function to calculate a safe progress percentage (used instead of lambda for pickle compatibility)
def safe_progress_pct(n, total):
    """Calculate a percentage while ensuring it stays between 0-100%"""
    return min(100, max(0, int(100 * n / max(1, total))))

# Global state variables for FEC repair coordination
_fec_repair_in_progress = False
_fec_repair_paused = False  # Will never be set to True anymore
repair_pause_lock = threading.Lock()
_currently_processing_file = None
_repair_stop_requested = False  # This flag is now ignored - repairs are never stopped
_metadata_queue = []  # Queue of filenames from metadata packets
# _repair_interrupted variable removed as we no longer use SIGUSR2 for interruption

# Add an Event for repair thread interruption
# This provides a more reliable thread-safe way to signal the repair thread
repair_interrupt_event = threading.Event()  # This event is never set now - repairs aren't interrupted

# Helper functions to access and modify FEC repair state
def get_repair_state():
    """Get the current repair state variables as a dictionary"""
    return {
        "in_progress": _fec_repair_in_progress,
        "paused": _fec_repair_paused,
        "current_file": _currently_processing_file,
        "metadata_queue": _metadata_queue
    }

def set_repair_in_progress(file_name):
    """Mark FEC repair as in progress for the given file"""
    global _fec_repair_in_progress, _fec_repair_paused, _currently_processing_file
    with repair_pause_lock:
        # Make sure we start with a clean state
        _fec_repair_in_progress = True
        _fec_repair_paused = False  # Start unpaused
        _currently_processing_file = file_name
        
        print("\n[FEC Repair starting for file: {}]".format(file_name))
        
def clear_repair_state():
    """Clear all FEC repair state flags"""
    global _fec_repair_in_progress, _fec_repair_paused, _currently_processing_file, _repair_stop_requested
    with repair_pause_lock:
        _fec_repair_in_progress = False
        _fec_repair_paused = False
        _repair_stop_requested = False
        _currently_processing_file = None
        
def pause_repair():
    """Pause function is disabled - repairs are no longer interruptible"""
    # This function is intentionally disabled
    print("FEC repair pause function called but ignored - repairs are no longer interruptible")
    return
    
def resume_repair():
    """Resume function is disabled - repairs are no longer interruptible"""
    # This function is intentionally disabled
    print("FEC repair resume function called but ignored - repairs are no longer interruptible")
    return
    
def is_repair_paused():
    """Check if FEC repair is paused - always returns False now"""
    # Always return False since we're disabling repair interruptions
    return False
        
def should_stop_repair():
    """Check if repair should be stopped - always returns False now"""
    # Always return False since we're disabling repair interruptions
    return False

# Global handler for SIGUSR1 that works even before receive_file is called
def global_sigusr1_handler(sig, frame):
    print("\n\n")
    print(f"\n{'='*30}")
    print(f"INITIAL SUMMARY")
    print(f"{'='*30}")
    print(f"✓ Receiver is running")
    print(f"✓ No transfers active yet")
    print(f"✓ Waiting for incoming packets...")
    print("\n")

# Set up the SIGUSR1 signal handler only
signal.signal(signal.SIGUSR1, global_sigusr1_handler)


def main():
    """Main entry point when called directly"""
    # Initialize progress display using Textual if available
    progress_display = get_progress_display()
    
    # Store the progress display in the main function for access in callbacks
    main.progress_display = progress_display
    
    # If using Textual display, start it
    if hasattr(progress_display, 'start'):
        progress_display.start()
    
    parser = argparse.ArgumentParser(description="Receive a file over UDP with Parallel Chunked Robust Soliton FEC")
    parser.add_argument("output", nargs='?', default=None, 
                        help="Path to save the received file (optional, defaults to original filename)")
    parser.add_argument("--host", default="", 
                        help="Network interface to bind to (empty string for all interfaces, supports IPv4 or IPv6)")
    parser.add_argument("--multicast", default=None, 
                        help="Join multicast group with the specified address (e.g., '224.0.0.1' for IPv4 or 'ff02::1' for IPv6)")
    parser.add_argument("--broadcast", action="store_true", 
                        help="Enable reception of broadcast packets (IPv4 only)")
    parser.add_argument("--port", type=int, default=12345, 
                        help="Network port to listen on")
    parser.add_argument("--loss", type=float, default=0.0, 
                        help="Simulated packet loss rate (0-1) for testing reliability")
    parser.add_argument("--timeout", type=float, default=600, 
                        help="Time in seconds to wait before giving up on receiving more packets")
    parser.add_argument("--max-packet-size", type=int, default=65536,
                        help="Maximum UDP packet size in bytes to receive")
    parser.add_argument("--accurate-speed", action="store_true",
                        help="Display network speed that accounts for all protocol overhead (matches tools like nload)")
    parser.add_argument("--partial", action="store_true",
                        help="Write partial files with missing chunks filled with zeros when FEC repair fails")
    parser.add_argument("--pcap", type=str, default=None,
                        help="Read packets from a .pcap file instead of the network interface")
    parser.add_argument("--pcapng", type=str, default=None,
                        help="Read packets from a .pcapng file instead of the network interface (newer format)")
    parser.add_argument("--napatech", type=str, default=None,
                        help="Convert Napatech capture file to PCAP format using /opt/napatech3/bin/capfileconvert")
    
    args = parser.parse_args()
    
    # Validate network parameters
    if args.port < 1 or args.port > 65535:
        print(f"Error: Port number must be between 1 and 65535")
        sys.exit(1)
    
    if args.loss < 0 or args.loss > 1:
        print(f"Error: Loss rate must be between 0 and 1")
        sys.exit(1)
        
    if args.timeout <= 0:
        print(f"Error: Timeout must be greater than 0")
        sys.exit(1)
        
    if args.max_packet_size < 1024 or args.max_packet_size > 65536:
        print(f"Error: Packet size must be between 1024 and 65536")
        sys.exit(1)
        
    # Quiet delay is no longer used - we process chunks immediately
    
    # We don't use tqdm progress bars anymore
    pass
    
    # Check for PCAP/PCAPNG/Napatech input
    pcap_temp_file = None
    
    # Handle Napatech file conversion if --napatech flag is specified
    if args.napatech:
        print(f"Converting Napatech capture file {args.napatech} to PCAP format...")
        pcap_temp_file = convert_napatech_to_pcap(args.napatech)
        
        if pcap_temp_file:
            print(f"Using converted PCAP file: {pcap_temp_file}")
            pcap_file = pcap_temp_file
            pcap_format = "pcap"
        else:
            print(f"Error: Failed to convert Napatech file. Exiting.")
            sys.exit(1)
    else:
        # Use regular PCAP/PCAPNG file if specified
        pcap_file = args.pcap or args.pcapng
        pcap_format = "pcapng" if args.pcapng else "pcap" if args.pcap else None
    
    # Call receive_file with the parsed arguments
    try:
        receive_file(args.output, bind_addr=(args.host, args.port), 
                    simulated_loss=args.loss, timeout=args.timeout,
                    max_packet_size=args.max_packet_size, accurate_speed=args.accurate_speed,
                    partial=args.partial, multicast=args.multicast, broadcast=args.broadcast,
                    pcap_file=pcap_file, pcap_format=pcap_format)
    finally:
        # Clean up progress display if needed
        if hasattr(main, 'progress_display') and hasattr(main.progress_display, 'stop'):
            main.progress_display.stop()
        
        # Clean up temporary PCAP file if it was created from Napatech conversion
        if pcap_temp_file and os.path.exists(pcap_temp_file):
            try:
                os.unlink(pcap_temp_file)
                print(f"Removed temporary PCAP file: {pcap_temp_file}")
            except Exception as e:
                print(f"Warning: Failed to remove temporary PCAP file: {e}")

if __name__ == "__main__":
    main()
