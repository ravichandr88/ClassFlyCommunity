from django.conf.urls import url, re_path

from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/chat/$', consumers.ChatConsumer),
      re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
      re_path(r'ws/online/(?P<room_name>\w+)/$',consumers.EchoConsumer)
]
 