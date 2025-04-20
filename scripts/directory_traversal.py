import aiohttp
import asyncio
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from colorama import Fore, init
import os
import re

init()

v = Fore.GREEN
reset = Fore.RESET

keywords = [
    "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp",
    "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "_apt", "uuidd", "messagebus",
    "/bin/bash", "/usr/sbin/nologin", "/bin/sync", "/usr/games", "/var/cache/man", "/var/spool/lpd",
    "/var/mail", "/var/spool/news", "/var/spool/uucp", "/root", "/var/backups", "/var/list", "/var/run/ircd",
    "/var/lib/gnats", "/nonexistent", "/run/uuidd"
]

escaped = [re.escape(k) for k in keywords]
combined_pattern = r"(" + "|".join(escaped) + r")"
pattern = re.compile(combined_pattern, flags=re.IGNORECASE)

sem = asyncio.Semaphore(20)

async def dpScan(url, session):
    async with sem:
        try:
            async with session.get(url) as r:
                r = await r.text()
                match = pattern.findall(r)
                if match:
                    print(f"{v}[+] PATH TRAVERSAL DETECTED ==> {url}{reset}")
                else:
                   pass
        except Exception:
            pass

async def main(file):
    async with aiohttp.ClientSession() as session:
        task = []
        path = os.path.join(os.path.dirname(__file__), "../payloads/pathtraversal_payloads.txt")
        with open(os.path.abspath(path), 'r') as rp:
            payloads = rp.readlines()

        with open(file, 'r') as rf:
            urls = rf.readlines()
        for payload in payloads:
            for url in urls:
                url = url.strip()
                urlparsed = urlparse(url)
                qs = parse_qs(urlparsed.query)
                for key in qs:
                    qs[key] = [payload]
                    encoded_query = urlencode(qs, doseq=True)
                    new_url = urlunparse(urlparsed._replace(query=encoded_query))
                    task.append(dpScan(new_url, session))
        
        await asyncio.gather(*task)