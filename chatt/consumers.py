# Someons sample code for refrence
# https://stackoverflow.com/questions/56096886/one-django-channels-websocket-consumer-used-across-whole-site
# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):

#         other_user = self.scope['url_route']['kwargs']['username']
#         me = self.scope['user']
#         thread_obj = await self.get_thread(me, other_user)
#         self.thread_obj = thread_obj
#         chat_room = f"thread_{thread_obj.id}"
#         self.chat_room = chat_room
#         # below creates the chatroom
#         await self.channel_layer.group_add(
#             chat_room,
#             self.channel_name
#         )

#         await self.send({
#             "type": "websocket.accept"
#         })

#     async def websocket_receive(self, event):
#         # when a message is recieved from the websocket
#         print("receive", event)

#         message_type = json.loads(event.get('text','{}')).get('type')
#         if message_type == "notification_read":
#             user = self.scope['user']
#             username = user.username if user.is_authenticated else 'default'
#             # Update the notification read status flag in Notification model.
#             notification = Notification.objects.filter(notification_user=user).update(notification_read=True)
#             print("notification read")
#             return

#         front_text = event.get('text', None)
#         if front_text is not None:
#             loaded_dict_data = json.loads(front_text)
#             msg =  loaded_dict_data.get('message')
#             user = self.scope['user']
#             username = user.username if user.is_authenticated else 'default'
#             notification_id = 'default'
#             myResponse = {
#                 'message': msg,
#                 'username': username,
#                 'notification': notification_id,
#             }
#             print(myResponse)
#             await self.create_chat_message(user, msg)
#             other_user = self.scope['url_route']['kwargs']['username']
#             other_user = User.objects.get(username=other_user)
#             await self.create_notification(other_user, msg)

#             # broadcasts the message event to be sent, the group send layer
#             # triggers the chat_message function for all of the group (chat_room)
#             await self.channel_layer.group_send(
#                 self.chat_room,
#                 {
#                     'type': 'chat_message',
#                     'text': json.dumps(myResponse)
#                 }
#             )

#     # chat_method is a custom method name that we made
#     async def chat_message(self, event):
#         # sends the actual message
#         await self.send({
#                 'type': 'websocket.send',
#                 'text': event['text']
#         })

#     async def websocket_disconnect(self, event):
#         # when the socket disconnects
#         print('disconnected', event)

#     @database_sync_to_async
#     def get_thread(self, user, other_username):
#         return Thread.objects.get_or_new(user, other_username)[0]

#     @database_sync_to_async
#     def create_chat_message(self, me, msg):
#         thread_obj = self.thread_obj
#         return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)

#     @database_sync_to_async
#     def create_notification(self, other_user, msg):
#         last_chat = ChatMessage.objects.latest('id')
#         created_notification = Notification.objects.create(notification_user=other_user, notification_chat=last_chat)
#         return created_notification

# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import TwoGroup, Messages, OnlineStatus 
from django.utils import timezone
from datetime import datetime
from .models import MeetingChat,MeetingMessages
from pro.sample_tasks import send_email

# To keep the user online



# function to send email for the user if he recid message and offline
def send_message_notification(sender,group,message):
    # get the email of the user, is it fresher or professional
    user = ''
    last_seen = ''
    if sender == group.prof:
        user = group.fresher
        last_seen = group.fresher_lastseen

    elif sender == group.fresher:
        user = group.prof
        last_seen = group.prof_lastseen

    print('last seen',last_seen , 'message created',message.created_on)
    # check whether the user is offline, if offline send email
    if last_seen < message.created_on - timezone.timedelta(minutes = 1):

        send_email(user,'ClassFly Message','{} : {}'.format(user.first_name,message.message))

    return


