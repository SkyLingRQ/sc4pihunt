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
keywords = []

interesting_patterns = {
    'API_KEYS': r'(?i)(?:api[_-]?key|apikey|apiKey|API_KEY|api.secret)["\'\s:=]+["\']?[a-zA-Z0-9_\-]{20,}["\']?',
    
    'PASSWORDS': r'(?i)(?:password|passwd|pwd|pass|user_pass|user_password|admin_password|root_pass)["\'\s:=]+["\']?.{8,}["\']?',
    
    'TOKENS': r'(?i)(?:token|access_token|auth_token|admin_token|user_token|TOKEN_ADMIN|JWT|bearer)["\'\s:=]+["\']?[a-zA-Z0-9_\-\.=]{20,}["\']?',
    
    'CREDENTIALS': r'(?i)(?:credentials|auth|login|auth_data)["\'\s:=]+["\']?.{8,}["\']?',
    
    'SECRET_KEYS': r'(?i)(?:secret|secret_key|client_secret|private_key)["\'\s:=]+["\']?[a-zA-Z0-9_\-]{20,}["\']?',
    
    'EMAILS': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    
    'HARDCODED_AUTH': r'(?i)(user(name)?|admin|login)["\'\s:=]+["\']?.{3,}["\']?.*(pass(word)?|pwd)["\'\s:=]+["\']?.{3,}["\']?',

    'AWS_ACCESS_KEY_ID': r'AKIA[0-9A-Z]{16}',

    'AWS_SECRET_ACCESS_KEY': r'(?i)aws_secret_access_key["\'\s:=]+["\']?[A-Za-z0-9/+=]{40}["\']?',

    'AWS_SESSION_TOKEN': r'(?i)aws_session_token["\'\s:=]+["\']?[A-Za-z0-9/+=]{300,}["\']?',

    'HEROKU_API_KEY': r'(?i)heroku_api_key["\'\s:=]+["\']?[0-9a-f]{32}["\']?',

    'GOOGLE_OAUTH_TOKEN': r'ya29\.[0-9A-Za-z\-_]+',

    'GOOGLE_API_KEY': r'AIza[0-9A-Za-z\-_]{35}',

    'TWILIO_SID': r'AC[0-9a-fA-F]{32}',

    'TWILIO_AUTH_TOKEN': r'(?i)twilio_auth_token["\'\s:=]+["\']?[0-9a-f]{32}["\']?',

    'FIREBASE_DB_URL': r'https:\/\/[a-z0-9\-]+\.firebaseio\.com',

    'SLACK_TOKEN': r'xox[pb]-[0-9a-zA-Z\-]+',

    'STRIPE_API_KEY': r'sk_(live|test)_[0-9a-zA-Z]{24}',

    'GITHUB_PAT': r'[a-f0-9]{40}',
    
    'AZURE_STORAGE_KEY': r'(?i)azure_storage_key["\'\s:=]+["\']?[A-Za-z0-9+/=]{88}["\']?',
    
    'FACEBOOK_ACCESS_TOKEN': r'EAACEdEose0cBA[0-9A-Za-z]+',
    
    'TWITTER_API_KEY': r'[0-9a-zA-Z]{25}',
    
    'SENDGRID_API_KEY': r'SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}',
    
    'MAILGUN_API_KEY': r'key-[0-9a-zA-Z]{32}',
    
    'MONGODB_URI': r'mongodb:\/\/[^\s]+:[^\s]+@[^\s]+',
    
    'DATADOG_API_KEY': r'[0-9a-f]{32}',
    
    'TWILIO_MESSAGING_SERVICE_SID': r'MG[0-9a-f]{32}',
    
    'STRIPE_PUBLIC_KEY': r'pk_(live|test)_[0-9a-zA-Z]{24}',

    'OKTA_API_TOKEN': r'(?i)okta_api_token["\'\s:=]+["\']?([a-z0-9]{40,})["\']?',

    'OKTA_CLIENT_SECRET': r'(?i)okta_client_secret["\'\s:=]+["\']?([A-Za-z0-9_\-\.]{30,})["\']?',
    
    'OKTA_OAUTH_JWT': r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+'
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
