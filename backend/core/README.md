# ⚙️ Core App Docs

The **Core** app is the central configuration and entry point of the backend.  
It contains project-wide settings, middleware, routing, and utility endpoints used for monitoring and maintenance.

---

## 🧱 Overview

- Defines global **Django settings**, **middleware**, and **URL routing**
- Implements `MaintenanceModeMiddleware` for quickly enabling maintenance mode
- Provides a `/ping/` endpoint for uptime monitoring and health checks
- Handles static file configuration (via **WhiteNoise**) and security middleware
- Acts as the main project package (`core.settings`, `core.urls`, `core.wsgi`)

---

## 🔧 Key Components

### **1️⃣ Middleware**
`core/middlewares.py`
```python
from django.conf import settings
from django.http import HttpResponse

class MaintenanceModeMiddleware:
    """
    Middleware that checks if the site is in maintenance mode.
    If MAINTENANCE_MODE=True in settings, all requests
    return a 503 Service Unavailable response.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False):
            return HttpResponse("Site is under maintenance", status=503)
        return self.get_response(request)
````

**How to enable maintenance mode**

```bash
# In your .env file
MAINTENANCE_MODE=True
```

or dynamically in Django shell:

```python
from django.conf import settings
settings.MAINTENANCE_MODE = True
```

---

### **2️⃣ Healthcheck Endpoint**

`core/views.py`

```python
from django.http import JsonResponse

def ping(request):
    """Simple healthcheck endpoint."""
    return JsonResponse({"status": "ok"}, status=200)
```

`core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", views.ping, name="ping"),
    path("api/accounts/", include("accounts.urls")),
]
```

✅  Accessible at:

```
GET /ping/
```

Response:

```json
{"status": "ok"}
```

---

### **3️⃣ Settings Highlights**

`core/settings.py`

* **Database** — configurable via `DATABASE_URL` or environment vars
  (supports SQLite for dev, MySQL for production)
* **Authentication** — JWT (via `djangorestframework-simplejwt`)
* **CORS** — managed by `django-cors-headers`
* **Static files** — served by `WhiteNoise`
* **Custom user model** — `accounts.User`
* **Maintenance mode** — toggled with `MAINTENANCE_MODE` flag

---

### **4️⃣ Tests**

`core/tests/test_middlewares.py`

```python
from django.test import TestCase, override_settings

class MaintenanceModeMiddlewareTests(TestCase):
    @override_settings(MAINTENANCE_MODE=False)
    def test_pass_through_when_disabled(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"status": "ok"})

    @override_settings(MAINTENANCE_MODE=True)
    def test_returns_503_when_enabled(self):
        res = self.client.get("/ping/")
        self.assertEqual(res.status_code, 503)
        self.assertEqual(res.content, b"Site is under maintenance")
```

---

## 🧪 Example Usage

### Check if backend is up

```bash
curl http://localhost:8000/ping/
```

Response:

```json
{"status": "ok"}
```

### Enable maintenance mode (temporarily)

```bash
export MAINTENANCE_MODE=True
python manage.py runserver
```

Response for any request:

```
HTTP/1.1 503 Service Unavailable
Site is under maintenance
```