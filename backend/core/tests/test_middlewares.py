from django.test import TestCase, override_settings


class MaintenanceModeMiddlewareTests(TestCase):
    @override_settings(MAINTENANCE_MODE=False)
    def test_pass_through_when_maintenance_disabled(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"status": "ok"})

    @override_settings(MAINTENANCE_MODE=True)
    def test_returns_503_when_maintenance_enabled(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 503)
        self.assertEqual(res.content, b"Site is under maintenance")

    @override_settings(MAINTENANCE_MODE=True)
    def test_middleware_short_circuits_before_view(self):
        res = self.client.get("/ping/")
        self.assertNotEqual(res.content, b'{"status": "ok"}')
        self.assertEqual(res.status_code, 503)
        self.assertEqual(res.content, b"Site is under maintenance")