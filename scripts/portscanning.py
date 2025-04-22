import socket
from colorama import Fore, init

init()
g = Fore.GREEN
c = Fore.CYAN
b = Fore.BLUE
r = Fore.RED
y = Fore.YELLOW
reset = Fore.RESET 

def openPortsAll(ip, puertos):
    for puerto in puertos:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            try:
                sock.connect((ip, puerto))
            except (socket.timeout, socket.error):
                print(f"{b}[{r}+{b}] {reset}STATUS: {r}CLOSE{reset} -> {puerto}")
            else:
                print(f"{b}[{r}+{b}] {reset}STATUS: {g}OPEN{reset} -> {puerto}")
            finally:
                sock.close()

def openPort(ip, ports):
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
        except (socket.timeout, socket.error):
            print(f"{b}[{r}+{b}] {reset}STATUS: {r}CLOSE{reset} -> {port}")
        else:
            print(f"{b}[{r}+{b}] {reset}STATUS: {g}OPEN{reset} -> {port}")
        finally:
            sock.close()