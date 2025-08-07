import aiohttp
import asyncio
from urllib.parse import parse_qs,urlencode,urlunparse,urlparse

keywords = [
    "root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp",
    "proxy", "www-data", "backup", "list", "irc", "gnats", "nobody", "_apt", "uuidd", "messagebus",
    "/bin/bash", "/usr/sbin/nologin", "/bin/sync", "/usr/games", "/var/cache/man", "/var/spool/lpd",
    "/var/mail", "/var/spool/news", "/var/spool/uucp", "/root", "/var/backups", "/var/list", "/var/run/ircd",
    "/var/lib/gnats", "/nonexistent", "/run/uuidd"
]


async def scan_pt(url, session):
    async with session.get(url) as response:
        r = await response.text()
        for keyword in keywords:
            if keyword in r:
                print(f"[+] LFI FOUND IN {url}")
            else:
                pass

async def main(file, pathtraversalWordlist):
    with open(file, 'r') as fr:
        urls = fr.readlines()
    with open(pathtraversalWordlist, 'r') as rf1:
        payloads_path = rf1.readlines()

    async with aiohttp.ClientSession() as session:
        task = []
        for payload in payloads_path:
            for url in urls:
                url_parse = urlparse(url.strip())
                qs = parse_qs(url_parse.query)
                
                for key in qs:
                    qs[key] = [payload.strip()]
                    new_query = urlencode(qs, doseq=True)
                    new_url = urlunparse(url_parse._replace(query=new_query))
                    task.append(scan_pt(new_url, session))
        await asyncio.gather(*task)