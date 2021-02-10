from channels.routing import ProtocolTypeRouter, URLRouter 
import chatt.routing 

application = ProtocolTypeRouter({    
    # (http->Django views is added by default)    
    'websocket':    
        URLRouter(
            chatt.routing.websocket_urlpatterns
        ),
})