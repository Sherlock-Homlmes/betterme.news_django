import json
import datetime
import pytz

from channels.generic.websocket import AsyncWebsocketConsumer

from database.redis.discord_user import DiscordUserOauth
from database.connector.mongo_meili_chat import add_employee_chat,all_chat

class EmployeeChat(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if self.room_name in all_chat:
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            #confirm connecting
            #await self.send(text_data=json.dumps({'message': f'you are connect to {self.room_name}'}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_token = text_data_json["user_token"]

        current_user = DiscordUserOauth.get_user(user_token)
        if current_user:
            # Send message to room group
            send_data =  {
                    'type': 'chat_message',

                    #'channel':self.room_name,
                    'user_id': current_user.id,
                    'user_name': current_user.username,
                    'user_avatar': current_user.avatar_url,
                    'message': message,
                    'time_stamp': now_time(),
                }
            add_employee_chat(send_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                send_data
            )

    # Receive message from room group
    async def chat_message(self, event):
        user_name = event['user_name']
        user_avatar = event['user_avatar']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user_name': user_name,
            'user_avatar': user_avatar,
            'message': message,
        }))

def now_time():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Ho_Chi_Minh"))
    return [pst_now.year,pst_now.month,pst_now.day,pst_now.hour,pst_now.minute]

