from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from authentication.models import User
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user = User.objects.get(id=self.room_name)
        if(user.user_type == 2):
            self.room_group_name = 'delivery_person'
        else:
            self.room_group_name = 'manager_'+str(self.room_name)
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
        message = text_data_json['message']
        print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
