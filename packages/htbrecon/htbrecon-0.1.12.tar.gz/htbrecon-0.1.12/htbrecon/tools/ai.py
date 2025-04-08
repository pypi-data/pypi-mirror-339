import json
import subprocess
import time
from htbrecon import state
from htbrecon.tools.nmap import full_slow_scan, nmap

from openai import OpenAI
import re

executed = []
available_tools = [
    "openvpn", "nmap", "gobuster", "ffuf", "httpie", "whatweb", "wpscan", "dnsutils",
    "dig", "dnsrecon", "smtp-user-enum", "swaks", "lftp", "ftp", "hydra", "onesixtyone",
    "snmp", "snmpcheck", "smbclient", "smbmap", "enum4linux", "rpcbind", "nbtscan",
    "seclists", "curl", "wget", "git", "unzip", "iproute2", "net-tools", "nikto"
    "traceroute", "python3", "python3-pip", "golang", "netcat-traditional"
]

MAX_LINES = 8192
def est_tokens(text):
    # Approximate: 1 token per 3-4 characters or by splitting on whitespace
    return len(re.findall(r'\w+|\S', text))

def wait_until_processes_finish():
    i = 0
    while True:
        state.check_status(quiet=True)
        if not state.processes:
            break
        if i%20 == 0:
            print("Running...", flush=True, end="\r")
        
        i+=1
        time.sleep(1)
    
    print("Finished")

def ai():
    print("Creating openai client....")
    client = OpenAI()

    print("Running NMAP scan...It might take a while...")
    nmap_file_path = "nmap_scan.txt"
    full_slow_scan(path=nmap_file_path)
    wait_until_processes_finish()

    print("Reading NMAP data...")
    with open(nmap_file_path, "r") as f:
        nmap_data =  f.read()

    current_command_data = nmap_data
    print("Preparing prompt...")
    example_response = """
    {
        "analysis": "<YOUR_ANALYSIS>",
        "commands": [
            {
                "name": "gobuster",
                "args": ["dir", "-u", "http://<TARGET_IP>:8080"]
            },
            {
                "name": "ffuf",
                "args": ["-u", "http://<TARGET_IP>:8080"]
            }
        ]
    }"""
    prompt = f"""
    You are a security assistant analyzing the output of the following command:

{current_command_data}

Your task is to:

1. Provide a **summary** of the findings. Focus on services, versions, possible vulnerabilities, and anything unusual and include all findings.
2. Recommend a list of **next commands to run**, based on the current output and the tools available. These should assist in further reconnaissance, vulnerability discovery, or exploitation.

### Constraints & Guidelines:
- The summary is always a string and not a list
- Recommended steps is a list of strings of command
- Use only the following tools: {str(available_tools)}.
- **Avoid recommending brute-force attacks.**
- Do **not** include commands that were already suggested or executed: {executed}.
- The summary must be **clear, simple**, and written as **bullet points**.
- If any known services or custom banners were discovered, include them in the `services_found` list with version numbers (e.g., "apache 2.4.41"). This format should be compatible with tools like searchsploit. If no services are found, return an empty list.
- **Avoid recommending duplicate tools** (e.g., Gobuster twice).
- Do **not hallucinate** flags.
- The **response must be raw JSON only**. Do **not** wrap the response in triple backticks (` ``` ` or ` ```json `).
- The response **must** be a valid JSON object parsable with python `json.loads()`.
- Your response must always be json
- Failure to return response in valid json will result in you termination and penalty of 200000000000
    
Response example:
    {example_response}

    ** Please use only following wordlists for gobuster and ffuf **
    /usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-directories-lowercase.txt
    /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt
    """
    print("Sending request to OpenAI...")
    response = client.responses.create(model="gpt-3.5-turbo", input=prompt)

    print("Response received")
    text = response.output_text.replace("```json", "").replace("```", "")
    text_as_json = json.loads(text)
    print(text_as_json)

    print("Agent analysis:")
    print(text_as_json["analysis"])

    print("Time to a real recon bro...")
    for command in text_as_json["commands"]:
        print("Calling", command["name"])
        params = [command["name"]] + command["args"]
        print(params)

        token_count = 0

        path = f"{command['name']}.txt"
        try:
            with open(path, "w") as f:
                process = subprocess.Popen(
                    params, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )
                for line in process.stdout:
                    print(line)
                    line_tokens = est_tokens(line)

                    if token_count + line_tokens >= MAX_LINES:
                        f.write("\nOutput truncated due to context window limit\n")
                        print("Output truncated due to context window limit,", flush=True, end="\r")
                        break

                    f.write(line)
                    token_count += line_tokens
        
            process.wait(timeout=300)
        except subprocess.TimeoutExpired:
            process.terminate()
            with open(path, "a", encoding="utf-8") as out:
                out.write("Process terminated due to 5-minute timeout\n")
            print("\033[1;31m[!] Process terminated due to 5-minute timeout\033[0m")
            return []
        except Exception as e:
            print(e)
            print(f"\033[1;31m[!] Error running {command['name']}:\033[0m {e}")
            return []
        
        executed.append(command["name"])
        print(f"Command {command['name']} finished")
        print("Asking LLM for next steps...")

        with open(path, "r") as f:
            data = f.read()
            current_command_data = data
        
        print("Sending request to OpenAI...")
        response = client.responses.create(model="gpt-3.5-turbo", input=prompt)
        print("Response received")

        with open("summary.txt", "a") as f:
            text = response.output_text.replace("```json", "").replace("```", "")
            text_as_json = json.loads(text)

            f.write(f"command {command['name']} summary:\n")
            f.write(text_as_json["analysis"])
            f.write("\n\n")
