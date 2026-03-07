"""
ASGI config for web_sell project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from home.consumers import AIConsumer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_sell.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket": AuthMiddlewareStack(
    URLRouter([
        path("ws/ai/", AIConsumer.as_asgi()),
    ]),
    ),
})

