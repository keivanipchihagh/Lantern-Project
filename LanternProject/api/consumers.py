import json
from datetime import datetime as dt
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from core.models import CoreMessage as Message
from core.models import CoreSession as Session


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        id = text_data_json['id']
        message = text_data_json['message']
        datetime = text_data_json['datetime']
        session_key = text_data_json['session_key']
        sender = text_data_json['sender']

        # Save the message
        # session_id = Session.objects.get(session_key = session_key).id
        # Message(content = message, ip = None, datetime = dt.now(), session_id = session_id).save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': id,
                'message': message,
                'datetime': datetime,
                'session_key': session_key,
                'sender': sender,
            }
        )        

    # Receive message from room group
    def chat_message(self, event):

        id = event['id']
        message = event['message']
        datetime = event['datetime']
        session_key = event['session_key']
        sender = event['sender']

        # Send message to WebSocket
        self.send(text_data = json.dumps({
            'id': id,
            'message': message,
            'datetime': datetime,
            'session_key': session_key,
            'sender': sender,
        }))
