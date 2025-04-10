"""
Main entry point for the Robust Soliton FEC package.

This package provides reliable file transfer over UDP using Robust Soliton
fountain codes. It's designed for high reliability in lossy networks, including
data diodes and one-way communication channels.
"""
import sys
import os
import argparse

def main():
    """Main entry point for the package"""
    # Get the program name from sys.argv[0]
    prog_name = os.path.basename(sys.argv[0])
    
    parser = argparse.ArgumentParser(
        description=f"""Robust Soliton FEC File Transfer

A UDP-based file transfer utility with Forward Error Correction (FEC)
that provides resilience against packet loss. Designed for transferring
files over perfect data diodes but also over lossy networks.

When using specialized capture cards (see --napatech) tapped into a media-converter, 
there is perfect UDP reception (no packet loss). For example NAPATECH NT4E-4T 4-Port 
PCIe x8 Gbit Capture Network Adapter 801-0075-09-02 connected to TP-Link MC200CM 
(850 nm light) or MC210CS (1310 nm light). If using beam splitters for TX->RX link, 
the 1310 nm fiber-optic is easy and cheaper to find.

For a complete parameter list, use:
  {prog_name} send --help
  {prog_name} receive --help

Example usage:
  # Sender
  {prog_name} send large_file.bin --host 192.168.1.100 --port 12345 --overhead 8.0
  
  # Receiver
  {prog_name} receive output.bin --port 12345
  
See README.md for detailed parameter descriptions and tuning recommendations.
""", 
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", choices=["send", "receive"], 
                        help="Mode: 'send' to transmit files, 'receive' to receive files")
    
    # Check for help after mode
    if len(sys.argv) == 3 and sys.argv[1] in ["send", "receive"] and sys.argv[2] in ["-h", "--help"]:
        if sys.argv[1] == "send":
            # Run sender's help directly
            from datadiode_RobustSoliton.RobustSolitonSender import main as sender_main
            sys.argv = [sys.argv[0], "--help"]
            sender_main()
            return
        else:
            # Run receiver's help directly
            from datadiode_RobustSoliton.RobustSolitonReceiver import main as receiver_main
            sys.argv = [sys.argv[0], "--help"]
            receiver_main()
            return
    
    # Check for empty command
    if len(sys.argv) == 1:
        parser.print_help()
        return
        
    # Parse just the first argument to determine mode
    try:
        args, remaining = parser.parse_known_args()
        
        if args.mode == "send":
            # Check if a file was specified for send mode
            if len(remaining) == 0:
                print("Error: Please specify a file to send.")
                print("Example: datadiode-RobustSoliton send myfile.txt")
                return
                
            # Import sender and run it with remaining arguments
            from datadiode_RobustSoliton.RobustSolitonSender import main as sender_main
            sys.argv = [sys.argv[0]] + remaining
            sender_main()
        elif args.mode == "receive":
            # Import receiver and run it with remaining arguments
            from datadiode_RobustSoliton.RobustSolitonReceiver import main as receiver_main
            sys.argv = [sys.argv[0]] + remaining
            receiver_main()
    except Exception as e:
        print(f"Error: {str(e)}")
        parser.print_help()

if __name__ == "__main__":
    main()
