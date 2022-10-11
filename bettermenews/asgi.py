"""
ASGI config for bettermenews project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

from email.mime import application
import os

from django.core.asgi import get_asgi_application
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
import main.urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bettermenews.settings')

#application = get_asgi_application()

application = ProtocolTypeRouter({
    #"http": AsgiHandler(),
    'http':get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(main.urls.websocket_urlpatterns)),
})
