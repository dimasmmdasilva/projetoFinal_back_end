import os
from pathlib import Path
from datetime import timedelta

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta para uso em desenvolvimento (não segura para produção)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-9-=sf=+m7tlz4^_$6iycv%xo(p6fhp+l&tly1bnhndb=ur$a^^")

# Modo de depuração
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ['dimasmmdasilva.pythonanywhere.com']

# Configuração do modelo de usuário personalizado
AUTH_USER_MODEL = 'core.User'

# Aplicações instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
    "twitter_corujinha.core",
]

# Middlewares
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configuração do URL principal
ROOT_URLCONF = "twitter_corujinha.urls"

# Banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dimasmmdasilva$projetofinaltwitter',  
        'USER': 'dimasmmdasilva',
        'PASSWORD': 'projetofinal0001',
        'HOST': 'dimasmmdasilva.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}


# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração do WSGI
WSGI_APPLICATION = "twitter_corujinha.wsgi.application"

# Configuração do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Configuração do Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Configuração de CORS
CORS_ALLOWED_ORIGINS = [
    "https://projeto-final-ebac-umber.vercel.app",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    'Authorization',
    'Content-Type',
    'X-Requested-With',
]

# Configuração de arquivos estáticos e de mídia
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurações adicionais de segurança e cookies
SESSION_COOKIE_SECURE = not DEBUG  # Apenas cookies seguros em produção
CSRF_COOKIE_SECURE = not DEBUG     # Apenas cookies seguros em produção
SESSION_COOKIE_SAMESITE = 'Lax'    # Evita envio de cookies de sessão para sites externos
CSRF_COOKIE_SAMESITE = 'Lax'       # Evita envio de cookies CSRF para sites externos
SESSION_COOKIE_HTTPONLY = True     # Protege contra ataques de XSS
CSRF_COOKIE_HTTPONLY = True        # Protege contra ataques de XSS

# Configuração de logs (opcional)
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
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}
