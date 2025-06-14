#!/usr/bin/env python3
import urllib.parse
import argparse
from colorama import init, Fore
init()

g = Fore.GREEN

def convert(listUrl, payload):
    new_urls = []

    with open(listUrl, 'r') as fileUrls:
        urls = fileUrls.readlines()
        
    for url in urls:
        url = url.strip()
        if "=" in url:
            urlP = urllib.parse.urlparse(url)
            url_query = urlP.query
            qs = urllib.parse.parse_qsl(url_query)
            QS = [(key, payload) for key, _ in qs]
            new_query = urllib.parse.urlencode(QS)
            urlFull = urllib.parse.urlunparse(urlP._replace(query=new_query))
            new_urls.append(urlFull)

    print("[1] Re write the original archive\n[2] Create new archive")
    op = int(input("[?] "))
    if op == 1:
        with open(listUrl, 'w') as replace:
            for new_url in new_urls:
                replace.write(new_url + "\n")
    elif op == 2:
        with open("queryreplace.txt", 'a') as replace2:
            for new_url2 in new_urls:
                replace2.write(new_url2 + "\n")
    else:
        print("[x] The option is incorrect")