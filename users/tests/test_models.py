""" Tests for botland.users.models """

from django.test import TestCase
from botland.users.models import User


# Create your model tests here.
class UserTests(TestCase):
    """User model test"""

    def setUp(self) -> None:
        """Setup test data"""

        user = User(username="test", email="test@example.com")
        user.save()

        return super().setUp()
