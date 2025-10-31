from typing import Dict, Any
from django.test import TestCase
from rest_framework import serializers
from faker import Faker
from accounts.models import User
from .factories import UserFactory, GameTokenFactory
from accounts.serializers import MeSerializer, UserRegistrationSerializer, GameTokenSerializer


"""
Serializer tests for `MeSerializer` (read-only profile) and
`UserRegistrationSerializer` (signup).

Uses Faker for realistic data and factory_boy for concise model setup.
"""
class MeSerializerTests(TestCase):
    """
    Tests for the read-only serializer that exposes the current user profile.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        Faker.seed(1337)
        cls.fake = Faker()
        cls.user = User.objects.create_user(
            username="player1",
            email="player1@example.com",
            password="supersecret123",
            first_name="Alex",
            last_name="Stone",
        )

    def test_serialization_includes_expected_fields(self) -> None:
        """
        The serializer must expose only the whitelisted fields.
        """
        data = MeSerializer(self.user).data
        self.assertEqual(
            set(data.keys()),
            {"id", "username", "email", "first_name", "last_name"},
        )

    def test_serialization_values_are_correct(self) -> None:
        """
        Serialized values must match the instance.
        """
        data = MeSerializer(self.user).data
        self.assertEqual(data["id"], self.user.id)
        self.assertEqual(data["username"], "player1")
        self.assertEqual(data["email"], "player1@example.com")
        self.assertEqual(data["first_name"], "Alex")
        self.assertEqual(data["last_name"], "Stone")

    def test_password_is_never_exposed(self) -> None:
        """
        Sensitive fields like `password` must not be included in output.
        """
        data = MeSerializer(self.user).data
        self.assertNotIn("password", data)

    def test_update_is_not_supported(self) -> None:
        """
        The serializer is read-only: calling `save()` with an instance must raise.
        """
        payload: Dict[str, Any] = {
            "email": "newmail@example.com",
            "first_name": "A",
            "last_name": "Player",
            "username": "player1",
        }
        ser = MeSerializer(instance=self.user, data=payload, partial=True)
        self.assertTrue(ser.is_valid(), ser.errors)
        with self.assertRaises(serializers.ValidationError):
            ser.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "player1@example.com")
        self.assertEqual(self.user.first_name, "Alex")
        self.assertEqual(self.user.last_name, "Stone")

    def test_creation_is_not_supported_with_read_only_fields(self) -> None:
        """
        Creating instances via this serializer must raise a ValidationError.
        """
        ser = MeSerializer(data={"username": "someone"})
        self.assertTrue(ser.is_valid(), ser.errors)
        with self.assertRaises(serializers.ValidationError):
            ser.save()


class UserRegistrationSerializerTests(TestCase):
    """
    Tests for the signup serializer that creates a user and hashes the password.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        Faker.seed(1337)
        cls.fake = Faker()
        cls.existing = UserFactory(username="takenuser", email="taken@example.com")

    # ------------ helpers ------------

    def _make_payload(self, **overrides: Any) -> Dict[str, Any]:
        """
        Build a valid registration payload using Faker; allow overrides per test.
        Keeping password deterministic for stable assertions.
        """
        password = "StrongPass123"
        base = {
            "username": self.fake.unique.user_name(),
            "email": self.fake.unique.email(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "password": password,
            "password2": password,
        }
        base.update(overrides)
        return base

    # ------------ tests ------------

    def test_valid_payload_creates_user_and_hashes_password(self) -> None:
        payload = self._make_payload()
        ser = UserRegistrationSerializer(data=payload)
        self.assertTrue(ser.is_valid(), ser.errors)

        user = ser.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, payload["username"])
        self.assertEqual(user.email, payload["email"])

        self.assertNotEqual(user.password, payload["password"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_password2_mismatch_raises_validation_error(self) -> None:
        payload = self._make_payload(password2="different123")
        ser = UserRegistrationSerializer(data=payload)
        with self.assertRaises(serializers.ValidationError) as cm:
            ser.is_valid(raise_exception=True)
        self.assertIn("password2", cm.exception.detail)
        self.assertIn("Passwords do not match.", str(cm.exception.detail["password2"][0]))

    def test_duplicate_email_rejected(self) -> None:
        # Collides with `taken@example.com` from setUpTestData
        payload = self._make_payload(email="taken@example.com")
        ser = UserRegistrationSerializer(data=payload)
        self.assertFalse(ser.is_valid())
        self.assertIn("email", ser.errors)
        self.assertIn("already in use", ser.errors["email"][0])

    def test_duplicate_username_rejected(self) -> None:
        # Collides with "takenuser" from setUpTestData
        payload = self._make_payload(username="takenuser")
        ser = UserRegistrationSerializer(data=payload)
        self.assertFalse(ser.is_valid())
        self.assertIn("username", ser.errors)
        self.assertIn("taken", ser.errors["username"][0].lower())

    def test_password_min_length_enforced(self) -> None:
        payload = self._make_payload(password="1234567", password2="1234567")
        ser = UserRegistrationSerializer(data=payload)
        self.assertFalse(ser.is_valid())
        self.assertIn("password", ser.errors)
        self.assertTrue(
            "8" in ser.errors["password"][0] or "at least" in ser.errors["password"][0].lower()
        )

    def test_required_fields(self) -> None:
        ser = UserRegistrationSerializer(data={})
        self.assertFalse(ser.is_valid())
        for field in ["username", "email", "password", "password2"]:
            self.assertIn(field, ser.errors)

    def test_password2_removed_from_validated_data(self) -> None:
        payload = self._make_payload()
        ser = UserRegistrationSerializer(data=payload)
        self.assertTrue(ser.is_valid(), ser.errors)
        self.assertNotIn("password2", ser.validated_data)

    def test_email_format_validation(self) -> None:
        payload = self._make_payload(email="not-an-email")
        ser = UserRegistrationSerializer(data=payload)
        self.assertFalse(ser.is_valid())
        self.assertIn("email", ser.errors)



class GameTokenSerializerTests(TestCase):
    """
    Tests for GameTokenSerializer, which is read-only and returns token data.
    """

    def test_serialization_includes_expected_fields(self) -> None:
        token = GameTokenFactory(is_active=True)

        data = GameTokenSerializer(token).data

        self.assertEqual(
            set(data.keys()),
            {"id", "value", "is_active", "generated_at"},
        )

        self.assertEqual(data["id"], token.id)
        self.assertEqual(data["value"], token.value)
        self.assertEqual(data["is_active"], token.is_active)

        # generated_at should be serialized to string (ISO-ish)
        self.assertIsNotNone(token.generated_at)
        self.assertIsInstance(data["generated_at"], str)

    def test_serializer_is_read_only_on_create(self) -> None:
        """
        Creating a GameToken through this serializer should raise,
        because it's meant to be output-only.
        """
        ser = GameTokenSerializer(data={})
        self.assertTrue(ser.is_valid(), ser.errors)

        with self.assertRaises(serializers.ValidationError):
            ser.save()

    def test_serializer_is_read_only_on_update(self) -> None:
        """
        Updating an existing GameToken through this serializer should raise.
        """
        token = GameTokenFactory(is_active=True)

        payload = {
            "is_active": False,
            "value": "hacked",
        }

        ser = GameTokenSerializer(instance=token, data=payload, partial=True)
        self.assertTrue(ser.is_valid(), ser.errors)

        with self.assertRaises(serializers.ValidationError):
            ser.save()

        # and confirm DB didn't get changed
        token.refresh_from_db()
        self.assertTrue(token.is_active)
        self.assertNotEqual(token.value, "hacked")