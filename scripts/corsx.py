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
BLACKLIST_STATUS_CODES = [
    204,  # No Content
    301, 302, 303, 307, 308,  # Redirecciones
    400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 418, 422, 429, 431, 451,  # Client errors
    500, 501, 502, 503, 504, 505, 511  # Server errors
]
async def scan_cors(url, session):
    urlMal = "evil.com"
    headers = {
        "Origin": urlMal,
        "User-Agent": random.choice(_useragent_list)
    }
    url = url.strip()
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status in BLACKLIST_STATUS_CODES:
                return

            header_result = resp.headers.get("Access-Control-Allow-Origin")
            header_result2 = resp.headers.get("Access-Control-Allow-Credentials")

            if header_result == urlMal:
                if header_result2 and header_result2.lower() == "true":
                    print(f"""\n            {g}C O R S - S C A N\n{rd}+ {g}{url}\n{rd}+{g} Reflected Origin and Credentials Access Control is True\n{rd}+{g} Critical{reset}\n""")
                    corsFound.append(url)
                else:
                    print(f"""\n            {g}C O R S - S C A N\n{rd}+ {g}{url}\n{rd}+{g} Reflected Origin \n{rd}+{g} Hight{reset}\n""")
                    corsFound.append(url)
            elif header_result == "*":
                if header_result2 and header_result2.lower() == "true":
                    print(f"""\n            {g}C O R S - S C A N\n{rd}+ {g}{url}\n{rd}+{g} Reflected * And Credentials Access Control is True \n{rd}+{g} WARNING {reset}\n""")
                    corsFound.append(url)
                else:
                    print(f"""\n            {g}C O R S - S C A N\n{rd}+ {g}{url}\n{rd}+{g} Reflected *\n{rd}+{g} Hight{reset}\n""")
                    corsFound.append(url)
            else:
                pass
    except Exception:
        pass

async def main(file):
    with open(file, 'r') as rf:
        urls = rf.readlines()
    async with aiohttp.ClientSession() as session:
        tasks = [scan_cors(url, session) for url in urls]
        await asyncio.gather(*tasks)
        print(f"\n{g}[+] {len(corsFound)} CORS vulnerabilities found{reset}\n")
