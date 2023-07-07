# Port-Scanner

A simple Python script that scans for open ports on a target host. It utilizes multi-threading to speed up the scanning process and provides basic information about the open ports.

## Features

- Scans a range of ports on a target host to check for openness
- Provides a list of open ports with their associated service names
- Performs Reverse DNS lookup
- Supports saving the results to a file

## Requirements

- Python 3.x
- The following Python libraries:
  - `pyfiglet` (for printing ASCII banners)
  - `socket` (for network communication)
  - `concurrent.futures` (for multi-threading)
  - `subprocess` (for executing the ping command)
  - `datetime` (for timestamping)
  - `dns.reversename`(For DNS lookup)
  
## Usage

1. Clone the repository:

2. Run the script

3. Follow the prompts to enter the target host, starting port, and ending port.

4. The script will scan the specified ports on the target host and display the results.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to submit a pull request.



