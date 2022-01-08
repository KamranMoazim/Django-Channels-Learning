from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/sc/<str:groupkname>", consumers.MySyncConsumer.as_asgi()),
    path("ws/ac/<str:groupkname>", consumers.MyAsyncConsumer.as_asgi())
]