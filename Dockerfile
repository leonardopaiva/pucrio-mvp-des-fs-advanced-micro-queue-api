# Usar uma imagem base do Ubuntu
FROM ubuntu:20.04

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências e o curl
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto para o diretório de trabalho
COPY . .

# Definir o comando para rodar o app (ajuste conforme necessário)
CMD ["python3", "app.py"]
