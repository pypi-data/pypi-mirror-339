# Robust Soliton Data Diode 

A data diode implementation using robust soliton fountain codes for reliable one-way data transmission.
Specialized network capture cards allow for lossless packet capture (see receiver --napatech). 

When using specialized capture cards (see --napatech) tapped into a media-converter, 
there is perfect UDP reception (no packet loss). For example NAPATECH NT4E-4T 4-Port 
PCIe x8 Gbit Capture Network Adapter 801-0075-09-02 connected to TP-Link MC200CM 
(850 nm light) or MC210CS (1310 nm light). If using beam splitters for TX->RX link, 
the 1310 nm fiber-optic is easy and cheaper to find.

## Installation

### From PyPI (recommended)

```
pip install datadiode-RobustSoliton
```

### From Source

1. Clone the repository:
   ```
   git clone https://github.com/BANPUMP-team/datadiode-RobustSoliton.git
   cd datadiode-RobustSoliton 
   ```

2. Install in development mode:
   ```
   pip install -e .
   ```

## Usage

### Basic operation:

Run the sender:
```
datadiode-RobustSoliton send [options] file_to_send
```

Run the receiver:
```
datadiode-RobustSoliton receive [options] output_file
```

For more details on options, run:
```
datadiode-RobustSoliton --help
datadiode-RobustSoliton send --help
datadiode-RobustSoliton receive --help
```
