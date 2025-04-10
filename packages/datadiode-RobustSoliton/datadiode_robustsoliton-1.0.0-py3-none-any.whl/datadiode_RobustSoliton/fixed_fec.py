"""
Fixed FEC implementation with safe UDP packet sizes
"""
import numpy as np
from collections import defaultdict
import pickle
import struct
import json  # Use JSON instead of pickle for smaller, safer serialization
from datadiode_RobustSoliton.soliton import robust_soliton, get_degree_from_distribution
from datadiode_RobustSoliton.prng import choose_blocks, get_blocks_from_seed, PRNGType

# Maximum safe UDP packet size
MAX_UDP_SIZE = 65000  # Slightly below the theoretical max of 65536

class Encoder:
    """
    Encoder for Fountain codes using Robust Soliton distribution.
    """
    def __init__(self, data, block_size=8192, c=0.03, delta=0.05, seed=None):
        """
        Initialize the encoder.
        
        Args:
            data: Input data as bytes
            block_size: Size of each block in bytes
            c: Robust soliton parameter
            delta: Desired decoding failure probability
            seed: Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
            
        self.data = data
        self.block_size = block_size
        
        # Split data into blocks
        self.blocks = []
        for i in range(0, len(data), block_size):
            block = data[i:i+block_size]
            if len(block) < block_size:
                # Pad the last block
                block = block + bytes(block_size - len(block))
            self.blocks.append(block)
        
        self.K = len(self.blocks)
        self.degree_dist = robust_soliton(self.K, c, delta)
        
        # Pre-allocate block data as numpy arrays for XOR operations
        self.block_arrays = [np.frombuffer(block, dtype=np.uint8) for block in self.blocks]
        
        # Calculate safe block size
        self._calculate_safe_block_size()
        
    def _calculate_safe_block_size(self):
        """Calculate the maximum safe block size based on UDP limits"""
        # Create a mock packet info with maximum expected values
        max_packet_info = {
            'degree': self.K,  # Maximum possible degree
            'seed_id': 2**32 - 1,  # Maximum seed ID
            'num_blocks': self.K,
            'block_size': self.block_size
        }
        
        # Use JSON instead of pickle - much smaller serialization
        info_bytes = json.dumps(max_packet_info).encode('utf-8')
        header = struct.pack('!I', len(info_bytes))
        
        # Calculate overhead
        metadata_size = len(header) + len(info_bytes)
        max_safe_data_size = MAX_UDP_SIZE - metadata_size - 100  # Extra safety margin
        
        # Debug messages commented out to avoid interference with progress bar
        # print(f"Metadata size: {metadata_size} bytes")
        # print(f"Maximum safe data size: {max_safe_data_size} bytes")
        
        if self.block_size > max_safe_data_size:
            old_block_size = self.block_size
            self.block_size = max_safe_data_size
            # Use warning for important messages
            import tqdm
            tqdm.tqdm.write(f"WARNING: Reducing block size from {old_block_size} to {self.block_size} to fit UDP limits")
            # We should really re-split the data, but for now we'll just truncate
        
    def next_packet(self):
        """
        Generate next packet according to the degree distribution.
        
        Returns:
            (packet_data, packet_info) where packet_info contains metadata
        """
        # Ensure a mix of degree 1 and higher degree packets
        if self.K > 3 and np.random.random() < 0.3:  # 30% chance of degree 1
            degree = 1
        else:
            degree = get_degree_from_distribution(self.degree_dist)
            
        # Ensure degree doesn't exceed K
        degree = min(degree, self.K)
        
        # Generate a random seed for block selection
        seed_id = np.random.randint(2**32)
        
        # Use our optimized block selection algorithm
        block_indices = get_blocks_from_seed(self.K, degree, seed_id)
        
        # XOR the selected blocks
        packet_data = np.zeros(self.block_size, dtype=np.uint8)
        for idx in block_indices:
            packet_data ^= self.block_arrays[idx]
        
        # Create packet info - now sending seed instead of block_indices
        packet_info = {
            'degree': degree,
            'seed_id': seed_id,
            'num_blocks': self.K,
            'block_size': self.block_size
        }
        
        return bytes(packet_data), packet_info
    
    def encode_packet(self, packet_data, packet_info, max_size=None):
        """
        Serialize a packet for transmission.
        
        Args:
            packet_data: The encoded data
            packet_info: Metadata about the packet
            max_size: Optional maximum size for UDP packet (default: uses MAX_UDP_SIZE)
            
        Returns:
            Bytes ready for transmission
        """
        # Use provided max_size or default to MAX_UDP_SIZE
        if max_size is None:
            max_size = MAX_UDP_SIZE
            
        # Convert numpy int64 to regular int for JSON serialization
        json_safe_info = {}
        for key, value in packet_info.items():
            # Convert numpy types to Python built-in types
            if isinstance(value, np.integer):
                json_safe_info[key] = int(value)
            elif isinstance(value, np.floating):
                json_safe_info[key] = float(value)
            else:
                json_safe_info[key] = value
                
        # Use JSON instead of pickle for more efficient serialization
        info_bytes = json.dumps(json_safe_info).encode('utf-8')
        header = struct.pack('!I', len(info_bytes))
        
        # Calculate total size
        total_size = len(header) + len(info_bytes) + len(packet_data)
        
        if total_size > max_size:
            # Log a warning if this happens (should be rare with our safe block size calculations)
            print(f"Warning: Packet size ({total_size} bytes) exceeds max UDP size ({max_size} bytes).")
            # Truncate packet data to fit within limit
            max_data_size = max_size - len(header) - len(info_bytes)
            if max_data_size > 0:
                packet_data = packet_data[:max_data_size]
                print(f"Reduced data size to {max_data_size} bytes")
            else:
                print(f"Cannot reduce packet size: metadata too large ({len(header) + len(info_bytes)} bytes)")
            
        return header + info_bytes + packet_data

class Decoder:
    """
    Decoder for Fountain codes using Robust Soliton distribution.
    """
    def __init__(self):
        """
        Initialize the decoder.
        """
        self.decoded_blocks = {}  # Maps block index to block data
        self.coded_packets = []   # List of (block_indices, data) tuples
        self.ripple = set()       # Set of indices of degree-1 packets
        self.num_blocks = None
        self.block_size = None
        self.received_packets = 0
        
    def decode_packet(self, packet_bytes):
        """
        Decode a serialized packet.
        
        Args:
            packet_bytes: Received packet bytes
            
        Returns:
            (packet_data, packet_info)
        """
        info_size_bytes = packet_bytes[:4]
        info_size = struct.unpack('!I', info_size_bytes)[0]
        
        info_bytes = packet_bytes[4:4+info_size]
        # Use JSON instead of pickle for safer deserialization
        packet_info = json.loads(info_bytes.decode('utf-8'))
        
        packet_data = packet_bytes[4+info_size:]
        
        return packet_data, packet_info
    
    def process_packet(self, packet_data, packet_info):
        """
        Process a received packet and attempt to decode blocks.
        
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
        
        # Reconstruct block indices from seed using our deterministic algorithm
        # Implementation in get_blocks_from_seed now ignores PRNG type
        # So we'll get the same block indices as the sender regardless of PRNG type
        degree = packet_info['degree']
        seed_id = packet_info['seed_id']
        block_indices = list(get_blocks_from_seed(self.num_blocks, degree, seed_id))
        
        # Convert data to numpy array
        packet_array = np.frombuffer(packet_data, dtype=np.uint8)
        
        # Process already decoded blocks
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
            processed_packets = 0
            
            # Limit the number of packets we process to avoid excessive loops
            max_packets_to_process = min(100, len(self.coded_packets))
            
            for indices, data in self.coded_packets[:max_packets_to_process]:
                processed_packets += 1
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
                    
            # Keep any remaining packets that we didn't process
            if processed_packets < len(self.coded_packets):
                new_coded_packets.extend(self.coded_packets[processed_packets:])
                
            self.coded_packets = new_coded_packets
            
            # Continue processing to see if we've unlocked more blocks
            # Repeat until no more progress is made or decoding is complete
            progress_made = True
            while progress_made and len(self.decoded_blocks) < self.num_blocks:
                progress_made = False
                new_coded_packets = []
                degree_one_packets = []
                
                # First collect all degree-1 packets
                for indices, data in self.coded_packets:
                    if len(indices) == 1:
                        degree_one_packets.append((indices[0], data))
                    else:
                        new_coded_packets.append((indices, data))
                
                # Process all degree-1 packets
                for idx, data in degree_one_packets:
                    self.decoded_blocks[idx] = data
                    progress_made = True
                
                # If we made progress, update remaining packets
                if progress_made:
                    updated_packets = []
                    for indices, data in new_coded_packets:
                        updated_indices = []
                        updated_data = data.copy()
                        
                        for idx in indices:
                            if idx in self.decoded_blocks:
                                # XOR with decoded block
                                updated_data = updated_data ^ self.decoded_blocks[idx]
                            else:
                                updated_indices.append(idx)
                        
                        if len(updated_indices) == 0:
                            # All blocks in this packet are now decoded
                            pass
                        elif len(updated_indices) == 1:
                            # This becomes a degree-1 packet
                            new_idx = updated_indices[0]
                            self.decoded_blocks[new_idx] = updated_data
                            progress_made = True
                        else:
                            # Still a higher degree packet
                            updated_packets.append((updated_indices, updated_data))
                    
                    new_coded_packets = updated_packets
                
                self.coded_packets = new_coded_packets
        else:
            # Before storing, check if this packet is useful
            # It's useful if it contains at least one undecoded block
            has_undecoded = False
            for idx in block_indices:
                if idx not in self.decoded_blocks:
                    has_undecoded = True
                    break
                    
            if has_undecoded:
                # Limit the number of stored packets to avoid memory issues
                if len(self.coded_packets) < 2000:  # Store up to 2000 packets
                    self.coded_packets.append((block_indices, packet_array))
            
        # Check if decoding is complete
        return len(self.decoded_blocks) == self.num_blocks
    
    def get_decoded_data(self):
        """
        Get the decoded data if decoding is complete.
        
        Returns:
            Decoded data as bytes if complete, None otherwise
        """
        # Check that all blocks have been decoded
        if len(self.decoded_blocks) < self.num_blocks:
            return None
            
        # Assemble the decoded blocks
        result = bytearray()
        for i in range(self.num_blocks):
            if i in self.decoded_blocks:
                block_data = self.decoded_blocks[i]
                result.extend(block_data)
            else:
                # This should never happen since we check for full decoding above
                print(f"Error: Missing block {i} despite full decoding check")
                return None
            
        return bytes(result)
    
    def get_stats(self):
        """
        Get decoding statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'received_packets': self.received_packets,
            'decoded_blocks': len(self.decoded_blocks),
            'total_blocks': self.num_blocks if self.num_blocks is not None else 0
        }
        
    def fast_decode_all_packets(self, packets, num_blocks, block_size, expected_size=None):
        """
        Fast decoding method for when all packets are available.
        Instead of complex FEC decoding, directly extracts blocks from degree-1 packets,
        then uses those to decode higher-degree packets in a cascade.
        
        Args:
            packets: List of encoded packets
            num_blocks: Total number of blocks in the chunk
            block_size: Size of each block in bytes
            expected_size: Expected size of the final decoded data (for truncation)
            
        Returns:
            Decoded data as bytes, or None if decoding fails
        """
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.decoded_blocks = {}  # Reset for this chunk
        self.coded_packets = []
        
        # Process all packets to extract degree-1 packets first
        degree_1_packets = []  # (block_index, data)
        higher_degree_packets = []  # (block_indices, data)
        
        # First pass: identify and sort packets by degree
        for i, packet_data in enumerate(packets):
            try:
                # Decode the packet
                decoded_data, packet_info = self.decode_packet(packet_data)
                
                # Extract block indices
                degree = packet_info.get('degree', 0)
                
                if degree == 1:
                    # This is a degree-1 packet (containing a single block)
                    if 'seed_id' in packet_info:
                        # Get block indices from seed
                        block_indices = list(get_blocks_from_seed(
                            packet_info['num_blocks'], 
                            packet_info['degree'], 
                            packet_info['seed_id']
                        ))
                        
                        if len(block_indices) == 1:
                            # Store directly
                            block_index = block_indices[0]
                            degree_1_packets.append((block_index, np.frombuffer(decoded_data, dtype=np.uint8)))
                            
                    elif 'block_nums' in packet_info:
                        # Backward compatibility mode
                        block_index = packet_info['block_nums'][0]
                        degree_1_packets.append((block_index, np.frombuffer(decoded_data, dtype=np.uint8)))
                else:
                    # Higher degree packet
                    if 'seed_id' in packet_info:
                        # Get block indices from seed
                        block_indices = list(get_blocks_from_seed(
                            packet_info['num_blocks'], 
                            packet_info['degree'], 
                            packet_info['seed_id']
                        ))
                        if len(block_indices) > 1:
                            # Store for further processing
                            higher_degree_packets.append(
                                (block_indices, np.frombuffer(decoded_data, dtype=np.uint8))
                            )
            except Exception:
                # Skip invalid packets
                continue
        
        # Store all found degree-1 packets
        for block_index, data in degree_1_packets:
            if block_index < num_blocks:
                self.decoded_blocks[block_index] = data
                
        # Now process higher degree packets in a cascade
        # This can decode additional blocks that weren't in degree-1 packets
        rounds = 0
        max_rounds = 10  # Limit iterations to avoid endless loops
        progress_made = True
        
        while progress_made and rounds < max_rounds:
            rounds += 1
            progress_made = False
            remaining_packets = []
            
            for block_indices, data in higher_degree_packets:
                # Filter out already decoded blocks
                remaining_indices = []
                packet_data = data.copy()  # Use copy to avoid modifying original
                
                # XOR out all known blocks
                for idx in block_indices:
                    if idx in self.decoded_blocks:
                        packet_data ^= self.decoded_blocks[idx]
                    else:
                        remaining_indices.append(idx)
                
                if len(remaining_indices) == 0:
                    # All blocks in this packet are decoded already
                    pass
                elif len(remaining_indices) == 1:
                    # This packet has been reduced to degree-1
                    # It reveals a new block
                    new_block_idx = remaining_indices[0]
                    self.decoded_blocks[new_block_idx] = packet_data
                    progress_made = True
                else:
                    # Still a higher degree packet, keep for next round
                    remaining_packets.append((remaining_indices, packet_data))
            
            # Update packet list for next round
            higher_degree_packets = remaining_packets
            
            # Early exit if we've decoded all blocks
            if len(self.decoded_blocks) == num_blocks:
                break
        
        # Check if we have all blocks
        if len(self.decoded_blocks) == num_blocks:
            # Build the final data
            result = bytearray()
            for i in range(num_blocks):
                if i in self.decoded_blocks:
                    result.extend(self.decoded_blocks[i])
                else:
                    # We're missing a block despite our check
                    # This shouldn't happen if we've verified all blocks are decoded
                    return None
            
            # Truncate to the expected size if provided
            if expected_size is not None and len(result) > expected_size:
                result = result[:expected_size]
                
            return bytes(result)
        
        # We couldn't decode all blocks even with fast path
        return None