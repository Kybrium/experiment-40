from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from rest_framework import status
from django.urls import reverse
from faker import Faker

from accounts.views import UserView
from accounts.models import User
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
    """End-to-end tests for SimpleJWT with cookie-based storage."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="player1",
            email="player1@example.com",
            password="supersecret123",
        )
        self.obtain_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")
        self.me_url = reverse("me")

    def test_obtain_token_sets_cookies(self):
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn("access", res.data)
        self.assertNotIn("refresh", res.data)
        self.assertIn("access_token", res.cookies)
        self.assertIn("refresh_token", res.cookies)

    def test_me_requires_cookie_auth(self):
        """Unauthenticated call should 401, authenticated cookie should pass."""
        # not logged in
        res1 = self.client.get(self.me_url)
        self.assertEqual(res1.status_code, status.HTTP_401_UNAUTHORIZED)

        # login -> cookies returned
        res2 = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.client.cookies = res2.cookies

        res3 = self.client.get(self.me_url)
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(res3.data["username"], "player1")

    def test_logout_clears_cookies(self):
        """Logout should remove access/refresh cookies."""
        # login
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.client.cookies = res.cookies

        # logout
        logout_url = reverse("logout")
        res2 = self.client.post(logout_url)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.cookies["access_token"].value, "")
        self.assertEqual(res2.cookies["refresh_token"].value, "")

    def test_refresh_token_via_cookie(self):
        """Refresh view should read refresh token from cookie and set new access cookie."""
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("refresh_token", res.cookies)

        self.client.cookies = res.cookies
        res2 = self.client.post(self.refresh_url)

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", res2.cookies)
        self.assertNotIn("access", res2.data)

    def test_verify_cookie_token(self):
        """Verify view should validate access token from cookie."""
        res = self.client.post(
            self.obtain_url,
            {"username": "player1", "password": "supersecret123"},
            format="json",
        )
        self.client.cookies = res.cookies
        verify_res = self.client.post(reverse("token_verify"))

        self.assertEqual(verify_res.status_code, status.HTTP_200_OK)



class RegistrationTests(APITestCase):
    """
    Tests for POST /api/accounts/register/ handled by UserView.
    """

    @classmethod
    def setUpTestData(cls):
        Faker.seed(2025)
        cls.fake = Faker()
        # Existing user for unique constraint checks
        cls.existing = UserFactory(username="takenuser", email="taken@example.com")

    def setUp(self):
        self.register_url = reverse("register_user")
        self.me_url = reverse("me")
        self.token_verify_url = reverse("token_verify")

    def _payload(self, **overrides):
        """Builds a valid registration payload using Faker; allows overrides."""
        password = overrides.pop("password", "StrongPass123")
        payload = {
            "username": self.fake.unique.user_name(),
            "email": self.fake.unique.email(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "password": password,
            "password2": overrides.pop("password2", password),
        }
        payload.update(overrides)
        return payload

    def test_register_success_returns_user_and_tokens(self):
        """Anonymous user can register and receives JWT tokens."""
        data = self._payload()
        res = self.client.post(self.register_url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data.get("ok"))
        self.assertIn("user", res.data)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

        user_data = res.data["user"]
        self.assertEqual(
            set(user_data.keys()),
            {"id", "username", "email", "first_name", "last_name"},
        )
        self.assertEqual(user_data["username"], data["username"])
        self.assertEqual(user_data["email"], data["email"])

        # Verify token works
        access = res.data["access"]
        self.client.cookies["access_token"] = access
        verify = self.client.post(self.token_verify_url)
        self.assertEqual(verify.status_code, status.HTTP_200_OK)

        # Can use token to access /me/
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        me = self.client.get(self.me_url)
        self.assertEqual(me.status_code, status.HTTP_200_OK)
        self.assertEqual(me.data["username"], data["username"])

    def test_register_hashes_password(self):
        """Ensure password is securely hashed in DB."""
        data = self._payload(password="supersecret123")
        res = self.client.post(self.register_url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(username=data["username"])
        self.assertTrue(user.check_password("supersecret123"))
        self.assertNotEqual(user.password, "supersecret123")

    def test_register_password_mismatch(self):
        """Password and password2 mismatch should trigger 400."""
        data = self._payload(password="StrongPass123", password2="different123")
        res = self.client.post(self.register_url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password2", res.data)

    def test_register_password_min_length(self):
        """Reject passwords shorter than 8 characters."""
        data = self._payload(password="1234567", password2="1234567")
        res = self.client.post(self.register_url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", res.data)

    def test_register_duplicate_username(self):
        """Username must be unique."""
        data = self._payload(username="takenuser")
        res = self.client.post(self.register_url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", res.data)

    def test_register_duplicate_email(self):
        """Email must be unique."""
        data = self._payload(email="taken@example.com")
        res = self.client.post(self.register_url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)

    def test_post_does_not_require_auth_but_get_does(self):
        """
        POST /register/ must allow unauthenticated users (AllowAny),
        while GET /me/ must require authentication.
        """
        res = self.client.post(self.register_url, self._payload(), format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # unauthenticated GET /me/ should be 401
        self.client.credentials()
        res2 = self.client.get(self.me_url)
        self.assertEqual(res2.status_code, status.HTTP_401_UNAUTHORIZED)