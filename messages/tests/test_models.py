""" Tests for botland.messages.models """

from django.test import TestCase
from botland.bots.models import Bot
from botland.chats.models import Chat, User
from botland.messages.models import Message


# Create your model tests here.
class MessageTests(TestCase):
    """Message model test"""

    def setUp(self) -> None:
        """Setup test data"""

        # Bot
        bot = Bot(
            name="Test bot",
            model="tests/test-model",
            description="A bot for testing",
        )
        bot.save()
        self.bot = bot

        # User
        user = User(username="test", email="test@botland.com")
        user.save()
        self.user = user

        # Chat
        chat = Chat(
            bot=self.bot,
            user=self.user,
            title="Test chat",
        )
        chat.save()
        self.chat = chat

        # Message
        message = Message(
            bot=self.bot,
            chat=self.chat,
            user=self.user,
            content="Test message",
        )
        message.save()
        self.message = message

        return super().setUp()

    def test_is_edited_before_update(self) -> None:
        """Test message.is_edited before update"""

        # Test before updating the message
        self.assertFalse(self.message.is_edited)
