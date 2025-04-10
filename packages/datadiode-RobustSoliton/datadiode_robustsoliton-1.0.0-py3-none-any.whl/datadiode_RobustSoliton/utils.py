"""
Utility functions and classes for the Robust Soliton implementation
"""
import os
import time
import hashlib
import mmap
import io
import sys
import threading
from typing import Dict, Any, Optional

def get_file_size(file_path):
    """Get the size of a file in bytes"""
    return os.path.getsize(file_path)

def get_file_hash(file_path):
    """Calculate MD5 hash of a file efficiently"""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def load_large_file(file_path):
    """
    Load a large file efficiently using memory mapping
    
    Args:
        file_path: Path to the file to load
        
    Returns:
        The file data as a bytes-like object
    """
    file_size = get_file_size(file_path)
    start_time = time.time()
    
    print(f"Loading file: {file_path}")
    print(f"File size: {file_size/1024/1024:.2f} MB")
    
    try:
        # Try to use memory mapping for efficient loading
        with open(file_path, 'rb') as f:
            # Memory map the file
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            data = mm
            print(f"File loaded using memory mapping in {time.time()-start_time:.2f} seconds")
            return data
    except Exception as e:
        print(f"Memory mapping failed: {e}, falling back to regular file reading")
        
        # Fall back to regular file reading
        with open(file_path, 'rb') as f:
            data = f.read()
        
        print(f"File loaded regularly in {time.time()-start_time:.2f} seconds")
        return data
        
def load_large_file_chunk(file_path, offset, size):
    """
    Load a specific chunk of a large file
    
    Args:
        file_path: Path to the file to load
        offset: Starting position in the file (in bytes)
        size: Size of the chunk to load (in bytes)
        
    Returns:
        The chunk data as a bytes object
    """
    start_time = time.time()
    
    try:
        # Try memory mapping first
        with open(file_path, 'rb') as f:
            # Memory map the file
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            # Extract the chunk
            data = mm[offset:offset+size]
            # Convert to bytes to ensure consistent behavior
            data_bytes = bytes(data)
            mm.close()
            return data_bytes
    except Exception as e:
        # Fall back to regular file reading
        with open(file_path, 'rb') as f:
            f.seek(offset)
            data = f.read(size)
        return data


