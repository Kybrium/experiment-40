from django.test import TestCase
from accounts.models import User
from accounts.serializers import MeSerializer
from rest_framework import serializers


class MeSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="player1",
            email="player1@example.com",
            password="supersecret123",
            first_name="Alex",
            last_name="Stone",
        )

    def test_serialization_includes_expected_fields(self):
        """Serializer exposes only the whitelisted fields."""
        data = MeSerializer(self.user).data
        self.assertEqual(
            set(data.keys()),
            {"id", "username", "email", "first_name", "last_name"},
        )

    def test_serialization_values_are_correct(self):
        """Serialized data matches the instance values."""
        data = MeSerializer(self.user).data
        self.assertEqual(data["id"], self.user.id)
        self.assertEqual(data["username"], "player1")
        self.assertEqual(data["email"], "player1@example.com")
        self.assertEqual(data["first_name"], "Alex")
        self.assertEqual(data["last_name"], "Stone")

    def test_password_is_never_exposed(self):
        """Sensitive fields like password are not included."""
        data = MeSerializer(self.user).data
        self.assertNotIn("password", data)

    def test_update_is_not_supported(self):
        """
        Since MeSerializer overrides update() to raise, calling save() with an
        instance must raise ValidationError even if data is 'valid'.
        """
        payload = {
            "email": "newmail@example.com",
            "first_name": "A",
            "last_name": "Player",
            "username": "player1",
        }
        ser = MeSerializer(instance=self.user, data=payload, partial=True)
        self.assertTrue(ser.is_valid(), ser.errors)
        with self.assertRaises(serializers.ValidationError):
            ser.save()

        # Ensure nothing changed in DB
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "player1@example.com")
        self.assertEqual(self.user.first_name, "Alex")
        self.assertEqual(self.user.last_name, "Stone")

    def test_creation_is_not_supported_with_read_only_fields(self):
        """
        This is read-only serializer so the exception
        must be raised.
        """
        ser = MeSerializer(data={"username": "someone"})
        self.assertTrue(ser.is_valid(), ser.errors)
        with self.assertRaises(serializers.ValidationError):
            ser.save()