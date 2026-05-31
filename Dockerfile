# Usa uma imagem oficial do Python, leve e otimizada
FROM python:3.12-slim

# Evita que o Python crie arquivos .pyc e força o log a aparecer no terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Instala os compiladores C e as dependências gráficas do Cairo para gerar PDFs
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq gcc pkg-config libcairo2-dev && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala tudo
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do projeto para dentro do contêiner
COPY . /app/

# Expõe a porta que o Django vai usar
EXPOSE 8000

# O comando padrão para manter o servidor rodando
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]