#!/usr/bin/env python3
import urllib.parse
import argparse
from colorama import init, Fore

init()

g = Fore.GREEN

def convert(listUrl, payload):
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
            print(f"{g}[Url Encoded] {urlFull}")
            with open("queryreplace.txt", 'a') as replace:
                replace.write(urlFull + '\n')