# 🧠 Backend Docs

Welcome to the backend documentation!

Each Django app has its own README file that describes its models, serializers, views, and tests.

## 📚 Navigation

- [Accounts Docs](accounts/README.md)
- [Core Docs](core/README.md)

---

### 🏗️ Stack Overview

**Core Framework**

* **Django 5.2.7** — modern, async-capable web framework for rapid backend development.
* **Django REST Framework (DRF 3.16.1)** — toolkit for building REST APIs.
* **asgiref 3.10.0** — ASGI utilities used by Django’s async internals.

**Authentication & Security**

* **djangorestframework-simplejwt 5.5.1** — JWT authentication layer for DRF.
* **PyJWT 2.10.1** — underlying JWT signing/verification used by SimpleJWT.
* **django-otp 1.6.1** — two-factor auth (TOTP, etc.) support.
* **qrcode 8.2** — generates QR codes for enrolling authenticators / TOTP apps.
* **django-cors-headers 4.9.0** — CORS middleware for allowing the frontend to talk to the API.

**Database & ORM**

* **mysqlclient 2.2.7** — MySQL driver for Django (dev/prod DB backend).
* **dj-database-url 3.0.1** — parses `DATABASE_URL` into Django `DATABASES` config.
* **sqlparse 0.5.3** — SQL formatter used by Django.
* **tzdata 2025.2** — timezone info for environments without system zoneinfo (e.g. Windows containers / alpine images).

**HTTP / Networking**

* **requests 2.32.5** — HTTP client we use to call external services (like `randomuser.me`) during account generation.
* **urllib3 2.5.0**, **certifi 2025.10.5**, **idna 3.11**, **charset-normalizer 3.4.4** — dependency stack that `requests` uses for secure TLS, encoding detection, and URL handling.

**Environment & Configuration**

* **python-dotenv 1.1.1** — loads `.env` into `os.environ` for local/dev config.

**Static Files & Middleware**

* **whitenoise 6.11.0** — serves static assets directly from Django in production (no extra CDN/web server required).

**Developer / DX / Console**

* **rich 14.2.0** — nice formatting / colors in logs and management commands.
* **colorama 0.4.6** — Windows console color support (pulled in for pretty output on Windows terminals).

**Documentation / Markdown / Code Highlighting**

* **markdown-it-py 4.0.0** — Markdown renderer for any developer-facing docs or previews.
* **mdurl 0.1.2** — URL parser used by markdown-it.
* **Pygments 2.19.2** — syntax highlighting for code blocks in rendered Markdown.

**Testing & QA**

* **coverage 7.11.0** — test coverage reporting.
* **factory_boy 3.3.3** — factories for generating model instances in tests.
* **Faker 37.11.0** — realistic fake data (names, emails, etc.) for factories.

---

### ⚙️ Development

**Run locally (you must have .env file, copy it from .env.example):**
```bash
python manage.py runserver