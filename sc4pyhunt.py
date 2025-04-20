import argparse
import asyncio
import os

parse = argparse.ArgumentParser(description="Sc4pihunt is a tool build in python for recon web.")
parse.add_argument("-sP", "--status", help="Realiza un escaneo de estado HTTP (status code) para una lista de URLs.")
parse.add_argument("-cx", "--cors", help="Detecta posibles vulnerabilidades de CORS en las URLs proporcionadas.")
parse.add_argument("-op", "--openredirect", help="Escanea las URLs en busca de vulnerabilidades de redirección abierta.")
parse.add_argument("--xss", help="Prueba vulnerabilidades de Cross-Site Scripting (XSS) en las URLs.")
parse.add_argument("-api", "-api-endpoints", help="Busca endpoints de API en las URLs objetivo.")
parse.add_argument("-S", "--subdomains", help="Enumera subdominios de un dominio dado.")
parse.add_argument("-wu", "--wayback-url", help="Recupera URLs archivadas para un dominio usando Wayback Machine.")
parse.add_argument("-WU", "--wayback-urls", action="store_true", help="Recupera y lista múltiples URLs archivadas de Wayback Machine.")
parse.add_argument("-ej", "--extrack-js", help="Extrae archivos JavaScript desde la URL proporcionada.")
parse.add_argument("-jS", "--jsensitive", help="Escanea archivos JavaScript en busca de datos sensibles (tokens, claves, etc).")
#parse.add_argument("-pT", "--pathTraversal", help="Detecta posibles fallos de path traversal en parametros mediante una lista de payloads.")

args = parse.parse_args()


if args.status:
    from scripts.status_probe import main as httprobe
    asyncio.run(httprobe(args.status))
if args.cors:
    from scripts.corsx import main as corsx
    asyncio.run(corsx(args.cors))
if args.openredirect:
    from scripts.openredirect import main as redirectx
    asyncio.run(redirectx(args.openredirect))
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
    with open(output_file, 'w') as out:
        for url in urls:
            url = url.strip()
            os.system(f"waybackurls {url} >> {output_file}")
            os.system(f"cat {output_file} | uniq > {output_file}")
if args.extrack_js:
    os.system(f"katana -u {args.extrack_js} -silent -em js -o jsfiles.txt")
if args.jsensitive:
    from scripts.jsensitive import main as jsensitive
    asyncio.run(jsensitive(args.jsensitive))
#if args.pathTraversal:
#    from scripts.directory_traversal import main as pathtraversal
#    asyncio.run(pathtraversal(args.pathTraversal))
if args.api:
    from scripts.api_endpoints import main as fuzzing_api
    asyncio.run(fuzzing_api(args.api))
