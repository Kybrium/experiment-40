# 🧠 Backend Docs

Welcome to the backend documentation!

Each Django app has its own README file that describes its models, serializers, views, and tests.

## 📚 Navigation

- [Accounts Docs](accounts/README.md)
- [Core Docs](core/README.md)

---

### 🏗️ Stack Overview

**Core Framework**
- **Django 5.2.7** — modern, async-ready web framework for rapid backend development.
- **Django REST Framework (DRF 3.16.1)** — powerful toolkit for building REST APIs.

**Authentication & Security**
- **SimpleJWT 5.5.1** — provides secure JWT-based authentication for API clients.
- **PyJWT 2.10.1** — underlying JSON Web Token implementation used by SimpleJWT.
- **django-cors-headers 4.9.0** — enables safe cross-origin requests (CORS) from frontend clients.

**Database & ORM**
- **mysqlclient 2.2.7** — MySQL driver for Django (used in development/production).
- **dj-database-url 3.0.1** — simplifies database configuration via `DATABASE_URL`.
- **sqlparse 0.5.3** — SQL formatter used internally by Django’s ORM.
- **tzdata 2025.2** — provides timezone data for environments missing system tzinfo.

**Environment & Configuration**
- **python-dotenv 1.1.1** — loads environment variables from `.env` files.

**Static Files & Middleware**
- **whitenoise 6.11.0** — serves static files efficiently in production (no extra web server required).

**Developer & Docs Utilities**
- **markdown-it-py 4.0.0** — renders Markdown for documentation or API descriptions.
- **mdurl 0.1.2** — URL parser for markdown-it.
- **Pygments 2.19.2** — syntax highlighting for code blocks in Markdown.
- **rich 14.2.0** — beautiful console output and log formatting.
- **asgiref 3.10.0** — ASGI utilities enabling async Django features.

---

### ⚙️ Development

**Run locally (you must have .env file, copy it from .env.example):**
```bash
python manage.py runserver