# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# from . import tasks







# COMMANDS = {
#     'help': {
#         'help': 'Display help message.',
#     },
#     'sum': {
#         'args': 2,
#         'help': 'Calculate sum of two integer arguments. Example: `sum 12 32`.',
#         'task': 'add'
#     },
#     'status': {
#         'args': 1,
#         'help': 'Check website status. Example: `status twitter.com`.',
#         'task': 'url_status'
#     },
# }



# class ChatConsumer(WebsocketConsumer):
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         response_message = 'Please type `help` for the list of the commands.'
#         message_parts = message.split()
#         if message_parts:
#             command = message_parts[0].lower()
#             if command == 'help':
#                 response_message = 'List of the available commands:\n' + '\n'.join([f'{command} - {params["help"]} ' for command, params in COMMANDS.items()])
#             elif command in COMMANDS:
#                 if len(message_parts[1:]) != COMMANDS[command]['args']:
#                     response_message = f'Wrong arguments for the command `{command}`.'
#                 else:
#                     getattr(tasks, COMMANDS[command]['task']).delay(self.channel_name, *message_parts[1:])
#                     response_message = f'Command `{command}` received.'
        
#         async_to_sync(self.channel_layer.send)(
#                 self.channel_name,
#                 {
#                     'type': 'chat_message',
#                     'message': response_message
#                 }
#             )

#     def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': f'[bot]: {message}'
#         }))


# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import TwoGroup,Messages
from django.utils import timezone
from datetime import datetime



class ChatConsumer(WebsocketConsumer):


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(str(self.scope['headers']).split('sessionid=')[1].split("'")[0])
        session_key = str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        if Session.objects.filter(session_key=session_key).count() == 1:
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)

            # We got the user, now check the chat room availabilty for the user
            if TwoGroup.objects.filter(channel_name = self.room_name).count() == 0:
                # If no chat room is found, return the user request
                print('No chat room found')
                return
             
            chat_room = TwoGroup.objects.get(channel_name = self.room_name)

            # now, we have the chat room, see whether the user is Professional or Fresher
            # If the user is not present in any of the uses, return empty
            if chat_room.prof.id != user.id and chat_room.fresher.id != user.id:
                print('Not found',chat_room.prof.id,chat_room.fresher.id,user.id)
                return
            else:
                print('Chat joined')

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
    # h7sc90o8n7buen965ydqrq2uspggy4nf
            self.accept()

        # if user object is not found return
        print('User not found')
        return 

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_channel    = text_data_json['user']
        room    = text_data_json['room']

        str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        session_key = str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        if Session.objects.filter(session_key=session_key).count() == 1:
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)


            try:
                room = ''

                if TwoGroup.objects.filter(channel_name = room, prof = user).count() != 0:
                    room = TwoGroup.objects.get(channel_name = room,  prof = user)

                elif TwoGroup.objects.filter(channel_name = room, fresher = user).count() != 0:
                    room = TwoGroup.objects.get(channel_name = room, fresher = user)

                Messages(
                message    = message,
                sender     = user,
                chatgroup  = room
                ).save()

                # Save data to database 
                


                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'time': str(timezone.now().strftime("%I:%M:%S %p")),
                        'user': user
                    }
                )
            except:
                return
        
        return

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user    = event['user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'time': str(timezone.now().strftime("%I:%M:%S %p")),
            'user': user
        }))






