import json
from typing import List

from channels.generic.websocket import AsyncWebsocketConsumer


class ScoreConsumer(AsyncWebsocketConsumer):
    board_ids: List[str] = []

    async def connect(self):
        self.board_ids = self.scope["url_route"]["kwargs"]["board_ids"].split(",")

        for board_id in self.board_ids:
            await self.channel_layer.group_add(board_id, self.channel_name)

        # Join room group
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        for board_id in self.board_ids:
            await self.channel_layer.group_discard(board_id, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("message:", message)

        # Sends an event to a group. The type of event corresponds to a method that
        # should be invoked on consumers that receive an event.
        # chat.message to converted to chat_message
        for board_id in self.board_ids:
            await self.channel_layer.group_send(
                board_id, {"type": "chat.message", "message": message}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to the WebSocket of the client associated with this consumer.
        await self.send(text_data=json.dumps({"message": message}))
