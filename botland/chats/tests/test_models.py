""" Tests for botland.chats.models """

from django.test import TestCase
from botland.bots.models import Bot
from botland.chats.models import Chat, User
from botland.messages.models import Message


# Create your model tests here.
class ChatTests(TestCase):
    """Chat model tests"""

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

        return super().setUp()

    def test_message_count(self) -> None:
        """Test chat.message_count"""

        # Test before adding message
        self.assertEqual(self.chat.message_count, 0)

        # Message
        message = Message(
            bot=self.bot,
            chat=self.chat,
            user=self.user,
            content="Test message",
        )
        message.save()

        # Test after adding message
        self.assertEqual(self.chat.message_count, 1)

    def test_unread_message_count(self) -> None:
        """Test chat.unread_message_count"""

        # Chat
        message = Message(
            bot=self.bot,
            chat=self.chat,
            user=self.user,
            content="Test message",
            is_read=True,
        )
        message.save()

        # Test before read
        self.assertEqual(self.chat.unread_message_count, 0)

        # Update message
        message.is_read = False
        message.save()

        # Test after adding message
        self.assertEqual(self.chat.unread_message_count, 1)
