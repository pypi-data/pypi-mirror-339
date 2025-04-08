from htbrecon import state
from htbrecon.tools.nmap import nmap

from openai import OpenAI

def ai():
    print("Creating openai client....")
    client = OpenAI()
    print("Processing HTB recon with LLM")

    nmap(ask_once=True)
    print("Running NMAP scan...")

    while True:
        state.check_status(quiet=True)

        if not state.processes:
            print("Finished")
            break


    with open("specific_port_scan.txt", "r") as f:
        nmap_data =  f.read()

    prompt = """Hello, you'll be my personal HTB recon friend and analyzer. I'll give you the NMAP scan results for a machine. Please analyze the data and provide me a list of commands I should use for further recon. Your responses should be in the JSON format.
    Exmaple:
    {
        "analysis": "<YOUR_ANALYSIS>",
        "commands": [
            {
                "name": "gobuster",
                "args": ["dir", "-u", "http://<TARGET_IP>:8080"]
            },
            {
                "name": "gobuster",
                "args": ["vhost", "-u", "http://<TARGET_IP>:8080"]
            }
        ]
    }
    Here are my paths for the wordlists:
    /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-directories-lowercase.txt
    /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
    Here is your NMAP data:
    """ + nmap_data
    response = client.responses.create(model="gpt-3.5-turbo", input=prompt)
    print(response.output_text)

