import asyncio
import aiohttp
import random
from colorama import Fore, init
from scripts.useragent.user_agent import _useragent_list

init()

rd = Fore.RED
reset = Fore.RESET
g = Fore.GREEN

corsFound = []

async def scan_cors(url, session):
    urlMal = "http://evil.com"
    headers = {
        "Origin":urlMal,
        "User-Agent":random.choice(_useragent_list)
    }
    url = url.strip()
    try:
        async with session.get(url, headers=headers) as resp:
            header_result = resp.headers.get("Access-Control-Allow-Origin")
            header_result2 = resp.headers.get("Access-Control-Allow-Credentials")
            if header_result == urlMal:
                if header_result2 and header_result2.lower() == "true":
                    print(f"\n            {g}C O R S - S C A N\n{rd}+ {g}{url}\n{rd}+{g} Reflected Origin And Credentials Access Control Is True\n{rd}+{g} Critical{reset}\n")
                else:
                    print(f"\n            {g}C O R S - S C A N\n{rd}+ {g}{url}\n{rd}+{g} Reflected Origin\n{rd}+{g} Hight{reset}\n")
                corsFound.append(url)
            else:
                pass
    except Exception:
        pass
async def main(file):
    with open(file, 'r') as rf:
        urls = rf.readlines()
    async with aiohttp.ClientSession() as session:
        task = [scan_cors(url, session) for url in urls]
        await asyncio.gather(*task)
        print(f"\n{g}[+] {len(corsFound)} Cors vulnerability found{reset}\n")