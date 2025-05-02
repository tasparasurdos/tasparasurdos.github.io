FROM debian:stable-slim

# Atualize e instale pacotes essenciais
RUN apt update && apt -y upgrade
RUN apt install -y wget fontconfig libfreetype6 libjpeg62-turbo \
    libpng16-16 libx11-6 libxcb1 libxext6 libxrender1 xfonts-75dpi \
    xfonts-base python3 python3-pip python3-venv

# Baixe e instale libssl1.1 manualmente
RUN wget http://ftp.br.debian.org/debian/pool/main/o/openssl/libssl1.1_1.1.1n-0+deb10u3_amd64.deb
RUN dpkg -i libssl1.1_1.1.1n-0+deb10u3_amd64.deb || apt-get install -f -y

# Baixe e configure o wkhtmltox
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || apt-get install -f -y

# Desativar o ambiente gerenciado externamente
RUN rm /usr/share/doc/python3.11/EXTERNALLY-MANAGED || true

# Defina o diretório de trabalho
WORKDIR /app
