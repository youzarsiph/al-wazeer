""" Consumers for botland.messages """

import json
from typing import Dict, List, Union
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from huggingface_hub import AsyncInferenceClient
from botland.bots.models import Bot
from botland.chats.models import Chat
from botland.messages.models import Message
from botland.messages.serializers import MessageCreateSerializer


# Create your consumers here.
class AsyncMessageConsumer(AsyncJsonWebsocketConsumer):
    """Message AsyncJsonWebsocketConsumer"""

    # HF InferenceClient
    client = AsyncInferenceClient()

    async def connect(self) -> None:
        """Connect"""

        # Check is the user is authenticated
        if not self.scope["user"].is_authenticated:
            await self.disconnect(code=401)

        # Chat
        self.chat = await self.get_chat()

        # Check is the user is owner of the chat
        if not self.scope["user"].id == self.chat.user_id:
            await self.disconnect(code=403)

        # Chatbot
        self.bot = await self.get_bot()

        # Chat history
        self.history = await self.get_chat_history()

        # Accept connection
        await self.accept()

    async def decode_json(self, text_data):
        """Validate incoming data"""

        data = json.loads(text_data)
        data["user"] = self.scope["user"]

        serializer = MessageCreateSerializer(data=data)

        # Data validation
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data

    async def receive_json(self, content: Dict, **kwargs) -> None:
        """Receive data"""

        # User message
        message = await self.create_message(
            content=content["content"],
            user=self.scope["user"].id,
        )

        # Add to chat history
        self.history.append({"role": "user", "content": message.content})

        await self.send_json(
            {
                "type": "message.receive",
                "content": self.serialize(message),
            }
        )

        # Bot's response
        response = await self.client.chat_completion(
            model=self.bot.model,
            messages=self.history,
            stream=False,
            max_tokens=2048,
        )

        # Bot's message
        bot_message = await self.create_message(
            content=response.choices[0].message.content
        )

        # Add to chat history
        self.history.append({"role": "assistant", "content": bot_message.content})

        # Return the result
        await self.send_json(
            {
                "type": "message.receive",
                "content": self.serialize(bot_message),
            }
        )

    def serialize(
        self,
        message: Message,
    ) -> Union[Dict[str, str], List[Dict[str, str]]]:
        """Serialize messages"""

        serializer = MessageCreateSerializer(
            context={"request": self.scope},
            data={
                "id": message.pk,
                "bot": message.bot,
                "chat": message.chat,
                "content": message.content,
                "created_at": message.created_at,
                "updated_at": message.updated_at,
            },
        )

        if serializer.is_valid():
            return serializer.validated_data

        return serializer.errors

    @database_sync_to_async
    def create_message(self, content: str, user=None) -> Message:
        """Creates chat message"""

        return Message.objects.create(
            user=user,
            bot=self.bot if user is None else None,
            chat=self.chat,
            content=content,
        )

    @database_sync_to_async
    def get_chat(self) -> Chat:
        """Return Chat instance"""

        return Chat.objects.get(pk=self.scope["url_route"]["kwargs"]["id"])

    @database_sync_to_async
    def get_bot(self) -> Bot:
        """Return Chat's Bot instance"""

        return Bot.objects.get(pk=self.chat.bot_id)

    @database_sync_to_async
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Returns Chat history"""

        history = [{"role": "system", "content": "You are a helpful assistant."}]
        history.extend(
            [
                {"role": "user" if msg.user else "assistant", "content": msg.content}
                for msg in self.chat.messages.all()
            ]
        )

        return history
