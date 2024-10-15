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
    "django.contrib.sessions",  # Suporte a sessões
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'twitter_corujinha.core',  # Sua aplicação principal
    "corsheaders",  # Habilitar CORS
]

# Middlewares
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Middleware para CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # Suporte a sessões
    "django.middleware.csrf.CsrfViewMiddleware",  # Proteção CSRF
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
                "django.template.context_processors.csrf",  # Adiciona o context processor para CSRF
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
        'rest_framework.authentication.SessionAuthentication',  # Autenticação baseada em sessão
        'rest_framework.authentication.BasicAuthentication',  # Autenticação básica
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

# Configurações CORS
CORS_ALLOWED_ORIGINS = [
    "https://twitter-corujinha-web.onrender.com",
    "https://twitter-corujinha.onrender.com",
]

# Habilitar credenciais e configurar os headers permitidos
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Definir URLs para redirecionamento de login e logout
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/dashboard/'  # Redirecionar após login bem-sucedido
LOGOUT_REDIRECT_URL = '/login/'  # Redirecionar após logout

# Tipo de campo padrão para chaves primárias
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
