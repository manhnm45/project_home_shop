from django.urls import path
from .consumers import AIConsumer

websocket_urlpatterns = [
    path("ws/ai/", AIConsumer.as_asgi()),
]
