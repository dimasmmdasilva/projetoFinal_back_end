# Usa uma imagem oficial do Python como base
FROM python:3.12-slim

# Instala as dependências do sistema necessárias (incluindo build tools e libpq-dev para PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl

# Instala o Poetry e cria um link simbólico para garantir que o Poetry esteja no PATH
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Define o diretório de trabalho no container
WORKDIR /app

# Copia todos os arquivos do projeto para o diretório de trabalho
COPY . /app/

# Define o diretório correto onde o manage.py está localizado
WORKDIR /app/twitter_corujinha

# Adiciona o diretório do projeto ao PYTHONPATH
ENV PYTHONPATH="/app"

# Instala as dependências usando o Poetry (sem criar um ambiente virtual no container)
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Coleta os arquivos estáticos, garantindo que esteja no diretório correto
RUN python manage.py collectstatic --noinput

# Expõe a porta 8000 para acessar o serviço Django via Gunicorn
EXPOSE 8000

# Executa as migrações e depois inicia o Gunicorn quando o container for iniciado
CMD ["sh", "-c", "python manage.py migrate && gunicorn --workers 3 --bind 0.0.0.0:8000 twitter_corujinha.wsgi:application"]