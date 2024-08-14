""" Tests for botland.bots.models """

from django.test import TestCase
from botland.bots.models import Bot


# Create your model tests here.
class BotTests(TestCase):
    """Bot model test"""

    def setUp(self) -> None:
        """Setup test data"""

        bot = Bot()
        bot.save()

        return super().setUp()
