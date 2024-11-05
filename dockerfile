FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Instala o Poetry para gerenciamento de dependências
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock /app/

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false && poetry install --only main --no-dev

# Copia o restante do código da aplicação
COPY . /app/

RUN mkdir -p /app/staticfiles /app/media

# Define variáveis de ambiente
ENV PYTHONPATH="/app"
ENV PORT=8000

# Expondo a porta para o Gunicorn
EXPOSE 8000

# Comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "--timeout", "120", "twitter_corujinha.wsgi:application"]
