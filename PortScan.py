import concurrent.futures
import pyfiglet
import socket
from datetime import datetime
import time
import dns.resolver
import dns.reversename
import subprocess

def print_banner():
    # Print the ASCII art banner
    ascii_banner = pyfiglet.figlet_format("PortSCAN   ^_^")
    print(ascii_banner)
    print()

def ping_host(target):
    # Ping the target host to check if it is up
    command = ["ping", "-c", "1", "-W", "1", target]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return process.returncode == 0

def get_service_name(port):
    # Get the service name associated with the given port
    try:
        service_name = socket.getservbyport(port)
    except:
        service_name = "Unknown"
    return service_name

def reverse_dns_lookup(ip_address):
    # Perform reverse DNS lookup to get the domain name associated with the IP address
    resolver = dns.resolver.Resolver()
    domain_name = str(resolver.resolve(dns.reversename.from_address(ip_address), "PTR")[0])
    return domain_name

def scan_port(target, port):
    # Scan a specific port on the target host
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    sock.close()
    return port if result == 0 else None

def scan_ports(target, start_port, end_port):
    open_ports = []
    print(f"Scanning target: {target}")
    print()
    print(f"Pinging host...")

    if not ping_host(target):
        print("Host is down.")
        return

    print("Host is up. Starting port scanning...")
    print()
    print(f"Scanning started at: {datetime.now()}")
    print()
    print("-" * 50)

    animation = "|/-\\"
    animation_index = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        port_range = range(start_port, end_port + 1)
        futures = [executor.submit(scan_port, target, port) for port in port_range]
            
        while any(not future.done() for future in futures):
            print(f"Scanning... {animation[animation_index % len(animation)]}", end="\r")
            animation_index += 1
            time.sleep(0.1)

        for future in concurrent.futures.as_completed(futures):
            try:
                open_port = future.result()
                if open_port:
                    open_ports.append(open_port)
                    service_name = get_service_name(open_port)
                    domain_name = reverse_dns_lookup(target)
                    print(f"Port {open_port:<6} OPEN {' ' * 5} {service_name} (Domain: {domain_name})")
            except Exception as e:
                print(f"Error scanning port: {e}")

        print()
        print("-" * 50)
        print()
        print(f"Scanning finished at: {datetime.now()}")
        
        if len(open_ports) > 0:
            print("Open ports:")
            for i, port in enumerate(open_ports, start=1):
                print(f"{i}) Port {port}")
            print()
            print("\nHappy hacking! 🎉")
            save_result = input("Would you like to save the results to a file? (y/n): ")
        else:
            print("No open ports found")

        if save_result == "y":
            file_name = input("Enter the file name: ")
            with open(file_name, "w") as file:
                for port in open_ports:
                    file.write(f"Port {port}\n")

            print("File saved successfully!")
        else:
            print("Sure, thank you")

def main():
    print_banner()
    target = input("Enter the target hostname or IP address: ")
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))

    scan_ports(target, start_port, end_port)

if __name__ == '__main__':
    main()
