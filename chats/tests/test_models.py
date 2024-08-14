""" Tests for botland.chats.models """

from django.test import TestCase
from botland.chats.models import Chat


# Create your model tests here.
class ChatTests(TestCase):
    """Chat model tests"""

    def setUp(self) -> None:
        """Setup test data"""

        chat = Chat()
        chat.save()

        return super().setUp()
