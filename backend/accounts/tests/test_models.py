from django.test import TestCase
from django.db import IntegrityError
from accounts.models import User, GameToken
from .factories import UserFactory, GameTokenFactory



class UserModelTests(TestCase):
    """Tests verifying basic behavior of the User model."""

    def test_create_user(self):
        """Factory creates a valid user; passwords are hashed."""
        user = UserFactory(username="player1")
        self.assertEqual(user.username, "player1")
        self.assertTrue(user.check_password("StrongPass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(user.slots, 1)
        self.assertEqual(user.preferred_language, User.LanguageChoices.ENGLISH)

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
        self.assertEqual(admin.slots, 1)
        self.assertEqual(admin.preferred_language, User.LanguageChoices.ENGLISH)

    def test_str_representation(self):
        """User string representation returns the username."""
        user = UserFactory(username="steve")
        self.assertEqual(str(user), "steve")

    def test_unique_username(self):
        """Usernames must be unique in the database."""
        UserFactory(username="alex")
        with self.assertRaises(IntegrityError):
            UserFactory(username="alex")


class GameTokenModelTests(TestCase):
    """Tests verifying behavior of the GameToken model."""

    def test_create_token_for_user(self):
        """
        Factory can create a GameToken tied to a user,
        and default flags/fields are correct.
        """
        user = UserFactory(username="player1")
        token = GameTokenFactory(user=user)

        self.assertEqual(token.user, user)

        self.assertIsInstance(token.value, str)
        self.assertGreater(len(token.value), 0)

        self.assertTrue(token.is_active)

        self.assertIsNotNone(token.generated_at)

    def test_unique_value_constraint(self):
        """
        Two different GameToken rows cannot share the same 'value'.
        """
        token1 = GameTokenFactory(value="SAME_VALUE_123")
        self.assertEqual(token1.value, "SAME_VALUE_123")

        with self.assertRaises(IntegrityError):
            GameTokenFactory(value="SAME_VALUE_123")

    def test_str_representation(self):
        """
        __str__ returns \"<user>'s Token #<id>\".
        """
        user = UserFactory(username="steve")
        token = GameTokenFactory(user=user, value="abc123")
        expected = f"{user}'s Token #{token.id}"
        self.assertEqual(str(token), expected)

    def test_is_active_flag_can_be_used_to_disable_token(self):
        """
        is_active can act as 'already used?' marker.
        """
        token = GameTokenFactory(is_active=True)
        self.assertTrue(token.is_active)

        token.is_active = False
        token.save(update_fields=["is_active"])

        refreshed = GameToken.objects.get(pk=token.pk)
        self.assertFalse(refreshed.is_active)