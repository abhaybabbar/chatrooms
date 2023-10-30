from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('hello')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.admin_message',
                'message': 'New User has joined our chat'
            }
        )
    
    
    async def chat_admin_message(self, event):
        await self.send(json.dumps({
            'username': 'Admin',
            'message': event['message']
        }))
        
        
    
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.admin_message',
                'message': 'Some User has disconnected our chat'
            }
        )
        