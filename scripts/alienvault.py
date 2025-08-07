import requests
from colorama import Fore, init
from urllib.parse import urlparse

init()

yellow = Fore.YELLOW
red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
reset = Fore.RESET


def main():
    url = input(f"{green}[ URL ]$~ {reset}")
    urlAlienvault = f"https://otx.alienvault.com/api/v1/indicators/domain/{url}/url_list?limit=500"

    if not url.startswith(("https://", "http://")):
        url_new = "http://"+url

    parseUrl = urlparse(url_new)
    dominio = parseUrl.netloc
    response = requests.get(urlAlienvault, timeout=10)
    print(yellow+"\n"+response.text+"\n"+reset)

    while True:
        try:
            page = int(input(f"{cyan}[ PAGE ]$~ {reset}"))
        except ValueError:
            print(f"{red}[ ERROR ] Valor erroneo: solo se admiten números enteros.{reset}")
            break
        urlAlienvault = f"https://otx.alienvault.com/api/v1/indicators/domain/{url}/url_list?limit=500&page={page}"
        response = requests.get(urlAlienvault, timeout=10)
        print(yellow+"\n"+response.text+"\n"+reset)

        save = input("You wanna save the content? yes/no: ")
        if save.lower() == "yes":
            with open(f"../{dominio}{page}.txt", 'w') as file:
                file.write(response.text)
            print("")
        elif save.lower() == "no":
            print("")
            continue
        else:
            print(f"{red}[x] Incorrect.{reset}")
            print("")