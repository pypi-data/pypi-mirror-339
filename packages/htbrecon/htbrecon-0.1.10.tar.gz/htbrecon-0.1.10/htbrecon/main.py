from InquirerPy import prompt, inquirer
from InquirerPy.base import Choice
from colorama import init, Fore
import sys
from htbrecon import banner
from htbrecon.tools import ai
from htbrecon.tools.gobuster import GOBUSTER, gobuster

from htbrecon.tools.hosts import add_to_etc_hosts, ADD_ETC_HOSTS
from htbrecon.tools.nmap import nmap, NMAP
from htbrecon import state
from htbrecon.tools.subdomains import SUBDOMAINS, subdomains

init(autoreset=True)

AI = "AI"
CONFIGURE = 'Configure'
EXIT = "Exit"
def main_menu():
    choice = inquirer.select(
        message="What do you want to do?",
        choices=[
            Choice(value=state.STATUS, name="🔍 Check Status"),
            Choice(value=AI, name="🤖 AI (Use LLM for your reconnaissance)"),
            Choice(value=ADD_ETC_HOSTS, name="✍️  Add to /etc/hosts"),
            Choice(value=NMAP, name="🛰️  Run Nmap Scan"),
            Choice(value=GOBUSTER, name="🪓 Gobuster"),
            Choice(value=SUBDOMAINS, name="🌐 Subdomain Finder"),
            Choice(value=EXIT, name="❌ Exit"),
        ],
    ).execute()
    return choice

def run():
    banner.display()
    while True:
        try:
            choice = main_menu()
            if choice == ADD_ETC_HOSTS:
                add_to_etc_hosts()
            if choice == NMAP:
                nmap()
            if choice == state.STATUS:
                state.check_status()
            if choice == GOBUSTER:
                gobuster()
            if choice == SUBDOMAINS:
                subdomains()
            if choice == AI:
                ai.ai()
            elif choice == 'Exit':
                print(Fore.RED + 'Exiting. Goodbye!')
                sys.exit()
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")





if __name__ == '__main__':
    run()