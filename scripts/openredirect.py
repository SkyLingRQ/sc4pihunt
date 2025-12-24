from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import asyncio
import aiohttp
import random
from scripts.useragent.user_agent import _useragent_list
from colorama import init, Fore

init()
green = Fore.GREEN
reset = Fore.RESET

payloads = [
    "https://google.com",
    "/google.com/%2f.",
    "//google.com",
    "///google.com",
    "%2F%2Fgoogle.com",
    "https:%2F%2Fgoogle.com"
]

async def redirectx(url, session):
    random_useragent = random.choice(_useragent_list)
    header = {"User-Agent":random_useragent}
    try:
        async with session.get(url, headers=header, allow_redirects=True) as response2:
            urlfinalParsed = urlparse(str(response2.url))
            if urlfinalParsed.netloc == "www.google.com":
                print(f"{green}[ VULNERABLLE ] {url}{reset}")
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
                    for payload in payloads:
                        query[key] = [payload]
                        new_query = urlencode(query, doseq=True)
                        new_url = urlunparse(urlp._replace(query=new_query))
                        task.append(redirectx(new_url, session))
        await asyncio.gather(*task)