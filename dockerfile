# Usa uma imagem oficial do Python como base, optando pela versão slim para menor tamanho
FROM python:3.12-slim

# Instala as dependências do sistema necessárias (build tools e libpq-dev para PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Instala o Poetry (especifica a versão 1.6.1) e adiciona ao PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho como a raiz do projeto
WORKDIR /app

# Copia apenas os arquivos de dependências primeiro para melhor aproveitamento de cache
COPY pyproject.toml poetry.lock /app/

# Instala as dependências do Poetry sem criar ambientes virtuais
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Agora copia o restante dos arquivos do projeto
COPY . /app/

# Define variáveis de ambiente
ENV PYTHONPATH="/app"
ENV PORT=8000

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expondo a porta para o serviço
EXPOSE $PORT

# Comando padrão para rodar o container
CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers 3 --bind 0.0.0.0:$PORT twitter_corujinha.wsgi:application"]
