""" Consumers for botland.messages """

import json
from typing import Dict, List
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from huggingface_hub import AsyncInferenceClient
from botland.bots.models import Bot
from botland.chats.models import Chat
from botland.messages.models import Message
from botland.messages.serializers import MessageCreateSerializer
from botland.users.models import User


# Create your consumers here.
class AsyncMessageConsumer(AsyncJsonWebsocketConsumer):
    """Message AsyncJsonWebsocketConsumer"""

    # HF AsyncInferenceClient
    client = AsyncInferenceClient()

    async def connect(self) -> None:
        """Connect"""

        # User
        user = self.scope["user"]

        # Check is the user is authenticated
        if not user.is_authenticated:
            # Close the connection
            await self.close(code=401, reason="Authentication")

            return

        # Chat
        self.chat = await self.get_chat()

        # Check is the user is owner of the chat
        if not user.id == self.chat.user_id:
            # Close the connection
            await self.close(code=403, reason="Authorization")

            return

        # User
        self.user = await self.get_user(self.scope["user"].id)

        # Chatbot
        self.bot = await self.get_bot()

        # Chat history
        self.history = await self.get_chat_history()

        # Accept connection
        await self.accept()

    async def decode_json(self, text_data):
        """Validate incoming data"""

        data = json.loads(text_data)
        data["user"] = self.user

        serializer = MessageCreateSerializer(data=data)

        # Data validation
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data

    async def receive_json(self, content: Dict[str, str], **kwargs) -> None:
        """Receive data"""

        # User message
        message = await self.create_message(
            content=content["content"],
            user=self.user,
        )

        # Add to chat history
        self.history.append({"role": "user", "content": message.content})
        print(self.history)

        await self.send_json(
            {
                "type": "message.user",
                "message": {
                    "id": message.id,
                    "user": self.user.id,
                    "content": message.content,
                    "is_read": message.is_read,
                    "is_starred": message.is_starred,
                    "is_edited": message.is_edited,
                    "created_at": str(message.created_at),
                    "updated_at": str(message.updated_at),
                },
            }
        )

        # Bot's response
        response = await self.client.chat_completion(
            model=self.bot.model,
            messages=self.history,
            max_tokens=2048,
        )

        # Bot's message
        bot_message = await self.create_message(
            content=response.choices[0].message.content
        )

        # Add to chat history
        self.history.append({"role": "assistant", "content": bot_message.content})
        print(self.history)

        # Return the result
        await self.send_json(
            {
                "type": "message.bot",
                "message": {
                    "id": bot_message.id,
                    "bot": bot_message.bot_id,
                    "content": bot_message.content,
                    "is_read": bot_message.is_read,
                    "is_starred": bot_message.is_starred,
                    "is_edited": bot_message.is_edited,
                    "created_at": str(bot_message.created_at),
                    "updated_at": str(bot_message.updated_at),
                },
            }
        )

    @database_sync_to_async
    def create_message(self, content: str, user=None) -> Message:
        """Creates chat message"""

        return Message.objects.create(
            user=self.user.id if user is not None else None,
            bot=self.bot if user is None else None,
            chat=self.chat,
            content=content,
        )

    @database_sync_to_async
    def get_bot(self) -> Bot:
        """Return Chat's Bot instance"""

        return Bot.objects.get(pk=self.chat.bot_id)

    @database_sync_to_async
    def get_chat(self) -> Chat:
        """Return Chat instance"""

        return Chat.objects.get(pk=self.scope["url_route"]["kwargs"]["id"])

    @database_sync_to_async
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Returns Chat history"""

        history = [{"role": "system", "content": "You are a helpful assistant."}]
        history.extend(
            [
                {
                    "role": "assistant" if msg.bot else "user",
                    "content": msg.content,
                }
                for msg in self.chat.messages.all()
            ]
        )

        return history

    @database_sync_to_async
    def get_user(self, id: int) -> User:
        """Returns user instance"""

        return User.objects.get(pk=id)
