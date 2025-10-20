from django.test import TestCase
from django.db import IntegrityError
from accounts.models import User
from .factories import UserFactory


class UserModelTests(TestCase):
    """Tests verifying basic behavior of the User model."""

    def test_create_user(self):
        """Factory creates a valid user; passwords are hashed."""
        user = UserFactory(username="player1")
        self.assertEqual(user.username, "player1")
        self.assertTrue(user.check_password("StrongPass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Superuser factory sets proper permission flags."""
        admin = User.objects.create_superuser(
            username="admin",
            password="adminpass123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.check_password("adminpass123"))

    def test_str_representation(self):
        """User string representation returns the username."""
        user = UserFactory(username="steve")
        self.assertEqual(str(user), "steve")

    def test_unique_username(self):
        """Usernames must be unique in the database."""
        UserFactory(username="alex")
        with self.assertRaises(IntegrityError):
            UserFactory(username="alex")