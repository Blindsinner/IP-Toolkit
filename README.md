
## IP Toolkit

IP Toolkit is a Python program with a graphical user interface (GUI) that provides various IP address-related functions.

The following functions are included:

-   Binary to IP address
-   IP address to Binary
-   Find Network Address from IP and Subnet Mask
-   Convert IP and CIDR Notation to Subnet Mask
-   Calculate Possible Subnetting from IP range
-   Determine IP Class and Private/Public Status
-   Convert IPv4 to IPv4-mapped IPv6
-   Convert IPv4-mapped IPv6 to IPv4
-   Display All Information for an IP Address and Subnet

## Requirements

-   Python 3.6 or later
-   `ipaddress` library
-   `tkinter` library (included with Python)

## Installation

1.  Clone the repository or download the code as a ZIP file and extract it.
2.  Open a terminal or command prompt and navigate to the directory where the code is located.
3.  Install the required libraries by running the command `pip install -r requirements.txt`.

### Download Exe file for windows (Portable)(Require Python 3.11 Installed)
[Download From Here](https://github.com/Blindsinner/IP-Toolkit/blob/main/ip_tool.py)
## Usage

To run the program, navigate to the directory where the code is located and run the command `python ip_toolkit.py`.

A GUI will appear with a list of available functions. Clicking on a function will display input fields for the required parameters, and clicking the "Submit" button will display the output in the text area at the bottom of the window.

## Example

To find the network address of the IP address `192.168.1.100` with subnet mask `255.255.255.0`, follow these steps:

1.  Run the program as described in the Usage section.
2.  Click the "Find Network Address from IP and Subnet Mask" button.
3.  Enter `192.168.1.100` in the "IP Address" field.
4.  Enter `255.255.255.0` in the "Subnet Mask / CIDR" field.
5.  Click the "Submit" button.

The program will output `192.168.1.0`.

## Credits

This program was created by [FAYSAL MAHMUD](https://github.com/Blindsinner) as a project for the Network Engineers
## License

This project is licensed under the MIT License
## Contributing

Contributions and pull requests are welcome. If you find any issues or have ideas for improvement, please open an issue or submit a pull request.

When submitting a pull request, please ensure that your code adheres to the current code style and that all tests pass.

## Thank you for your contributions!
