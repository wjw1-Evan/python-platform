"""
WebSocket消费者 - 实时通知
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.notifications.models import Notification
from apps.users.models import User
from bson import ObjectId


class NotificationConsumer(AsyncWebsocketConsumer):
    """通知WebSocket消费者"""
    
    async def connect(self):
        """连接"""
        self.user_id = self.scope['url_route']['kwargs'].get('user_id')
        self.company_id = self.scope['url_route']['kwargs'].get('company_id')
        self.room_group_name = f'notifications_{self.company_id}_{self.user_id}'
        
        # 加入组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """断开连接"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """接收消息"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
        except:
            pass
    
    async def notification_message(self, event):
        """发送通知消息"""
        message = event['message']
        await self.send(text_data=json.dumps(message))
