import argparse
import asyncio
import os

parse = argparse.ArgumentParser(description="")
parse.add_argument("--status", help="")
parse.add_argument("--cors", help="")
parse.add_argument("--openredirect", help="")
parse.add_argument("--xss", help="")
parse.add_argument("-api-endpoints", help="")
parse.add_argument("--subdomains", help="")
parse.add_argument("-wayback-url", help="")
parse.add_argument("-wayback-urls", action="store_true", help="")
parse.add_argument("-ej", "--extrack-js", help="")
parse.add_argument("-jS", "--jsensitive", help="")

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
    os.system(f"sudo subfinder -d {args.subdomains} -all -recursive -silent -o s.txt && sudo assetfinder -subs-only {args.subdomains} > e.txt && sort -u s.txt e.txt > subdomains.txt && sudo rm -rf e.txt s.txt")
if args.wayback_url:
    os.system("waybackurls {args.wayback_url} >> s.txt && gau {args.wayback_url} >> t.txt && sort -u s.txt t.txt > pathone.txt && sudo rm -rf s.txt t.txt")
if args.wayback_urls:
    archive_path = input("[ FILE ] Path: ")
    output_file = "resultados.txt"
    with open(archive_path, 'r') as f:
        urls = f.readlines()
    with open(output_file, 'w') as out:
        for url in urls:
            url = url.strip()
            os.system(f"waybackurls {url} >> {output_file}")
if args.extrack_js:
    os.system(f"katana -u {args.extrack_js} -silent -em js -o jsfiles.txt")
if args.jsensitive:
    from scripts.jsensitive import main as jsensitive
    asyncio.run(jsensitive(args.jsensitive))