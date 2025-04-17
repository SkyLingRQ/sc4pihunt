import aiohttp
import asyncio
from colorama import Fore, init
import re

init()
g = Fore.GREEN
rd = Fore.RED
y = Fore.YELLOW
p = Fore.MAGENTA
reset = Fore.RESET
keywords = []

interesting_patterns = {
    'API_KEYS': r'(?i)(?:api[_-]?key|apikey|apiKey|API_KEY|api.secret)["\'\s:=]+["\']?[a-zA-Z0-9_\-]{20,}["\']?',
    
    'PASSWORDS': r'(?i)(?:password|passwd|pwd|pass|user_pass|user_password|admin_password|root_pass)["\'\s:=]+["\']?.{8,}["\']?',
    
    'TOKENS': r'(?i)(?:token|access_token|auth_token|admin_token|user_token|TOKEN_ADMIN|JWT|bearer)["\'\s:=]+["\']?[a-zA-Z0-9_\-\.=]{20,}["\']?',
    
    'CREDENTIALS': r'(?i)(?:credentials|auth|login|auth_data)["\'\s:=]+["\']?.{8,}["\']?',
    
    'SECRET_KEYS': r'(?i)(?:secret|secret_key|client_secret|private_key)["\'\s:=]+["\']?[a-zA-Z0-9_\-]{20,}["\']?',
    
    'EMAILS': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        
    'SENSITIVE_FUNCTIONS': r'(?i)(eval|setTimeout|setInterval|Function|exec|spawn|child_process|system|os\.system|subprocess)\s*\([^)]+\)',
    
    'HARDCODED_AUTH': r'(?i)(user(name)?|admin|login)["\'\s:=]+["\']?.{3,}["\']?.*(pass(word)?|pwd)["\'\s:=]+["\']?.{3,}["\']?',
}


async def recon_sensitive_info(jsurl, session):
    try:
        async with session.get(jsurl) as response:
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