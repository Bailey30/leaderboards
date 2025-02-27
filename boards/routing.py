from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from boards.consumers import ScoreConsumer


websocket_urlpatterns = [
    re_path("ws/score/", ScoreConsumer.as_asgi()),
]
