""" Tests for botland.bots.models """

from django.test import TestCase
from botland.bots.models import Bot
from botland.chats.models import Chat, User


# Create your model tests here.
class BotTests(TestCase):
    """Bot model test"""

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

        return super().setUp()

    def test_chat_count(self) -> None:
        """Test bot.chat_count"""

        # Test before adding chat
        self.assertEqual(self.bot.chat_count, 0)

        # Chat
        chat = Chat(
            bot=self.bot,
            user=self.user,
            title="Test chat",
        )
        chat.save()

        # Test after adding chat
        self.assertEqual(self.bot.chat_count, 1)
