import asyncio
import aiohttp
import random
from scripts.useragent.user_agent import _useragent_list
from colorama import init, Fore
init(autoreset=True)

r = Fore.RED
g = Fore.GREEN
c = Fore.CYAN
y = Fore.YELLOW


banner = f"""{r}
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  _   _           _     _   _                _             _____      _           _   _               ║
║ | | | |         | |   | | | |              | |           |_   _|    (_)         | | (_)              ║
║ | |_| | ___  ___| |_  | |_| | ___  __ _  __| | ___ _ __    | | _ __  _  ___  ___| |_ _  ___  _ __    ║
║ |  _  |/ _ \/ __| __| |  _  |/ _ \/ _` |/ _` |/ _ \ '__|   | || '_ \| |/ _ \/ __| __| |/ _ \| '_ \   ║
║ | | | | (_) \__ \ |_  | | | |  __/ (_| | (_| |  __/ |     _| || | | | |  __/ (__| |_| | (_) | | | |  ║
║ \_| |_/\___/|___/\__| \_| |_/\___|\__,_|\__,_|\___|_|     \___/_| |_| |\___|\___|\__|_|\___/|_| |_|  ║
║                                                                   _/ |                               ║
║                                                                  |__/                                ║
║                                {y}[1] Scan Single URL{r}                                                   ║
║                                {y}[2] Scan multiples URLs{r}                                               ║
║                                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""


listHeaders = [
        "Host",
        "X-Forwarded-Host",
        "X-Host",
        "X-Forwarded-Server",
        "X-Http-Host-Override",
        "X-Rewrite-Url",
        "X-Original-Url"
]

sem = asyncio.Semaphore(100)

async def scan_hhi(url, session):
    try:
        async with session.get(url) as response_original:
            content_original = await response_original.text()
    except Exception:
        pass
    for header in listHeaders:
        headers = {
                    header:"evil.com",
                    "User-Agent":random.choice(_useragent_list)
            }
        
        try:
            async with sem:
                async with session.get(url, headers=headers, timeout=10) as response:
                    headersResponse = response.headers
                    htmlResponse = await response.text()
                    if response.status in [200, 301, 302, 307, 308]:
                        if content_original != htmlResponse:
                            if "evil.com" in htmlResponse or "evil.com" in str(headersResponse):
                                banner2 = f"""{c}
        {g}╔════════════════════════════════════╗
        ║  {r}Host Header Injection Detected{g}    ║
        ╚════════════════════════════════════╝
        ┌──[{g}Target URL{c}─────────────────────────────────┐
        {url}
        │──[{g}Header Vulnerable]{c}──────────────────────────┐
        {header}
        │──[{g}Response Details]{c}───────────────────────────┐
        {response.status}
                            """
                                print(banner2)
                            else:
                                pass
                        else:
                            pass
        except Exception:
            pass
async def main():
    async with aiohttp.ClientSession() as session:
        print(banner)
        try:
            op = int(input(f"{g}[$] Select an option (1-2): "))
        except ValueError:
            print(f"{r}[x] Value incorrect. Numbers must be used (1-2)")
            exit()
        

        if op == 1:
            url = input("[~] URL: ")
            await scan_hhi(url.strip(), session)
        elif op == 2:
            task = []
            listaUrls = input("[~] Path: ")
            with open(listaUrls, 'r') as urlss:
                urls = urlss.readlines()
            for url in urls:
                task.append(scan_hhi(url, session))
            await asyncio.gather(*task)