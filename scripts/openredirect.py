from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import asyncio
import aiohttp
import random
from scripts.useragent.user_agent import _useragent_list
from colorama import init, Fore

init()
green = Fore.GREEN
reset = Fore.RESET

urlPayload = "https://www.google.com"

async def redirectx(url, session):
    header = {"User-Agent":random.choice(_useragent_list)}
    try:
        async with session.get(url, allow_redirects=True, header=header) as response2:
            response2 = str(response2.url)
            if response2.startswith(urlPayload):
                print(f"{green}[ VULNERABLLE ] {url}{reset}")
            else:
                pass
    except Exception:
        pass

async def main(file):
    task = []
    with open(file, 'r') as rf:
        urls = rf.readlines()
    async with aiohttp.ClientSession() as session:
        for url in urls:
            if "=" in url:
                urlp = urlparse(url)
                query = parse_qs(urlp.query)
                for key in query:
                    query[key] = [urlPayload]
                    new_query = urlencode(query, doseq=True)
                    new_url = urlunparse(urlp._replace(query=new_query))
                    task.append(redirectx(new_url, session))
        await asyncio.gather(*task)