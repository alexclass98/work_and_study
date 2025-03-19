# was_app/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/wall/$', consumers.WallConsumer.as_asgi()),
]