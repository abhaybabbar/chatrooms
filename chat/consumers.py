from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope["user"]
        print("username", self.user)
        if not self.user.is_authenticated:
            await self.close()
        
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.admin_message',
                'message': f'{self.user} has joined our chat'
            }
        )
    
    
    async def chat_admin_message(self, event):
        await self.send(json.dumps({
            'username': 'Admin',
            'message': event['message']
        }))
        
    
    async def chat_message(self, event):
        await self.send(json.dumps({
            'username': event['username'],
            'message': event['message']
        }))
        
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # username = text_data_json['username']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': self.user.username
            }
        )
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.admin_message',
                'message': f'{self.user} has disconnected our chat'
            }
        )
        