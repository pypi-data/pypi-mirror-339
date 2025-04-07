# opscan/scanner.py

import socket
from concurrent.futures import ThreadPoolExecutor

open_ports = []

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    except:
        pass

def scan_all_ports(ip):
    print(f"Scanning {ip} for open ports (0–65535)...\n")
    with ThreadPoolExecutor(max_workers=1000) as executor:
        for port in range(0, 65536):
            executor.submit(scan_port, ip, port)
    open_ports.sort()
    return open_ports
