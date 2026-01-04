<p align="center">
  <img src="img/Logo de SC4PIHUNT.png" alt="SC4PIHUNT Logo" width=400>
</p>


# SC4PYHUNT DESCRIPTION
Sc4pyhunt is a tool build in python for recon web. 🕸️

# INSTALL
```bash
git clone https://github.com/SkyLingRQ/sc4pihunt
cd sc4pyhunt
chmod +x sc4pyhunt.py install.sh
sudo ./install.sh
pip install -r requirements.txt
```

# USAGE
```bash
usage: sc4pyhunt.py [-h] [-sP STATUS] [-cx CORS] [-op REDIRECT] [--xss XSS] [-api API] [-S SUBDOMAINS] [-wu WAYBACK_URL] [-WU]
                    [-ej EXTRACK_JS] [-jS JSENSITIVE] [-pT [PATHTRAVERSAL]] [-pS PORTSCANNING] [-qR QSREPLACE] [-ip IP]
                    [--clickjacking] [--hhi] [--admin-panel] [-alienvault] [-crt CRT] [--ssti SSTI] [-sql SQLINJECTION] [-f FILE]
                    [-crlf CRLF_INJECTION]

Sc4pihunt is a tool build in python for recon web.

options:
  -h, --help            show this help message and exit
  -sP STATUS, --status STATUS
                        Realiza un escaneo de estado HTTP (status code) para una lista de URLs.
  -cx CORS, --cors CORS
                        Detecta posibles vulnerabilidades de CORS en las URLs proporcionadas.
  -op REDIRECT, --redirect REDIRECT
                        Escanea las URLs en busca de vulnerabilidades de redirección abierta.
  --xss XSS             Prueba vulnerabilidades de Cross-Site Scripting (XSS) en las URLs.
  -api API, -api-endpoints API
                        Busca endpoints de API en las URLs objetivo.
  -S SUBDOMAINS, --subdomains SUBDOMAINS
                        Enumera subdominios de un dominio dado.
  -wu WAYBACK_URL, --wayback-url WAYBACK_URL
                        Recupera URLs archivadas para un dominio usando Wayback Machine.
  -WU, --wayback-urls   Recupera y lista múltiples URLs archivadas de Wayback Machine.
  -ej EXTRACK_JS, --extrack-js EXTRACK_JS
                        Extrae archivos JavaScript desde la URL proporcionada.
  -jS JSENSITIVE, --jsensitive JSENSITIVE
                        Escanea archivos JavaScript en busca de datos sensibles (tokens, claves, etc).
  -pT [PATHTRAVERSAL], --pathTraversal [PATHTRAVERSAL]
                        Detecta posibles fallos de path traversal en parametros mediante una lista de payloads proporcionada por el
                        usuario.
  -pS PORTSCANNING, --portscanning PORTSCANNING
                        Escaneo de puertos a una IP
  -qR QSREPLACE, --qsreplace QSREPLACE
                        Remplaza valores de querys de una lista de URLs.
  -ip IP                Extraer ip de un dominio
  --clickjacking        Genera un HTML que verifica si la web es vulnerable a clickjacking mediante un iframe
  --hhi                 Escanear una URL o lista de URLs en busca de una inyección de el header Host.
  --admin-panel         Hace un alasisis mediante endpoints para el reconocimiento de rutas de admin panel en una lista de webs o una
                        única URL
  -alienvault           Consultar dominio en AlienVault
  -crt CRT              Buscar subdominios mediante el servicio de crt.sh
  --ssti SSTI           Escanear una lista de URLs en busca de vulnerabilidad Server-Side Template Injection (SSTI)
  -sql SQLINJECTION, --sqlinjection SQLINJECTION
                        Escanear respuestas de URLs con payloads de SQLInjection en busca de indicios vulnerables.
  -f FILE, --file FILE  Archivo con URLs para automatizar.
  -crlf CRLF_INJECTION, --crlf-injection CRLF_INJECTION
                        Escanear una lista de URLs en busca de inyecciones CRLF.
```


