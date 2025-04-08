import ipaddress
from colorama import init, Fore
from InquirerPy import inquirer

ADD_ETC_HOSTS = "Add to /etc/hosts"

def add_to_etc_hosts():
    ip = inquirer.text(message="Enter IP address:").execute()
    domain = inquirer.text(message="Enter domain name:").execute()

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(Fore.RED + f"Invalid IP address: {ip}")
        return

    print(Fore.YELLOW + f"[*] Adding {ip} {domain} to /etc/hosts...")

    try:
        with open('/etc/hosts', 'r') as f:
            lines = f.readlines()
    except PermissionError:
        print(Fore.RED + "[!] Permission denied: run the tool with sudo to modify /etc/hosts.")
        return

    updated = False
    for i, line in enumerate(lines):
        if ip in line and domain in line:
            line = line.strip()
            print(Fore.YELLOW + f"[*] Entry already exists: {line}")
            return
        elif ip in line and domain not in line:
            print(Fore.YELLOW + f"[*] IP found with different domain: {line.strip()}")
            lines[i] = line.strip() + f" {domain}\n"
            updated = True
            break

    if not updated:
        lines.append(f"{ip} {domain}\n")

    try:
        with open('/etc/hosts', 'w') as f:
            f.writelines(lines)
        print(Fore.GREEN + f"[+] Added {ip} {domain} to /etc/hosts.")
    except PermissionError:
        print(Fore.RED + "[!] Permission denied while writing. Use sudo.")