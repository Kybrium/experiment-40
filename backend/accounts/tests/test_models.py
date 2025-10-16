from django.test import TestCase
from accounts.models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        """User can be created with a username and password."""
        user = User.objects.create_user(username="player1", password="strongpass123")
        self.assertEqual(user.username, "player1")
        self.assertTrue(user.check_password("strongpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Superuser has proper flags set."""
        admin = User.objects.create_superuser(username="admin", password="adminpass123")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_str_representation(self):
        """User __str__ returns username."""
        user = User.objects.create_user(username="steve", password="password")
        self.assertEqual(str(user), "steve")

    def test_unique_username(self):
        """Username must be unique."""
        User.objects.create_user(username="alex", password="pass")
        with self.assertRaises(Exception):
            User.objects.create_user(username="alex", password="anotherpass")