class ChatConsumer(WebsocketConsumer):


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(str(self.scope['headers']).split('sessionid=')[1].split("'")[0])
        session_key = ''
        try:
            session_key = str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        except:
            # If there is no session, then it should be regarding session ID 
            if MeetingChat.objects.filter(channel_name = self.room_name, locked = False).count() == 1:
                async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
                )
                self.accept()
                return
            else:
                print('No chat room found')
                return

        if Session.objects.filter(session_key=session_key).count() !=  0:
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)

            # Create an online status or get an existing one
            try:
                OnlineStatus(user = user).save()
                print('Online status created')
            except:
                print('Old object got updated')
                online = OnlineStatus.objects.get(user = user)
                online.status_count = 0
                online.save()
            
            # predfine of chat_roo object

            chat_room = ''
            # variable to check whether the chats is for normal chatting or meeting chating
            meeting_room = False
            # We got the user, now check the chat room availabilty for the user
            if TwoGroup.objects.filter(channel_name = self.room_name).count() == 1 :
                chat_room = TwoGroup.objects.get(channel_name = self.room_name)

            elif MeetingChat.objects.filter(channel_name = self.room_name).count() == 1:
                chat_room = MeetingChat.objects.get(channel_name = self.room_name)
                meeting_room = True

            else:
                # If no chat room is found, return the user request
                print('No chat room found')
                return
            
            
            # now, we have the chat room, see whether the user is Professional or Fresher
            # If the user is not present in any of the uses, return empty
            if not meeting_room:
                if chat_room.prof.id != user.id and chat_room.fresher.id != user.id:
                    print('Not found',chat_room.prof.id,chat_room.fresher.id,user.id)
                    return
                else:
                    print('Chat joined')

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
    
            self.accept()

            return
        
        

        # if user object is not found return
        print('User not found')
        return 

    def disconnect(self, close_code):
        # Leave room group
        str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        session_key = str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        if Session.objects.filter(session_key=session_key).count() == 1:
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
            user.user_status.last_seen = timezone.now()
            user.user_status.save()


        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = ''
        status = ''
        user_channel = ''
        user_position = ''
        
        try:
            message = text_data_json['message']
        except:
            status = text_data_json['status']

        type    = text_data_json['type']
        user_channel    = text_data_json['room']
        user_position   = text_data_json['user']
        
        print('All values : ',type,message,status,user_channel,user_position)

        str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        session_key = str(self.scope['headers']).split('sessionid=')[1].split("'")[0]
        if Session.objects.filter(session_key=session_key).count() == 1:
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)

        
            room = ''
            if type == 'chat_message' or type == 'status':
                if  user_position == 'prof' and TwoGroup.objects.filter(channel_name = user_channel, prof = user).count() != 0:
                    print('First If done')
                    room = TwoGroup.objects.get(channel_name = user_channel,  prof = user)

                elif user_position == 'fresher' and TwoGroup.objects.filter(channel_name = user_channel, fresher = user).count() != 0:
                    print("Second If done")
                    room = TwoGroup.objects.get(channel_name = user_channel, fresher = user)
                else:
                    print('line 225,No user room match with user_position')
                    return

            elif type == 'meet_message' and MeetingChat.objects.filter(channel_name = user_channel).count() == 1:
                print('line 229, meeting found')
                room = MeetingChat.objects.get(channel_name = user_channel).get_user(user)
                if not room:
                    print('No user room match with user_position')
                    return


            else:
                print('No user room match with user_position')
                return

            print('Type: ',type)
            print("type == 'chat_message'",type == 'chat_message')
            print("type == 'status'",type == 'status')
            
            # Send status for room group
            if type == 'status':
                print('Elif entered')

                # update self user online status
                online_status = OnlineStatus.objects.get(user = user)
                online_status.status_count += 1
                online_status.save()

                
                # fetch the status_count of the opposite user
                status_count = 0
                last_seen = 'Chat Not opened'

                print('prof_lastseen',room.prof_lastseen)
                print('fresher_lastseen',room.fresher_lastseen)
                
                if user_position == 'prof':
                    # if the user position is "prof" then opposite user online status code, last_seen(for chatpage ) and room lastseen value for current position user
                    try:
                        print(user_position,'user_position proffesional')
                        status_count = room.fresher.user_status.status_count
                        last_seen    = str(room.fresher.user_status.last_seen.strftime("%d-%m-%Y  %I:%M:%S %p"))
                        
                        room.prof_lastseen = timezone.now()
                        room.save()
                    except:
                        status_count = 0

                elif user_position == 'fresher':
                    try:
                        print(user_position,'user_position fresher')
                        status_count = room.prof.user_status.status_count
                        last_seen    = str(room.prof.user_status.last_seen.strftime("%d-%m-%Y  %I:%M:%S %p"))
                        
                        room.fresher_lastseen = timezone.now()
                        room.save()
                    except:
                        status_count = 0
                
                print('prof_lastseen',room.prof_lastseen)
                print('fresher_lastseen',room.fresher_lastseen)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': type,
                        'status': status_count,
                        'last_seen':last_seen
                    }
                    )
            # this is for chatting
            
            elif type == 'chat_message':
                
                try:        
                    print('If and elif done')
                    # Save data to database 
                    message_object = Messages(
                    message    = message,
                    sender     = user,
                    chatgroup  = room
                    )

                    message_object.save()

                    print('Message saved successfully')

                    # if the user is not online try to send email
                    
                    send_message_notification(user,room,message_object)

                except:
                    print('Try not found ')
                    return

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': type,
                        'message': message,
                        'user': user_position
                    }
                    )

            elif type == 'meet_message':
                try:        
                    print('If and elif done')
                    # Save data to database 
                    MeetingMessages(
                    message    = message,
                    sender     = user,
                    meeting_room  = room
                    ).save()
                    print('Message saved successfully')
                    
                except:
                    print('Try not found ')
                    return

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': type,
                        'message': message,
                        'user': str(user.id),
                        'room': room.channel_name
                    }
                    )

             
            else:
                print('Wrong type of status data recived')
        else:    
            print('If condition fails, no session found')
            
        return
    
    # to update the user online status
    def status(self, event):
            self.send(text_data=json.dumps({
                'type':'status',
                'status':event['status'],
                'last_seen':event['last_seen']
            }))

    # Receive message from room group
    def chat_message(self, event):
            print('message sent sent to user')
            message = event['message']
            user    = event['user']
            

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'type':'chat_message',
                'message': message,
                'time': str(timezone.now().strftime("%I:%M:%S %p")),
                'user': user
            }))


    # Receive message from room group
    def meet_message(self, event):
        
            message = event['message']
            user    = event['user']
            room    = event['room']

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'type':'meet_message',
                'message': message,
                'time': str(timezone.now().strftime("%I:%M:%S %p")),
                'user': str(user),
                'room': room
            }))

       




