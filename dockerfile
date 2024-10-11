# Usa uma imagem oficial do Python como base
FROM python:3.12-slim

# Instala as dependências do sistema necessárias (incluindo build tools e libpq-dev para PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl

# Instala o Poetry (opcionalmente define a versão) e cria um link simbólico para garantir que o Poetry esteja no PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho no container como a raiz do projeto
WORKDIR /app

# Copia todos os arquivos do projeto para o diretório de trabalho
COPY . /app/

# Adiciona o diretório do projeto ao PYTHONPATH
ENV PYTHONPATH="/app"

# Instala as dependências usando o Poetry (sem criar um ambiente virtual no container)
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Executa as migrações e depois inicia o Gunicorn quando o container for iniciado
CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers 3 --bind 0.0.0.0:$PORT twitter_corujinha.wsgi:application"]
