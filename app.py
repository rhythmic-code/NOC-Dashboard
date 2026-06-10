import subprocess
import socket
import platform
from concurrent.futures import ThreadPoolExecutor
from scapy.all import sniff


# ==========================
# DEVICE DISCOVERY
# ==========================

def ping_host(ip):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "300", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            return ip

    except:
        pass

    return None


def device_discovery():

    subnet = input(
        "Enter subnet (example: 192.168.1): "
    )

    print("\nScanning network...\n")

    active_hosts = []

    with ThreadPoolExecutor(max_workers=100) as executor:

        futures = [
            executor.submit(
                ping_host,
                f"{subnet}.{i}"
            )
            for i in range(1, 255)
        ]

        for future in futures:
            host = future.result()

            if host:
                try:
                    hostname = socket.gethostbyaddr(host)[0]
                except:
                    hostname = "Unknown"

                active_hosts.append(
                    [host, hostname]
                )

    print("\nActive Devices\n")

    for ip, hostname in active_hosts:
        print(f"{ip:15} {hostname}")


# ==========================
# ROUTING TABLE
# ==========================

def routing_table():

    print("\nRouting Table Analysis\n")

    try:
        output = subprocess.check_output(
            ["route", "print"],
            text=True
        )

        print(output)

    except Exception as e:
        print("Error:", e)


# ==========================
# DNS CONFIGURATION
# ==========================

def dns_configuration():

    print("\nDNS Configuration\n")

    try:
        output = subprocess.check_output(
            ["ipconfig", "/all"],
            text=True
        )

        capture = False

        for line in output.splitlines():

            if "DNS Servers" in line:
                capture = True
                print(line.strip())

            elif capture:

                if line.startswith(" "):
                    print(line.strip())

                else:
                    break

    except Exception as e:
        print("Error:", e)


# ==========================
# CONNECTIVITY TEST
# ==========================

def connectivity_test():

    host = input(
        "Enter host/IP (default 8.8.8.8): "
    )

    if not host:
        host = "8.8.8.8"

    print()

    result = subprocess.run(
        ["ping", "-n", "4", host],
        text=True
    )


# ==========================
# WINDOWS FIREWALL
# ==========================

def show_firewall_rules():

    print("\nFirewall Rules\n")

    try:
        output = subprocess.check_output(
            [
                "netsh",
                "advfirewall",
                "firewall",
                "show",
                "rule",
                "name=all"
            ],
            text=True
        )

        print(output[:5000])

    except Exception as e:
        print("Error:", e)


def block_ip():

    ip = input("Enter IP to block: ")

    rule_name = f"Block_{ip}"

    try:
        subprocess.run(
            [
                "netsh",
                "advfirewall",
                "firewall",
                "add",
                "rule",
                f"name={rule_name}",
                "dir=in",
                "action=block",
                f"remoteip={ip}"
            ]
        )

        print("Rule added successfully.")

    except Exception as e:
        print("Error:", e)


# ==========================
# PACKET INSPECTION
# ==========================

def packet_callback(packet):

    protocol = "OTHER"

    if packet.haslayer("TCP"):
        protocol = "TCP"

    elif packet.haslayer("UDP"):
        protocol = "UDP"

    elif packet.haslayer("ICMP"):
        protocol = "ICMP"

    print(packet.summary())


def packet_inspection():

    print("\nCapturing 20 packets...\n")

    try:
        sniff(
            prn=packet_callback,
            count=20,
            store=False
        )

    except Exception as e:
        print("Error:", e)
        print("Install Npcap and run as Administrator.")


# ==========================
# MENU
# ==========================

def menu():

    while True:

        print("""
==================================
 MINI NOC DASHBOARD (WINDOWS)
==================================

1. Device Discovery
2. Routing Table Analysis
3. DNS Configuration
4. Connectivity Test
5. Show Firewall Rules
6. Block IP Address
7. Packet Inspection
8. Exit

==================================
""")

        choice = input("Select option: ")

        if choice == "1":
            device_discovery()

        elif choice == "2":
            routing_table()

        elif choice == "3":
            dns_configuration()

        elif choice == "4":
            connectivity_test()

        elif choice == "5":
            show_firewall_rules()

        elif choice == "6":
            block_ip()

        elif choice == "7":
            packet_inspection()

        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()