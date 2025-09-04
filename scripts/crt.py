import requests
from urllib.parse import urlparse
import json
from colorama import init,Fore

init(autoreset=True)

red = Fore.RED

def main(domain):
    subdomains = set()
    try:
        if not domain.startswith(("https://", "http://")):
            url = f"https://crt.sh/?q={domain}&output=json"
            response = requests.get(url, timeout=(15, 120))
            data = response.json()
            if data:
                for subdomain in data:
                    subdomains.add(subdomain["common_name"])
            else:
                print(red+"[!] NO DATA FOUND")
                exit()
        else:
            domainParse = urlparse(domain)
            domain = domainParse.netloc
            url = f"https://crt.sh/?q={domain}&output=json"
            response = requests.get(url, timeout=(15, 120))
            data = response.json()
            if data:
                for subdomain in data:
                    subdomains.add(subdomain["common_name"])
            else:
                print(red+"[!] NO DATA FOUND")
                exit()
    except Exception as e:
        print(f"{red}[!] Has been a error: {e}")
        exit()
    with open("crt_subdomains.txt", 'a') as file:
        for subdomain in subdomains:
            if subdomain:
                file.write(subdomain+"\n")