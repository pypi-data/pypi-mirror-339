import socket
import threading
from typing import List

def scan_port(ip: str, port: int, open_ports: List[int], timeout: float = 1.0) -> None:
    """Scan a single port and append to open_ports if it's open."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    if result == 0:  # Port is open
        open_ports.append(port)
    sock.close()

def scan_ports(ip: str, start_port: int = 1, end_port: int = 1024, timeout: float = 1.0) -> List[int]:
    """
    Scan a range of ports on the given IP address.
    
    Args:
        ip (str): The IP address to scan (e.g., '192.168.1.1').
        start_port (int): Starting port number (default: 1).
        end_port (int): Ending port number (default: 1024).
        timeout (float): Timeout for each connection attempt in seconds (default: 1.0).
    
    Returns:
        List[int]: List of open ports.
    """
    open_ports = []
    threads = []

    # Validate IP
    try:
        socket.inet_aton(ip)
    except socket.error:
        raise ValueError(f"Invalid IP address: {ip}")

    # Scan ports using threads for speed
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports, timeout))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return sorted(open_ports)