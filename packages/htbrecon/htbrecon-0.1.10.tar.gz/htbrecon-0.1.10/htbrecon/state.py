processes = []
from colorama import init, Fore, Style
STATUS  = "Status"



def check_status(quiet=False):
    global processes
    if not processes:
        print(Fore.GREEN + "Nothing running here.")
        return

    for proc in processes:
        running = proc["process"].poll() is None
        proc_name = proc["name"]
        color = Fore.YELLOW if running else Fore.GREEN

        human_readable = "finished" if not running else "running"
        if quiet:
            continue
        print(color + f"{proc_name} is {human_readable}")

    processes = [p for p in processes if p["process"].poll() is None]
