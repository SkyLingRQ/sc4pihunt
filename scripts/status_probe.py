import asyncio
import aiohttp
from colorama import init, Fore

init()
rd = Fore.RED
g = Fore.GREEN
yellow = Fore.YELLOW
reset = Fore.RESET

urlLive = []

async def status_probe(url, session):
    try:
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        async with session.get(url) as url_response:
            if url_response.status == 200:
                print(f"{g}[200] {url}{reset}")
                urlLive.append(url)
            else:
                print(f"{yellow}[{url_response.status}] {url}{reset}")
    except Exception:
        pass

async def main(file):
    try:
        with open(file, 'r') as rf:
            urls = rf.readlines()
    except Exception:
        print("[x] No se pudo leer el archivo")
        exit()
    async with aiohttp.ClientSession() as session:
        task = [status_probe(url, session) for url in urls]
        await asyncio.gather(*task)
    

    if urlLive:
        with open("subdomains_live.txt", 'a') as live:
            for urll in urlLive:
                live.write(urll+"\n")
