from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.views import UserView
from .factories import UserFactory


class MeViewTests(TestCase):
    """Tests for the /api/accounts/me/ endpoint (UserView)."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserView.as_view()
        self.user = UserFactory(
            username="player1",
            email="player1@example.com",
            first_name="Alex",
            last_name="Stone",
            password="supersecret123",
        )

    def test_me_requires_authentication(self):
        """Unauthenticated request should be 401."""
        request = self.factory.get("/api/accounts/me/")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_current_user_data(self):
        """Authenticated GET returns serialized current user."""
        request = self.factory.get("/api/accounts/me/")
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # shape
        self.assertEqual(
            set(data.keys()),
            {"id", "username", "email", "first_name", "last_name"},
        )

        # values
        self.assertEqual(data["id"], self.user.id)
        self.assertEqual(data["username"], "player1")
        self.assertEqual(data["email"], "player1@example.com")
        self.assertEqual(data["first_name"], "Alex")
        self.assertEqual(data["last_name"], "Stone")


class JWTFlowTests(APITestCase):
    """
    End-to-end tests for SimpleJWT:
    - token obtain pair
    - refresh
    - verify
    - use Bearer token to access /me
    """

    def setUp(self):
        self.user = UserFactory(
            username="player1",
            email="player1@example.com",
            first_name="Alex",
            last_name="Stone",
            password="supersecret123",
        )
        self.obtain_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")
        self.verify_url = reverse("token_verify")
        self.me_url = reverse("me")

    def test_obtain_token_pair_success(self):
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_obtain_token_pair_invalid_credentials(self):
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        # first obtain
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        refresh = res.data["refresh"]

        res2 = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertIn("access", res2.data)

    def test_verify_token(self):
        # obtain -> verify access
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        access = res.data["access"]

        res2 = self.client.post(self.verify_url, {"token": access}, format="json")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

    def test_access_protected_me_endpoint(self):
        # obtain -> use Authorization header
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        access = res.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        res2 = self.client.get(self.me_url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["username"], "player1")