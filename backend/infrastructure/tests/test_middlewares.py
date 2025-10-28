from django.test import TestCase, override_settings
from accounts.models import User



class MaintenanceModeMiddlewareTests(TestCase):
    @override_settings(MAINTENANCE_MODE=False)
    def test_pass_through_when_maintenance_disabled(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ok")

    @override_settings(MAINTENANCE_MODE=True)
    def test_returns_503_when_maintenance_enabled(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 503)
        self.assertEqual(res.content, b"Site is under maintenance")

    @override_settings(MAINTENANCE_MODE=True)
    def test_middleware_short_circuits_before_view(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 503)
        self.assertEqual(res.content, b"Site is under maintenance")


class UserLanguageMiddlewareTests(TestCase):
    def test_accept_language_header_wins(self):
        """
        If client sends Accept-Language, that value should become
        request.LANGUAGE_CODE and active translation.
        """
        res = self.client.get("/ping/", HTTP_ACCEPT_LANGUAGE="uk")

        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertEqual(data["lang"], "uk")
        self.assertEqual(data["active_lang"], "uk")

    def test_falls_back_to_user_preferred_language_when_no_header(self):
        """
        If there's no Accept-Language header, middleware should use the
        authenticated user's preferred_language.
        """
        user = User.objects.create_user(
            username="ivan",
            password="pass12345",
            preferred_language="uk",
        )

        self.client.force_login(user)

        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertEqual(data["lang"], "uk")
        self.assertEqual(data["active_lang"], "uk")

    def test_defaults_to_en_when_no_header_and_anonymous(self):
        """
        If no Accept-Language and user is anonymous (or has no preferred_language),
        we expect default 'en'.
        """
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertEqual(data["lang"], "en")
        self.assertEqual(data["active_lang"], "en")