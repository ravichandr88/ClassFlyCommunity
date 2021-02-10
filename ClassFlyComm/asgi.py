"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClassFlyComm.settings")
django.setup()
application = get_default_application()


# import os

# import django
# from channels.auth import AuthMiddlewareStack
# from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter, URLRouter
# # from django.core.asgi import get_asgi_application
# # import chat.routing
# from chat import routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClassFlyComm.settings')
# django.setup()

# application = ProtocolTypeRouter({
#   "https": AsgiHandler(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
#   # Just HTTP for now. (We can add other protocols later.)
# })