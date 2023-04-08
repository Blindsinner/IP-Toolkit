import ipaddress
import socket
import tkinter as tk
from tkinter import messagebox

import ipaddress

def binary_to_ip(binary_ip):
    # Remove dots from the input string
    binary_ip = binary_ip.replace('.', '')
    # Split the binary string into 4 octets
    octets = [binary_ip[i:i+8] for i in range(0, len(binary_ip), 8)]
    # Convert each octet to decimal and join with dots to form IP address
    if len(octets) == 4: # IPv4
        return '.'.join(str(int(octet, 2)) for octet in octets)
    elif len(octets) == 8: # IPv6
        return ':'.join([octet.lstrip('0') or '0' for octet in octets]).replace(':0:', '::', 1)

def ip_to_binary(ip_address):
    ip = ipaddress.ip_address(ip_address)
    if ip.version == 4:
        binary_ip = bin(int(ip))[2:].zfill(32)
        return ".".join([binary_ip[i:i+8] for i in range(0, 32, 8)])
    elif ip.version == 6:
        binary_ip = bin(int(ip))[2:].zfill(128)
        return ":".join([binary_ip[i:i+16] for i in range(0, 128, 16)])


def ip_to_binary(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        if isinstance(ip, ipaddress.IPv4Address):
            binary_ip = bin(int(ip))[2:]
            binary_ip = binary_ip.rjust(32, '0')
            return ".".join([binary_ip[i:i+8] for i in range(0, 32, 8)])
        elif isinstance(ip, ipaddress.IPv6Address):
            binary_ip = bin(int(ip))[2:]
            binary_ip = binary_ip.rjust(128, '0')
            return ":".join([binary_ip[i:i+16] for i in range(0, 128, 16)])
    except ValueError:
        return "Error: Invalid IP address."

def network_address(ip, prefix_or_mask):
    try:
        ip = ip.strip()
        prefix_or_mask = prefix_or_mask.strip()

        # Detect IP version
        ip_obj = ipaddress.ip_address(ip)
        ip_version = ip_obj.version

        if ip_version == 4:
            if '.' in prefix_or_mask:
                mask = ipaddress.IPv4Address(prefix_or_mask)
                prefix_length = ipaddress.ip_network(f'0.0.0.0/{mask}').prefixlen
            else:
                prefix_length = int(prefix_or_mask)
            ip_interface = ipaddress.IPv4Interface(f"{ip}/{prefix_length}")
        elif ip_version == 6:
            if ':' in prefix_or_mask:
                mask = ipaddress.IPv6Address(prefix_or_mask)
                prefix_length = ipaddress.ip_network('::/' + str(mask)).prefixlen
            else:
                prefix_length = int(prefix_or_mask)
            ip_interface = ipaddress.IPv6Interface(f"{ip}/{prefix_length}")

        network_address = ip_interface.network.network_address
        return network_address.exploded
    except ValueError as ve:
        return f"Error: {ve}"



def cidr_to_subnet_mask(ip_address, cidr):
    binary_mask = '1' * cidr + '0' * (32 - cidr)
    octets = [binary_mask[i:i+8] for i in range(0, 32, 8)]
    subnet_mask = '.'.join(str(int(octet, 2)) for octet in octets)
    return cidr, subnet_mask
def ipv4_to_ipv6(ipv4_address):
    ipv6_obj = ipaddress.IPv6Address('::ffff:' + ipv4_address)
    compressed = ipv6_obj.compressed
    expanded_shortened = ipv6_obj.exploded[:9] + ipv6_obj.exploded[25:]
    expanded = ipv6_obj.exploded
    return compressed, expanded_shortened, expanded

def ipv6_to_ipv4(ipv6_address):
    try:
        ipv6 = ipaddress.IPv6Address(ipv6_address)
        if ipv6.ipv4_mapped is not None:
            return ipv6.ipv4_mapped
        else:
            return "This is not an IPv4-mapped IPv6 address"
    except ipaddress.AddressValueError:
        return "Invalid IPv6 address"


def possible_subnets(ip_address, subnet_mask):
    try:
        ip = ipaddress.ip_interface(f"{ip_address}/{subnet_mask}")
        network = ipaddress.ip_network(ip.network)
        return network.num_addresses
    except ValueError:
        return "Error: Invalid IP address or subnet mask."

def ip_class_private_public(ip_address, cidr):
    try:
        ip = ipaddress.ip_address(ip_address)
        ip_class = ""
        if isinstance(ip, ipaddress.IPv4Address):
            net = ipaddress.IPv4Network(f"{ip_address}/{cidr}")
            first_octet = int(ip_address.split(".")[0])

            if net.prefixlen <= 8:
                ip_class = "Class A"
            elif net.prefixlen <= 16:
                ip_class = "Class B"
            elif net.prefixlen <= 24:
                ip_class = "Class C"
            elif net.prefixlen <= 32:
                ip_class = "Class D"

            if first_octet >= 224 and first_octet <= 239:
                ip_class = "Class D"
            elif first_octet >= 240 and first_octet <= 255:
                ip_class = "Class E"

            if net.is_private:
                return f"{ip_class}, Private"
            elif ip_class == "Class D":
                return f"{ip_class}, Multicast"
            elif ip_class == "Class E":
                return f"{ip_class}, Experimental"
            else:
                return f"{ip_class}, Public"
        elif isinstance(ip, ipaddress.IPv6Address):
            if ip.is_private:
                ip_class = "Unique Local Address (ULA)"
            else:
                ip_class = "Global Unicast Address"
            return ip_class
    except ValueError:
        return "Error: Invalid IP address or subnet mask."


def display_all_info(ip_address, cidr):
    try:
        ip_net = ipaddress.IPv4Network(f"{ip_address}/{cidr}", strict=False)
        network_address = str(ip_net.network_address)
        broadcast_address = str(ip_net.broadcast_address)
        first_ip = str(ip_net[1])
        last_ip = str(ip_net[-2])
        ip_range = f"{first_ip} - {last_ip}"
        total_hosts = ip_net.num_addresses
        usable_hosts = total_hosts - 2
        compressed, expanded_shortened, expanded = ipv4_to_ipv6(ip_address)
        output = {
            "IP Address": ip_address,
            "Subnet Mask": str(ip_net.netmask),
            "Wildcard Mask": str(ip_net.hostmask),
            "CIDR Notation": cidr,
            "Network Address": network_address,
            "Binary IP": ip_to_binary(ip_address),
            "Short": f"{ip_address}/{cidr}",
            "Binary Subnet Mask": ip_to_binary(str(ip_net.netmask)),
            "Integer ID": int(ipaddress.IPv4Address(ip_address)),
            "Hex ID": hex(int(ipaddress.IPv4Address(ip_address))),
            "Binary ID": bin(int(ipaddress.IPv4Address(ip_address)))[2:].zfill(32),
            "IP Class": ip_class_private_public(ip_address, cidr=cidr).split(',')[0],
            "IP Type": "Private" if ipaddress.IPv4Network(ip_address + '/' + str(cidr), strict=False).is_private else "Public",
            "Usable Host IP Range": ip_range,
            "Broadcast Address": broadcast_address,
            "Total Number of Hosts": total_hosts,
            "Number of Usable Hosts": usable_hosts,
            "in-addr.arpa": ".".join(reversed(ip_address.split("."))) + ".in-addr.arpa",
            "IPv4 Mapped Address": f"::ffff:{ip_address}",
            "6to4 Prefix": f"2002:{ip_address[:2].zfill(2)}{ip_address[3:5].zfill(2)}::{ip_address[6:8].zfill(2)}{ip_address[9:11].zfill(2)}/{cidr}",
            "IPv6 Compressed": compressed,
            "IPv6 Expanded (Shortened)": expanded_shortened,
            "IPv6 Expanded": expanded
        }
        return output
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as e:
        print(f"Error: {str(e)}")



def gui_main():
    options = [
        "Binary to IP address",
        "IP address to Binary",
        "Find Network Address from IP and Subnet Mask",
        "Convert IP and CIDR Notation to Subnet Mask",
        "Calculate Possible Subnetting from IP range",
        "Determine IP Class and Private/Public Status",
        "Convert IPv4 to IPv4-mapped IPv6",
        "Convert IPv4-mapped IPv6 to IPv4",
        "Display All Information for an IP Address and Subnet"
]

    def on_option_click(option):
        ip_label.grid_forget()
        ip_entry.grid_forget()
        subnet_label.grid_forget()
        subnet_entry.grid_forget()
        submit_button.grid_forget()

        if option == "Binary IP to IP address":
            ip_label.config(text="Binary IP:")
            subnet_label.grid_forget()
            subnet_entry.grid_forget()
        elif option == "IP address to Binary" or option == "Determine IP Class and Private/Public Status":
            ip_label.config(text="IP Address:")
            subnet_label.grid_forget()
            subnet_entry.grid_forget()
        else:
            ip_label.config(text="IP Address:")
            subnet_label.grid(row=len(options)+1, column=0, sticky="w", padx=5, pady=5)
            subnet_entry.grid(row=len(options)+1, column=1, padx=5, pady=5)
        if option == "Binary to IP address" or option == "Convert IPv4 to IPv4-mapped IPv6":
            ip_label.config(text="IP Address:")
            subnet_label.grid_forget()
            subnet_entry.grid_forget()
        elif option == "Convert IPv4-mapped IPv6 to IPv4":
            ip_label.config(text="IPv6 Address:")  # Change this line
            subnet_label.grid_forget()
            subnet_entry.grid_forget()


        ip_label.grid(row=len(options), column=0, sticky="w", padx=5, pady=5)
        ip_entry.grid(row=len(options), column=1, padx=5, pady=5)
        submit_button.grid(row=len(options), column=2, padx=5, pady=5)
        submit_button.grid(row=len(options)+1, column=2, padx=5, pady=5)

        submit_button.config(text="Submit", command=lambda: on_submit(option))



    def on_submit(option):
        ip_address = ip_entry.get()
        subnet_mask_or_cidr = subnet_entry.get()

        if option == "Binary IP to IP address":
            result = binary_to_ip(ip_address)
        elif option == "IP address to Binary":
            result = ip_to_binary(ip_address)
        elif option == "Find Network Address from IP and Subnet Mask":
            result = network_address(ip_address, subnet_mask_or_cidr)
        elif option == "Convert IP and CIDR Notation to Subnet Mask":
            result = cidr_to_subnet_mask(ip_address, int(subnet_mask_or_cidr))
        elif option == "Calculate Possible Subnetting from IP range":
            result = possible_subnets(ip_address, subnet_mask_or_cidr)
        elif option == "Determine IP Class and Private/Public Status":
            result = ip_class_private_public(ip_address)
        elif option == "Convert IPv4 to IPv4-mapped IPv6":
            compressed, expanded_shortened, expanded = ipv4_to_ipv6(ip_address)
            result = f"IPv6 Compressed: {compressed}\nIPv6 Expanded (Shortened): {expanded_shortened}\nIPv6 Expanded: {expanded}"
        elif option == "Convert IPv4-mapped IPv6 to IPv4":
            try:
                result = ipv6_to_ipv4(ip_address)
            except ValueError as e:
                result = str(e)
        elif option == "Display All Information for an IP Address and Subnet":
            output = display_all_info(ip_address, subnet_mask_or_cidr)
            if output is None:
                result = "Error: invalid input"
            else:
                result = '\n'.join(f"{k}: {v}" for k, v in output.items())

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"{option}:\n{result}")


    root = tk.Tk()
    root.title("IP Toolkit")

    ip_label = tk.Label(root)
    ip_entry = tk.Entry(root)

    subnet_label = tk.Label(root, text="Subnet Mask / CIDR:")
    subnet_entry = tk.Entry(root)

    submit_button = tk.Button(root)

    options = options = [
        "Binary to IP address",
        "IP address to Binary",
        "Find Network Address from IP and Subnet Mask",
        "Convert IP and CIDR Notation to Subnet Mask",
        "Calculate Possible Subnetting from IP range",
        "Determine IP Class and Private/Public Status",
        "Convert IPv4 to IPv4-mapped IPv6",
        "Convert IPv4-mapped IPv6 to IPv4",
        "Display All Information for an IP Address and Subnet"
]

    for idx, option in enumerate(options, start=0):
        button = tk.Button(root, text=option, command=lambda opt=option: on_option_click(opt))
        button.grid(row=idx, column=0, columnspan=2, pady=2)

    output_label = tk.Label(root, text="Output:")
    output_label.grid(row=len(options) + 2, column=0, sticky="w", padx=5, pady=5)

    output_text = tk.Text(root, wrap=tk.WORD, width=40, height=10)
    output_text.grid(row=len(options) + 2, column=1, padx=5, pady=5)

    scrollbar = tk.Scrollbar(root, command=output_text.yview)
    scrollbar.grid(row=len(options) + 2, column=2, sticky='nsew')
    output_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__ == "__main__":
    gui_main()