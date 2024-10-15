import os
from pathlib import Path
import dj_database_url

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta (não compartilhe em produção)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-9-=sf=+m7tlz4^_$6iycv%xo(p6fhp+l&tly1bnhndb=ur$a^^")

# Debug (ajustar para False em produção)
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Permitir todos os hosts para ambiente Docker
ALLOWED_HOSTS = ['*']

# Aplicativos instalados
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",  # Adiciona suporte a sessões
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'twitter_corujinha.core',  # Sua aplicação
    "corsheaders",
]

# Middlewares
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # Sessões ativadas
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # Proteção CSRF para sessões seguras
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Autenticação baseada em sessão
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuração de URLs
ROOT_URLCONF = "twitter_corujinha.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = "twitter_corujinha.wsgi.application"

# Configuração do banco de dados PostgreSQL
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Modelo de usuário customizado
AUTH_USER_MODEL = 'core.User'

# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configurações de linguagem e tempo
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Configurações do Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # Usando autenticação baseada em sessão
        'rest_framework.authentication.BasicAuthentication',  # Caso precise de autenticação básica em endpoints REST
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Apenas usuários autenticados podem acessar as APIs
    ),
}

# Configurações de arquivos estáticos e de mídia para o Docker e Nginx
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações CORS para permitir requisições do front-end e back-end hospedados no Render
CORS_ALLOWED_ORIGINS = [
    "https://twitter-corujinha-web.onrender.com",
    "https://twitter-corujinha.onrender.com",
]

# Tipo de campo padrão para chaves primárias
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
