import asyncio
import aiohttp
from colorama import init, Fore

init()
g = Fore.GREEN
reset = Fore.RESET

async def status_probe(url, session):
    try:
        url = url.strip()
        async with session.get(url) as url_response:
            if url_response.status == 200:
                print(f"{g}[200] {url}{reset}")
            else:
                pass
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