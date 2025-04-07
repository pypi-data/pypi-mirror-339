# opscan/__main__.py

import sys
from opscan.scanner import scan_all_ports

def main():
    if len(sys.argv) != 2:
        print("Usage: opscan <ip-address>")
        sys.exit(1)

    ip = sys.argv[1]
    open_ports = scan_all_ports(ip)

    if open_ports:
        print("\n✅ Open ports found:")
        for port in open_ports:
            print(f"  🔓 Port {port}")
    else:
        print("\n❌ No open ports found.")

if __name__ == "__main__":
    main()
