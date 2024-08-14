""" Tests for botland.messages.models """

from django.test import TestCase
from botland.messages.models import Message


# Create your model tests here.
class MessageTests(TestCase):
    """Message model test"""

    def setUp(self) -> None:
        """Setup test data"""

        message = Message()
        message.save()

        return super().setUp()
