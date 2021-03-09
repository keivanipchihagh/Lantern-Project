import json
from datetime import datetime as dt
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from core.models import CoreMessage as Message
from core.models import CoreRoom as Room


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

        # id = text_data_json['id']
        # message = text_data_json['message']
        # datetime = text_data_json['datetime']
        # room_key = text_data_json['room_key']
        # sender = text_data_json['sender']
        message = text_data_json['message']

        # Save the message
        # room_id = Room.objects.get(room_key = room_key).id
        # Message(content = message, ip = None, datetime = dt.now(), sender = sender, room_id = room_id).save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'room_gate',
                # 'id': id,
                # 'message': message,
                # 'datetime': datetime,
                # 'room_key': room_key,
                # 'sender': sender,
                'message': message
            }
        )        

    # Receive message from room group
    def room_gate(self, event):

        # id = event['id']
        # message = event['message']
        # datetime = event['datetime']
        # room_key = event['room_key']
        # sender = event['sender']
        message = event['message']

        # Send message to WebSocket
        self.send(text_data = json.dumps({
            # 'id': id,
            # 'message': message,
            # 'datetime': datetime,
            # 'room_key': room_key,
            # 'sender': sender,
            'message': message
        }))
