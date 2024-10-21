import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta e Debug (ajustar DEBUG para False em produção)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-9-=sf=+m7tlz4^_$6iycv%xo(p6fhp+l&tly1bnhndb=ur$a^^")
DEBUG = True  # Coloque False em produção
ALLOWED_HOSTS = ['*']  # Ajuste em produção para incluir domínios específicos

# Aplicativos instalados
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'twitter_corujinha.core',  # Módulo principal
    "corsheaders",  # Habilitar CORS
    'rest_framework_simplejwt.token_blacklist',  # JWT Token Blacklist para suporte a logout
]

# Middlewares
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Middleware para CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # Proteção CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuração de URLs e Templates
ROOT_URLCONF = "twitter_corujinha.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Caso precise adicionar templates customizados, adicione o caminho aqui
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

# WSGI
WSGI_APPLICATION = "twitter_corujinha.wsgi.application"

# Banco de dados PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'twitter_db',  
        'USER': 'postgres',  
        'PASSWORD': 'Dim4s3388***',  
        'HOST': 'host.docker.internal',  
        'PORT': '5432',  
    }
}

# Modelo de usuário customizado
AUTH_USER_MODEL = 'core.User'

# Configurações do Django Rest Framework com suporte a JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Autenticação JWT
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Apenas usuários autenticados podem acessar as APIs
    ),
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Configuração JWT para Cookies
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_COOKIE_NAME': 'jwt_access',
    'TOKEN_COOKIE_HTTPONLY': True,
}

# Configurações de cookies seguros
SESSION_COOKIE_SECURE = True  # Defina como True em produção
CSRF_COOKIE_SECURE = True  # Defina como True em produção
SECURE_SSL_REDIRECT = True  # Defina como True em produção
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Configurações CORS ajustadas corretamente
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Frontend rodando localmente
    "http://web:8000",  # Backend rodando no Docker
]
CORS_ALLOW_CREDENTIALS = True

# Configurações de arquivos estáticos e de mídia
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações de Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Nível de log definido como DEBUG
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {  # Logs detalhados de consultas ao banco de dados
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.request': {  # Logs de requisições HTTP
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}