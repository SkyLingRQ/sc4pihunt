import aiohttp
import asyncio
import random
from scripts.useragent.user_agent import _useragent_list
from colorama import Fore, init
import re

init()
g = Fore.GREEN
rd = Fore.RED
y = Fore.YELLOW
p = Fore.MAGENTA
reset = Fore.RESET


interesting_patterns = {
    "Generic API Key": r'(?i)(api[_-]?key|apikey|client[_-]?key)["\s:=]+["\']([a-zA-Z0-9_\-]{20,})["\']',
    "Password": r'(?i)(password|passwd|pwd|admin_pass|root_pass)["\s:=]+["\']([^"\']{8,})["\']',
    "Auth Token": r'(?i)(access[_-]?token|auth[_-]?token|bearer|jwt)["\s:=]+["\']([a-zA-Z0-9\-_.=]{20,})["\']',
    "JWT": r'eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{10,}',
    "AWS Access Key": r'AKIA[0-9A-Z]{16}',
    "AWS Secret Key": r'(?i)aws(.{0,20})?(secret|private)?(.{0,20})?key["\s:=]+["\']([A-Za-z0-9/+=]{40})["\']',
    "Private Key Block": r'-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----',
    "DB Connection": r'(?i)(mongodb|mysql|postgres|postgresql):\/\/[^\s\'"]+:[^\s\'"]+@[^\s\'"]+',
    "URL with Token": r'https?:\/\/[^\s\'"]*(token|key|auth|access)[=\/][^\s\'"&]+',
    "Session ID": r'(?i)(sessionid|phpsessid|jsessionid)["\s:=]+["\']([a-zA-Z0-9\-]{16,})["\']',
    "Dangerous JS Sink": r'(?i)(eval|new Function|setTimeout|setInterval|document\.write|innerHTML|outerHTML)\s*=?',
    "Google API Key": r'AIza[0-9A-Za-z\-_]{35}',
    "Google OAuth Token": r'ya29\.[0-9A-Za-z\-_]+',
    "Stripe Secret Key": r'sk_(live|test)_[0-9a-zA-Z]{24}',
    "Slack Token": r'xox[baprs]-[0-9a-zA-Z\-]{10,48}',
    "GitHub Token": r'ghp_[A-Za-z0-9]{36}',
    "SendGrid Key": r'SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}',
}


async def recon_sensitive_info(jsurl, session):
    header = {"User-Agent":random.choice(_useragent_list)}
    try:
        async with session.get(jsurl, headers=header) as response:
            r = await response.text()
            sensitive = {}
            for param, values in interesting_patterns.items():
                l = re.findall(values, r)
                if l:
                    print(g+"[+] POSSIBLE INFORMATION SENSITIVE"+reset)
                    print(f"{rd}[#] URL ==> {jsurl}{reset}")
                    print(f"{p}[$] {param} ==>{y} {l}{reset}\n")
    except Exception:
        pass


async def main(jsfile):
    task = []
    async with aiohttp.ClientSession() as session:
        with open(jsfile, 'r') as rf:
            jsUrls = rf.readlines()
        for jsurl in jsUrls:
            jsurl = jsurl.strip()
            task.append(recon_sensitive_info(jsurl, session))
        await asyncio.gather(*task)