class MultiProgressDisplay:
    """
    Display multiple progress bars simultaneously in the terminal
    using ANSI control sequences for cursor positioning.
    """
    def __init__(self, initial_bars=5):
        """Initialize with dynamic progress bar support"""
        self.progress_bars = {}  # filename -> {index, total, received, start_time, etc.}
        self.lock = threading.Lock()
        self.reserved_lines = 0
        self.lines_added = 0
        self.message_line = 1  # Line after the progress bars for messages, will be updated
        
        # ANSI codes for terminal control
        self.CLEAR_LINE = "\033[2K"
        self.CURSOR_UP = "\033[{}A"
        self.CURSOR_DOWN = "\033[{}B"
        self.CURSOR_HOME = "\r"
        self.SAVE_POS = "\033[s"
        self.RESTORE_POS = "\033[u"
        
        # Colors - array of colors to cycle through
        self.colors = [
            "\033[38;5;39m",   # Blue
            "\033[38;5;208m",  # Orange
            "\033[38;5;46m",   # Green
            "\033[38;5;196m",  # Red
            "\033[38;5;201m",  # Magenta
            "\033[38;5;226m",  # Yellow
            "\033[38;5;81m",   # Cyan
            "\033[38;5;214m",  # Dark Orange
        ]
        self.RESET = "\033[0m"
        
        # Reserve initial space
        self.reserved_lines = initial_bars
        # Print more initial newlines to create separation from previous outputs
        print("\n" * (initial_bars + 5))
        
    def add_transfer(self, filename, total_packets):
        """Add a new file transfer to track"""
        with self.lock:
            # Check if we're already tracking this file
            if filename in self.progress_bars:
                return
            
            # Add a new line if we need more space
            if self.lines_added >= self.reserved_lines:
                # Add extra newlines for better separation
                print("\n\n\n")  # Add multiple newlines for this progress bar
                self.reserved_lines += 3  # Account for the extra newlines
                
            # Assign the next index and color
            index = self.lines_added
            color_index = index % len(self.colors)
            self.lines_added += 1
            
            # Update message line position
            self.message_line = self.lines_added + 1
            
            # Store the transfer info
            self.progress_bars[filename] = {
                "index": index,
                "total": total_packets,
                "received": 0,
                "start_time": time.time(),
                "last_update": time.time(),
                "speed": 0.0,
                "color": self.colors[color_index],
            }
            
            # Display initial progress bar
            self._update_progress_bar(filename)
            
    def update_transfer(self, filename, packets_received):
        """Update the progress of a file transfer"""
        with self.lock:
            if filename not in self.progress_bars:
                return
                
            # Update the transfer info
            transfer = self.progress_bars[filename]
            transfer["received"] = packets_received
            
            # Calculate speed
            elapsed = time.time() - transfer["start_time"]
            if elapsed > 0:
                bytes_received = packets_received * 8192  # Assuming 8KB packets
                transfer["speed"] = bytes_received / elapsed / (1024 * 1024)
                
            # Update the progress bar
            self._update_progress_bar(filename)
            
    def complete_transfer(self, filename):
        """Mark a transfer as complete"""
        with self.lock:
            if filename not in self.progress_bars:
                return
                
            # Mark as complete
            transfer = self.progress_bars[filename]
            transfer["received"] = transfer["total"]
            
            # Update the progress bar with complete status
            self._update_progress_bar(filename, complete=True)
            
    def print_message(self, message):
        """Print a message below the progress bars"""
        with self.lock:
            # Save cursor position
            sys.stdout.write(self.SAVE_POS)
            
            # Move to message line (after all progress bars)
            sys.stdout.write(self.CURSOR_UP.format(1))
            
            # Clear line and print message with extra newlines for better separation
            sys.stdout.write(self.CLEAR_LINE + self.CURSOR_HOME + "\n\n" + message + "\n")
            
            # Restore cursor position
            sys.stdout.write(self.RESTORE_POS)
            sys.stdout.flush()
            
    def _update_progress_bar(self, filename, complete=False):
        """Update a specific progress bar"""
        if filename not in self.progress_bars:
            return
            
        transfer = self.progress_bars[filename]
        index = transfer["index"]
        total = transfer["total"]
        received = transfer["received"]
        speed = transfer["speed"]
        color = transfer["color"]
        
        # Calculate percentage and bar
        if total > 0:
            pct = min(100, int(received * 100 / total))
        else:
            pct = 0
            
        # Create the progress bar
        bar_width = 20
        filled_width = int(pct / 100 * bar_width)
        empty_width = bar_width - filled_width
        bar = f"{color}{'█' * filled_width}{' ' * empty_width}{self.RESET}"
        
        # Create status line
        if complete:
            status = f"Receiving {filename}: 100%|{bar}| {total}/{total} pkts (complete)"
        else:
            status = f"Receiving {filename}: {pct}%|{bar}| {received}/{total} pkts ({speed:.2f}MB/s)"
            
        # Save cursor position
        sys.stdout.write(self.SAVE_POS)
        
        # Calculate how many lines to move up to reach this file's progress bar
        # We need to go up from the current position (end of output) to the specific bar
        # This is (total bars + 1) - index position from top
        lines_from_bottom = self.lines_added + 1 - index
        
        # Move cursor to the progress bar's line
        sys.stdout.write(self.CURSOR_UP.format(lines_from_bottom))
        
        # Clear line and write new status
        sys.stdout.write(self.CLEAR_LINE + self.CURSOR_HOME + status)
        
        # Restore cursor position
        sys.stdout.write(self.RESTORE_POS)
        sys.stdout.flush()
        
    def stop(self):
        """Clean up before exiting"""
        with self.lock:
            self.progress_bars = {}
            # Move cursor below all progress bars
            sys.stdout.write(self.CURSOR_DOWN.format(self.lines_added))
            sys.stdout.flush()
        
    def remove_transfer(self, filename):
        """Remove a transfer from tracking but keep its line"""
        with self.lock:
            if filename not in self.progress_bars:
                return
                
            # Get transfer info
            transfer = self.progress_bars[filename]
            index = transfer["index"]
            
            # Clear the progress bar
            sys.stdout.write(self.SAVE_POS)
            lines_from_bottom = self.lines_added + 1 - index
            sys.stdout.write(self.CURSOR_UP.format(lines_from_bottom))
            sys.stdout.write(self.CLEAR_LINE)
            sys.stdout.write(self.RESTORE_POS)
            sys.stdout.flush()
            
            # Remove from tracking
            del self.progress_bars[filename]


# Factory function to get appropriate progress display
def get_progress_display():
    """
    Returns an appropriate progress display that supports unlimited progress bars.
    """
    return MultiProgressDisplay(initial_bars=1)  # Start with 1 line, but can grow dynamically