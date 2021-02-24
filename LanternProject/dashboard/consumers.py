import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from core.models import CoreRoom as Room


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.hall_name = self.scope['url_route']['kwargs']['hall_name']
        self.hall_group_name = 'chat_%s' % self.hall_name

        # Join hall group
        async_to_sync(self.channel_layer.group_add)(
            self.hall_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave hall group
        async_to_sync(self.channel_layer.group_discard)(
            self.hall_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        id = text_data_json['id']
        room_key = text_data_json['room_key']
        status = text_data_json['status']
        date_opened = text_data_json['date_opened']
        user_id = text_data_json['user_id']

        # Save the message
        # hall_id = Room.objects.get(hall_key = hall_key).id
        # Message(content = message, ip = None, datetime = dt.now(), sender = sender, hall_id = hall_id).save()

        # Send message to hall group
        async_to_sync(self.channel_layer.group_send)(
            self.hall_group_name,
            {
                'type': 'hall_gate',
                'id': id,
                'room_key': room_key,
                'status': status,
                'date_opened': date_opened,
                'user_id': user_id,
            }
        )        

    # Receive message from hall group
    def hall_gate(self, event):

        id = event['id']
        room_key = event['room_key']
        status = event['status']
        date_opened = event['date_opened']
        user_id = event['user_id']

        # Send message to WebSocket
        self.send(text_data = json.dumps({
            'id': id,
            'room_key': room_key,
            'status': status,
            'date_opened': date_opened,
            'user_id': user_id,
        }))
