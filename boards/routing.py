from django.urls import re_path
from boards.consumers import ScoreConsumer


websocket_urlpatterns = [
    re_path(
        r"ws/score/(?P<board_ids>(\d+,?)+)/$", ScoreConsumer.as_asgi()
    ),  # re_path(r"ws/score/", ScoreConsumer.as_asgi()),
]
