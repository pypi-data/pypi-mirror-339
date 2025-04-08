from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from colorama import Fore
import subprocess

from htbrecon import state
from .nmap import GO_BACK

GOBUSTER = "Gobuster"

COMMON = "Common"
MEDIUM = "Medium"
LARGE = "Large"

def gobuster_menu():
    return inquirer.select(
        message="What would you like to do?",
        choices=[
            Choice(value=COMMON, name="🔎 Common wordlist"),
            Choice(value=MEDIUM, name="📦 Medium wordlist"),
            Choice(value=LARGE, name="💣 Large wordlist"),
            Choice(value=GO_BACK, name="↩️  Go back"),
        ],
    ).execute()

def gobuster():
    while True:
        choice = gobuster_menu()

        if choice == COMMON:
            run_gobuster_scan(
                name="Common Scan",
                wordlist="/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt",
                output_file="gobuster_common.txt"
            )
        elif choice == MEDIUM:
            run_gobuster_scan(
                name="Medium Scan",
                wordlist="/usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-directories-lowercase.txt",
                output_file="gobuster_medium.txt"
            )
        elif choice == LARGE:
            run_gobuster_scan(
                name="Large Scan",
                wordlist="/usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-directories-lowercase.txt",
                output_file="gobuster_large.txt"
            )
        elif choice == GO_BACK:
            return

def run_gobuster_scan(name, wordlist, output_file):
    url = inquirer.text(message="Enter URL:").execute()
    ext = inquirer.text(message="Enter extension (optional, space-separated):").execute()

    params = ['gobuster', 'dir', '-u', url, '-w', wordlist, '-o', output_file]

    if ext:
        params.extend(['-x', ext])  # Correct usage of -x for extensions

    print(Fore.GREEN + f"Running {name.lower()} on {url}")
    process = subprocess.Popen(params, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    state.processes.append({
        "name": name,
        "process": process
    })