import argparse
import asyncio
import os
import requests
import json
import socket
from colorama import Fore, init
from time import sleep

init()

red = Fore.RED
green = Fore.GREEN
purple = Fore.MAGENTA
yellow = Fore.YELLOW
reset = Fore.RESET

parse = argparse.ArgumentParser(description="Sc4pihunt is a tool build in python for recon web.")
parse.add_argument("-sP", "--status", help="Realiza un escaneo de estado HTTP (status code) para una lista de URLs.")
parse.add_argument("-cx", "--cors", help="Detecta posibles vulnerabilidades de CORS en las URLs proporcionadas.")
parse.add_argument("-op", "--redirect", help="Escanea las URLs en busca de vulnerabilidades de redirección abierta.")
parse.add_argument("--xss", help="Prueba vulnerabilidades de Cross-Site Scripting (XSS) en las URLs.")
parse.add_argument("-api", "-api-endpoints", help="Busca endpoints de API en las URLs objetivo.")
parse.add_argument("-S", "--subdomains", help="Enumera subdominios de un dominio dado.")
parse.add_argument("-wu", "--wayback-url", help="Recupera URLs archivadas para un dominio usando Wayback Machine.")
parse.add_argument("-WU", "--wayback-urls", action="store_true", help="Recupera y lista múltiples URLs archivadas de Wayback Machine.")
parse.add_argument("-ej", "--extrack-js", help="Extrae archivos JavaScript desde la URL proporcionada.")
parse.add_argument("-jS", "--jsensitive", help="Escanea archivos JavaScript en busca de datos sensibles (tokens, claves, etc).")
parse.add_argument("-pT", "--pathTraversal", help="Detecta posibles fallos de path traversal en parametros mediante una lista de payloads proporcionada por el usuario.", default=None, nargs="?")
parse.add_argument('-pS', "--portscanning" ,help="Escaneo de puertos a una IP")
parse.add_argument('-qR', '--qsreplace', help="Remplaza valores de querys de una lista de URLs.")
parse.add_argument("-ip", help="Extraer ip de un dominio")
parse.add_argument("--clickjacking", help="Genera un HTML que verifica si la web es vulnerable a clickjacking mediante un iframe", action="store_true")
parse.add_argument("--hhi", help="Escanear una URL o lista de URLs en busca de una inyección de el header Host.", action="store_true")
parse.add_argument("--admin-panel", help="Hace un alasisis mediante endpoints para el reconocimiento de rutas de admin panel en una lista de webs o una única URL", action="store_true")
parse.add_argument("-alienvault", help="Consultar dominio en AlienVault", action="store_true")
parse.add_argument("-crt", help="Buscar subdominios mediante el servicio de crt.sh")
parse.add_argument("--ssti", help="Escanear una lista de URLs en busca de vulnerabilidad Server-Side Template Injection (SSTI)")
parse.add_argument("-sql", "--sqlinjection", help="Escanear respuestas de URLs con payloads de SQLInjection en busca de indicios vulnerables.")
parse.add_argument("-f", "--file", help="Archivo con URLs para automatizar.", default=None)
args = parse.parse_args()


##### CHECK VERSION OF SCRIPT #####

    ### GET VERSION LATEST

url = "https://raw.githubusercontent.com/SkyLingRQ/sc4pihunt/main/others/version/version.json"

version_data = requests.get(url)
version = version_data.json()["latest_version"]

    ### GET VERSION OF ACTUAL SC4PIHUNT

with open("others/version/version.json", 'r') as random:
    load_json = json.load(random)

if load_json["latest_version"] != version:
    print(f"{red}[!] Sc4pihunt is outdated. Update for more features!!{reset}")
    sleep(1)
    
else:
    pass


##### END OF THE CHECK #####

if args.status:
    from scripts.status_probe import main as httprobe
    asyncio.run(httprobe(args.status))
if args.cors:
    from scripts.corsx import main as corsx
    asyncio.run(corsx(args.cors))
if args.redirect:
    from scripts.openredirect import main as redirectx
    asyncio.run(redirectx(args.redirect))
if args.xss:
    from scripts.vacpxss import main as vacpxss
    asyncio.run(vacpxss(args.xss))
if args.subdomains:
    os.system(f"subfinder -d {args.subdomains} -all -recursive -silent -o s.txt && assetfinder -subs-only {args.subdomains} > e.txt && sort -u s.txt e.txt > subdomains.txt && rm -rf e.txt s.txt")
if args.wayback_url:
    os.system(f"waybackurls {args.wayback_url} >> s.txt && gau {args.wayback_url} >> t.txt && sort -u s.txt t.txt > pathone.txt && rm -rf s.txt t.txt")
if args.wayback_urls:
    archive_path = input("[ FILE ] Path: ")
    output_file = "resultados.txt"
    with open(archive_path, 'r') as f:
        urls = f.readlines()
    with open(output_file, 'w') as _:
        for url in urls:
            url = url.strip()
            os.system(f"waybackurls {url} >> {output_file}")
if args.extrack_js:
    os.system(f"katana -u {args.extrack_js} -silent -em js -o jsfiles.txt")
if args.jsensitive:
    from scripts.jsensitive import main as jsensitive
    asyncio.run(jsensitive(args.jsensitive))
if args.api:
    from scripts.api_endpoints import main as fuzzing_api
    asyncio.run(fuzzing_api(args.api))

if args.portscanning:
    from scripts.portscanning import openPortsAll, openPort
    try:
        op = int(input("[1] Escaneo total de puertos\n[2] Escaneo de ciertos puertos\n$~ "))
    except ValueError:
        print(f"{red}[x] El valor del prompt debe de ser entero o sea, un número.{reset}")
    if op == 1:
        puertos = range(0, 65536)
        openPortsAll(args.portscanning, puertos)
    elif op == 2:
        rang = input("[#] EJEMPLO: 0,80,4444\n[?] ")
        if ',' in rang:
            ports = [int(port) for port in rang.split(',')]
        
        if ports:
            openPort(args.portscanning, ports)
        else:
            print(f"{red}[x] Puertos en 0.{reset}")
if args.qsreplace:
    from scripts.queryreplace import convert
    payload = input(f"[{green}${reset}] PAYLOAD IS: ")
    convert(args.qsreplace, payload)
if args.ip:
    try:
        ip = socket.gethostbyname(args.ip)
        print(f"{purple}[+] {args.ip} ==>{yellow} {ip}{reset}")
    except Exception:
        print(f"{red}[x] Ocurrió un error.{reset}")
if args.clickjacking:
    from scripts.clickjacking import generateClickjacking
    generateClickjacking()
if args.hhi:
    from scripts.hhi import main as hhi_scan
    asyncio.run(hhi_scan())
if args.admin_panel:
    from scripts.adminFinder import main as adminFinder
    asyncio.run(adminFinder())
if args.alienvault:
    from scripts.alienvault import main as alienvault
    alienvault()
if args.crt:
    from scripts.crt import main as crt
    crt(args.crt)
if args.ssti:
    from scripts.ssti_reflected import main as ssti_scan
    asyncio.run(ssti_scan(args.ssti))
if args.pathTraversal is not None or args.file:
    from scripts.directory_traversal import main as lfi
    url_to_scan = args.pathTraversal if args.pathTraversal else None
    file_to_scan = args.file if args.file else None
    asyncio.run(lfi(url=url_to_scan, file=file_to_scan))
if args.sqlinjection:
    from scripts.sqli import main as sqlinjection
    asyncio.run(sqlinjection(args.sqlinjection))