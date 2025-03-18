"""Consumers for al_wazeer.messages"""

import json
from typing import Any, Dict, List, Optional, Union
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from huggingface_hub import AsyncInferenceClient

from al_wazeer.assistants.models import Assistant
from al_wazeer.chats.models import Chat
from al_wazeer.messages.models import Message
from al_wazeer.messages.serializers import MessageSerializer
from al_wazeer.users.models import User


# Create your consumers here.
class MessageConsumer(AsyncJsonWebsocketConsumer):
    """Send and receive messages"""

    user: User
    model: Chat
    assistant: Assistant
    history: List[Dict[str, str]]
    client = AsyncInferenceClient()

    async def connect(self) -> None:
        """Connect to chat"""

        # User
        self.user = self.scope["user"]

        # Check is the user is authenticated
        if not self.user.is_authenticated:
            await self.close(code=401, reason="Authentication")
            return

        # Chat
        self.object = await self.get_object()

        # Check is the user is owner of the chat
        if not self.user.pk == self.object.user_id:
            await self.close(code=403, reason="Authorization")
            return

        # Assistant
        self.assistant = await self.get_assistant()

        # Chat history
        self.history = await self.get_chat_history()

        # Accept connection
        await self.accept()

    async def decode_json(self, text_data):
        """Decode and validate incoming data"""

        return await self.serialize_message(json.loads(text_data))

    async def receive_json(self, content: Optional[Dict[str, str]], **kwargs) -> None:
        """Receive messages"""

        raise NotImplementedError(f"receive_json is not implemented for {__name__}")

    async def create_assistant_message(self) -> Dict[str, str]:
        """Generate and create assistant message and add it to chat history"""

        message = await self.serialize_message(
            await self.create_message(
                chat_id=self.object.pk,
                assistant_id=self.assistant.pk,
                content=await self.generate_response(self.assistant.model),
            )
        )

        # Add assistant response to chat history
        self.history.append({"content": message["content"], "role": "assistant"})

        return message

    async def create_user_message(self, content: Dict[str, str]) -> Dict[str, str]:
        """Create user message and add it to chat history"""

        message = await self.serialize_message(
            await self.create_message(
                chat_id=self.object.pk,
                content=content["content"],
            )
        )

        # Add user message to chat history
        self.history.append({"content": message["content"], "role": "user"})

        return message

    async def generate_response(self, model: str) -> str:
        """Generates assistant response"""

        response = await self.client.chat_completion(
            messages=self.history, model=model, max_tokens=2048
        )

        return response.choices[0].message.content

    @database_sync_to_async
    def create_message(self, **kwargs) -> Message:
        """Creates chat message"""

        return Message.objects.create(user_id=self.user.pk, **kwargs)

    @database_sync_to_async
    def get_assistant(self) -> Assistant:
        """Get assistant instance"""

        return self.object.assistant

    @database_sync_to_async
    def get_object(self) -> Chat:
        """Get model object"""

        return self.model.objects.get(pk=self.scope["url_route"]["kwargs"]["id"])

    @database_sync_to_async
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get chat history"""

        history = [{"content": self.object.role, "role": "system"}]
        history.extend(
            [
                {
                    "role": "assistant" if message.assistant else "user",
                    "content": message.content,
                }
                for message in self.object.messages.all()
            ]
        )

        return history

    @database_sync_to_async
    def serialize_message(
        self,
        data: Union[Message, Dict[str, Any]],
    ) -> Union[Dict[str, str], None]:
        """Serializes message"""

        if isinstance(data, dict):
            if data["type"] == "retry":
                print("Retrying")
                return data

            serializer = MessageSerializer(data=data["message"])

            # Data validation
            if serializer.is_valid(raise_exception=False):
                return serializer.validated_data

            return None

        elif isinstance(data, Message):
            return MessageSerializer(instance=data).data

        return None
