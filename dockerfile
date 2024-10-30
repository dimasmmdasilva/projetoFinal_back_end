FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --only main --no-dev

COPY . /app/

RUN mkdir -p /app/staticfiles /app/media

ENV PYTHONPATH="/app"
ENV PORT=8000

EXPOSE 8000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "--timeout", "120", "twitter_corujinha.wsgi:application"]
