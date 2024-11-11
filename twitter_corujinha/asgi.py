import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twitter_corujinha.settings")

application = get_asgi_application()
