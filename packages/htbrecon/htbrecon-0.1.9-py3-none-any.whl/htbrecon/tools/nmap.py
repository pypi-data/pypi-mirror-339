import ipaddress
import subprocess
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from colorama import init, Fore
from htbrecon import state

init(autoreset=True)

NMAP = "Nmap"

QUICK_SCAN = "Quick Scan"
FULL_SCAN = "Full Scan (fast)"
SPECIFIC_PORT_SCAN = "Specific Port Scan"
UDP_SCAN = "UDP Scan (slow)"
GO_BACK = "Go back"

NMAP_CHOICES = [
    Choice(value=QUICK_SCAN, name="⚡ Quick scan"),
    Choice(value=FULL_SCAN, name="📋 Full scan"),
    Choice(value=SPECIFIC_PORT_SCAN, name="🎯 Scan specific ports"),
    Choice(value=UDP_SCAN, name="🌐 UDP scan"),
    Choice(value=GO_BACK, name="↩️ Go back"),
]

def nmap_menu():
    return inquirer.select(
        message="What would you like to do?",
        choices=NMAP_CHOICES
    ).execute()

def nmap(ask_once=False):
    while True:
        choice = nmap_menu()

        if choice == QUICK_SCAN:
            quick_scan()
        elif choice == FULL_SCAN:
            full_scan()
        elif choice == SPECIFIC_PORT_SCAN:
            specific_port_scan()
        elif choice == UDP_SCAN:
            print(Fore.YELLOW + "UDP scan feature coming soon...")
        elif choice == GO_BACK:
            return
        
        if ask_once:
            break

def quick_scan():
    ip = inquirer.text(message="Enter IP:").execute()

    if not is_valid_ip(ip):
        print(Fore.RED + f"Invalid IP address: {ip}")
        return

    print(Fore.GREEN + f"Running quick scan on {ip}...")
    process = subprocess.Popen(
        ['nmap', '-sC', '-sV', '-oN', 'quick_scan.txt', ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    state.processes.append({
        "name": "Quick Scan",
        "process": process
    })

def full_scan():
    ip = inquirer.text(message="Enter IP:").execute()

    if not is_valid_ip(ip):
        print(Fore.RED + f"Invalid IP address: {ip}")
        return

    print(Fore.GREEN + f"Running full scan on {ip}...")
    process = subprocess.Popen(
        ['nmap', '-p-', '--min-rate=1000', '-oN', 'full_scan.txt', ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    state.processes.append({
        "name": "Full Scan",
        "process": process
    })

def specific_port_scan():
    ip = inquirer.text(message="Enter IP:").execute()
    ports = inquirer.text(message="Enter comma-separated ports:").execute()

    if not is_valid_ip(ip):
        print(Fore.RED + f"Invalid IP address: {ip}")
        return

    print(Fore.GREEN + f"Running specific ports scan on {ip}...")
    process = subprocess.Popen(
        ['nmap', '-sC', '-sV', '-p', ports, '-oN', 'specific_port_scan.txt', ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    state.processes.append({
        "name": "Specific Port Scan",
        "process": process
    })

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False