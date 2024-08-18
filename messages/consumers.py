""" Consumers for botland.messages """

import json
from typing import Dict, List
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from huggingface_hub import AsyncInferenceClient
from botland.bots.models import Bot
from botland.chats.models import Chat
from botland.messages.models import Message
from botland.messages.serializers import MessageSerializer


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

        # Check is the user is authenticated
        if not self.scope["user"].id == self.chat.user_id:
            await self.disconnect(code=403)

        # Chatbot
        self.bot = await self.get_bot()

        # Chat history
        self.history = await self.get_chat_history()

        # Accept connection
        await self.accept()

    async def disconnect(self, code) -> None:
        """Disconnect"""

        await super().disconnect(code)

    async def receive_json(self, content: Dict, **kwargs) -> None:
        """Receive data"""

        # User's message
        message = await self.create_message(
            content=content["content"],
            user=self.scope["user"],
        )

        # Add to chat history
        self.history.append({"role": "user", "content": message.content})

        # Bot's response
        response = await self.client.chat_completion(
            model=self.bot.slug,
            messages=self.history,
            stream=False,
        )

        # Data validation
        serializer = MessageSerializer(
            data={"content": response.choices[0].message.content},
            context={"request": self.scope},
        )

        if serializer.is_valid():
            # Bot's message
            bot_message = await self.create_message(
                content=serializer.validated_data.get("content")
            )

            # Add to chat history
            self.history.append({"role": "assistant", "content": bot_message.content})

            serializer = MessageSerializer(
                instance=bot_message,
                data=serializer.validated_data,
            )
            serializer.is_valid()

            # Return the result
            await self.send_json({"message": serializer.validated_data})
        else:
            await self.send_json({"message": serializer.errors})

    @classmethod
    async def decode_json(cls, text_data):
        """Validate incoming data"""

        serializer = MessageSerializer(data=json.loads(text_data))

        # Data validation
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data

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
