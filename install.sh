#!/bin/bash

# ACTUALIZACIÓN DE PAQUETES
sudo apt update -y
sudo apt install golang-go -y

# VARIABLES
GOPATH="$HOME/go"
GOBIN="$GOPATH/bin"

# ASEGURARSE DE QUE GOPATH ESTÁ CONFIGURADO
export PATH=$PATH:$GOBIN

# MENSAJE DE INICIO
echo -e "\n\033[1;32m[+] Comenzando Instalación De Herramientas Externas Necesarias...\033[0m\n"

# INSTALACIÓN DE HERRAMIENTAS
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
CGO_ENABLED=1 go install github.com/projectdiscovery/katana/cmd/katana@latest

# MOVER LOS BINARIOS A /usr/bin
sudo mv "$GOBIN/waybackurls" /usr/bin/
sudo mv "$GOBIN/gau" /usr/bin/
sudo mv "$GOBIN/subfinder" /usr/bin/
sudo mv "$GOBIN/assetfinder" /usr/bin/
sudo mv "$GOBIN/katana" /usr/bin/

# FINAL
echo -e "\n\033[1;32m[✔] La instalación ha terminado.\033[0m\n"

# BORRAR INSTALADOR
[[ "$0" == "./install.sh" ]] && sudo rm -f install.sh