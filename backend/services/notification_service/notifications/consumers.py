"""
WebSocket消费者 - 实时通知推送
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    """通知WebSocket消费者"""
    
    async def connect(self):
        """建立连接"""
        # 从查询参数获取token
        token = self.scope['query_string'].decode().split('token=')[-1].split('&')[0]
        
        if not token:
            await self.close()
            return
        
        # 验证token并获取用户信息
        user_info = await self.get_user_from_token(token)
        if not user_info:
            await self.close()
            return
        
        self.user_id = user_info['user_id']
        self.company_id = user_info['company_id']
        
        # 加入用户专属的房间组
        self.room_group_name = f'notifications_{self.company_id}_{self.user_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """断开连接"""
        if hasattr(self, 'room_group_name'):
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
        except json.JSONDecodeError:
            pass
    
    async def notification_message(self, event):
        """接收通知消息"""
        message = event['message']
        await self.send(text_data=json.dumps(message))
    
    @database_sync_to_async
    def get_user_from_token(self, token):
        """从token中获取用户信息，从数据库读取company_id"""
        try:
            access_token = AccessToken(token)
            user_id = access_token.get('user_id')
            
            if not user_id:
                return None
            
            # 从数据库读取用户的company_id
            from services.company_service.companies.models import UserCompany
            
            user_company = UserCompany.objects.filter(
                user_id=user_id,
                is_deleted=False,
                is_active=True
            ).first()
            
            company_id = user_company.company_id if user_company else None
            
            return {
                'user_id': user_id,
                'company_id': company_id,
            }
        except (TokenError, Exception):
            return None
