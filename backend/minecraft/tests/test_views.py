from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
import requests

from minecraft.views import LinkMinecraftAccountView
from minecraft.models import MinecraftAccount
from .factories import UserFactory, GameTokenFactory


class LinkMinecraftAccountViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LinkMinecraftAccountView.as_view()
        self.user = UserFactory()

    def test_no_available_token_returns_403(self):
        """
        If the user has no active, unbound GameToken -> 403 and no nickname generation.
        """
        # user has 0 tokens (or only inactive/used tokens). We won't create any tokens.

        request = self.factory.get("/fake-endpoint")
        force_authenticate(request, user=self.user)

        with patch("minecraft.views.generate_unique_nickname") as mock_gen:
            response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "No available tokens. Generate one first.",
        )

        mock_gen.assert_not_called()
        self.assertEqual(MinecraftAccount.objects.count(), 0)

    def test_happy_path_creates_account_and_burns_token(self):
        """
        When a valid token exists and generate_unique_nickname returns a nickname:
        - MinecraftAccount row is created
        - token.is_active flips to False
        - response is 201 and includes expected data
        """
        # create an active token owned by this user
        token = GameTokenFactory(user=self.user, is_active=True)

        request = self.factory.get(
            "/fake-endpoint",
            {"gender": "male", "nationality": "US"},
        )
        force_authenticate(request, user=self.user)

        with patch("minecraft.views.generate_unique_nickname") as mock_gen:
            mock_gen.return_value = "alex_stone"

            response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.data

        # response content
        self.assertTrue(body["ok"])
        self.assertEqual(body["nickname"], "alex_stone")
        self.assertIsNone(body["uuid"])
        self.assertIn("account_id", body)
        self.assertIn("created_at", body)

        # DB assertions
        account = MinecraftAccount.objects.get(id=body["account_id"])
        self.assertEqual(account.nickname, "alex_stone")
        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.token, token)
        self.assertIsNone(account.uuid)
        self.assertFalse(account.is_dead)
        self.assertTrue(account.is_active)

        # token should now be burned
        token.refresh_from_db()
        self.assertFalse(token.is_active)

        # nickname generator called with provided query params
        mock_gen.assert_called_once_with(
            max_attempts=10,
            gender="male",
            nationality="US",
        )

    def test_external_request_exception_returns_502_and_does_not_consume_token(self):
        """
        If generate_unique_nickname raises a requests.RequestException:
        - return 502 with the correct error message
        - do not create account
        - do not burn the token
        """
        token = GameTokenFactory(user=self.user, is_active=True)

        request = self.factory.get("/fake-endpoint")
        force_authenticate(request, user=self.user)

        with patch("minecraft.views.generate_unique_nickname") as mock_gen:
            mock_gen.side_effect = requests.RequestException("network is down")

            response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertEqual(
            response.data["detail"],
            "Failed to generate identity. Please try again.",
        )

        # nothing created
        self.assertEqual(MinecraftAccount.objects.count(), 0)

        # token should still be active (not burned)
        token.refresh_from_db()
        self.assertTrue(token.is_active)

    def test_runtime_error_returns_502_identity_provider_error(self):
        """
        If generate_unique_nickname raises RuntimeError:
        - return 502 with 'Identity provider error.'
        - do not create account
        - token stays active
        """
        token = GameTokenFactory(user=self.user, is_active=True)

        request = self.factory.get("/fake-endpoint")
        force_authenticate(request, user=self.user)

        with patch("minecraft.views.generate_unique_nickname") as mock_gen:
            mock_gen.side_effect = RuntimeError("identity_provider_error")

            response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertEqual(
            response.data["detail"],
            "Identity provider error.",
        )

        self.assertEqual(MinecraftAccount.objects.count(), 0)

        token.refresh_from_db()
        self.assertTrue(token.is_active)

    def test_none_nickname_returns_502_and_does_not_create_account(self):
        """
        If generate_unique_nickname returns None:
        - return 502 with correct detail
        - skip account creation
        - leave token active
        """
        token = GameTokenFactory(user=self.user, is_active=True)

        request = self.factory.get("/fake-endpoint")
        force_authenticate(request, user=self.user)

        with patch("minecraft.views.generate_unique_nickname") as mock_gen:
            mock_gen.return_value = None

            response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertEqual(
            response.data["detail"],
            "Currently impossible to generate a new user, please try again later.",
        )

        # no account created
        self.assertEqual(MinecraftAccount.objects.count(), 0)

        # token should still be active (unchanged)
        token.refresh_from_db()
        self.assertTrue(token.is_active)