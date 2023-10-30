from django.urls import path, re_path
from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    # path('ws/chat/<str:room_name>/', ChatRoomConsumer, name='chat_room'),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatRoomConsumer.as_asgi()),
]