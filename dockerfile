# Usa uma imagem oficial do Python como base, optando pela versão slim para menor tamanho
FROM python:3.12-slim

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Instala o Poetry (especifica a versão 1.6.1)
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho como a raiz do projeto
WORKDIR /app

# Copia apenas os arquivos de dependências primeiro
COPY pyproject.toml poetry.lock /app/

# Instala as dependências do Poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# Copia o restante dos arquivos do projeto
COPY . /app/

# Define variáveis de ambiente
ENV PYTHONPATH="/app"
ENV PORT=8000

# Expondo a porta para o serviço
EXPOSE $PORT

# Comando padrão para rodar o Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "twitter_corujinha.wsgi:application"]
