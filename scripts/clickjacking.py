from colorama import init, Fore

init()
r = Fore.RED
v = Fore.GREEN
reset = Fore.RESET
def generateClickjacking():
    url = input(f"{r}[{v}${r}]{reset} URL TO CLICKJACKING PROBE ==> ")
    index = f"""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prueba de Clickjacking</title>
        <style>
            iframe {{
                width: 800px;
                height: 600px;
                border: 2px solid red;
            }}
            .overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 800px;
                height: 600px;
                opacity: 0.2;
                background-color: black;
                z-index: 9999;
            }}
            .container {{
                position: relative;
                width: 800px;
                height: 600px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <iframe src="{url}" title="Clickjacking ¿YES OR NO?"></iframe>
            <div class="overlay"></div>
        </div>
    </body>
    </html>
    """
    with open("index.html", 'w') as index1:
        index1.write(index)