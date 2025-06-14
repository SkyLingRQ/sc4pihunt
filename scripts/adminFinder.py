import aiohttp
import asyncio
import random
from urllib.parse import urlparse
from scripts.useragent.user_agent import _useragent_list
from colorama import init, Fore
from tqdm import tqdm
import sys

init(autoreset=True)

rd = Fore.RED
y = Fore.YELLOW
g = Fore.GREEN
c = Fore.CYAN
rs = Fore.LIGHTMAGENTA_EX

sem = asyncio.Semaphore(100)

banner = f"""
{rd}[{rs}+{rd}]=================================[{rs}+{rd}]
{rd}|       {g}ADMIN PANEL FINDER           {rd}|
{rd}|       {g}By: Sc4pyhunt                {rd}|
{rd}|       {g}Targeting hidden URLs...     {rd}|
{rd}[{rs}+{rd}]=================================[{rs}+{rd}]
"""

endpoints = [
    "/admin/", "/administrator/", "/admin1/", "/admin2/", "/admin3/", "/admin4/", "/admin5/",
    "/usuarios/", "/usuario/", "/usuarios/admin", "/login/", "/adminarea/", "/adminArea/",
    "/admin_area/", "/cpanel/", "/wp-login.php", "/adminLogin.php", "/admin/index.php",
    "/admin/login.php", "/admin/home.php", "/admin/controlpanel.php", "/admin/cp.php",
    "/administrator/index.php", "/administrator/login.php", "/admin/account.php",
    "/admin_area/login.php", "/admin_area/admin.php", "/admin/account.php", "/admin_panel/",
    "/admin1.php", "/admin2.php", "/admin3.php", "/admin4.php", "/admin5.php", "/usuarios.php",
    "/usuario.php", "/cpanel.php", "/adminarea.php", "/admin_area.php", "/panel-administrador/"
]

def build_url(base_url, endpoint):
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'http://' + base_url
    parsed = urlparse(base_url)
    return f"{parsed.scheme}://{parsed.netloc}{endpoint}"

async def admin_finder(url, session):
    headers = {"User-Agent": random.choice(_useragent_list)}
    try:
        async with sem:
            async with session.get(url, headers=headers, timeout=10) as r:
                status = r.status
                if status == 200:
                    print(f"{g}[{status}] {url}")
                elif status == 403:
                    print(f"{y}[{status}] {url}")
                elif status in [301, 302]:
                    print(f"{c}[{status}] {url}")
                elif status == 404:
                    pass
                else:
                    print(f"{rs}[{status}] {url}")
    except aiohttp.ClientError as e:
        print(f"{rd}[ERROR] {url} - {e}")
    except asyncio.TimeoutError:
        print(f"{rd}[TIMEOUT] {url}")

async def scan_multiple(session):
    file = input("[#] Ruta del archivo: ").strip()
    try:
        with open(file, 'r') as fr:
            targets = [line.strip() for line in fr if line.strip()]
    except FileNotFoundError:
        print(f"{rd}[x] Archivo no encontrado.")
        return

    print("[+] Escaneando múltiples URLs...\n")
    tasks = []
    for base in tqdm(targets, desc="Generando tareas", ncols=80):
        for ep in endpoints:
            full_url = build_url(base, ep)
            tasks.append(admin_finder(full_url, session))
    await asyncio.gather(*tasks)

async def scan_single(session):
    url = input("[#] URL única: ").strip()
    tasks = [admin_finder(build_url(url, ep), session) for ep in endpoints]
    await asyncio.gather(*tasks)

async def main():
    print(banner)
    print("[1] Escanear múltiples URLs (archivo)")
    print("[2] Escanear una sola URL")
    try:
        op = int(input("[#] Opción: ").strip())
    except ValueError:
        print(f"{rd}[x] Opción inválida.")
        sys.exit(1)

    async with aiohttp.ClientSession() as session:
        if op == 1:
            await scan_multiple(session)
        elif op == 2:
            await scan_single(session)
        else:
            print(f"{rd}[x] Selección inválida.")
            sys.exit(1)