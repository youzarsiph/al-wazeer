"""Consumers for al_wazeer.chats"""

from typing import Dict, Optional

from al_wazeer.chats.models import Chat
from al_wazeer.messages.consumers import MessageConsumer


# Create your views here.
class ChatMessageConsumer(MessageConsumer):
    """Consumer for sending and receiving messages for chats"""

    model = Chat

    async def receive_json(self, content: Optional[Dict[str, str]], **kwargs) -> None:
        """Send and receive messages"""

        if content is None:
            await self.close(code=1000, reason="Invalid data")
            return

        if "type" in content.keys() and content["type"] == "retry":
            try:
                response = await self.create_assistant_message()
                await self.send_json(
                    {"type": None, "generating": False, "data": response}
                )

            except Exception as error:
                await self.send_json(
                    {
                        "type": "error",
                        "generating": False,
                        "data": {"content": str(error)},
                    }
                )

            return

        # User message
        message = await self.create_user_message(content)
        await self.send_json({"type": None, "generating": True, "data": message})

        try:
            # Assistant's response
            response = await self.create_assistant_message()
            await self.send_json({"type": None, "generating": False, "data": response})

        except Exception as error:
            await self.send_json(
                {"type": "error", "generating": False, "data": {"content": str(error)}}
            )
