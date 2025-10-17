# ⚙️ Core App Overview

The **Core** app serves as the central hub of the backend — managing configuration, middleware, routing, and maintenance utilities used across the project.

---

## 🧱 Responsibilities

* Defines **global Django settings**, middleware, and routing.
* Manages **maintenance mode** via `MaintenanceModeMiddleware`.
* Provides a `/ping/` healthcheck endpoint for uptime monitoring.
* Integrates **WhiteNoise** for static file serving in production.
* Handles **custom admin logic** — including **2FA-secured admin (django-otp)** in production.

---

## 🔐 Admin Access

* **Development:** uses the default Django Admin.
* **Production:** uses a secure **OTP-based Admin** (`django-otp` + `qrcode`) for two-factor authentication.
* This ensures admin access requires both credentials and a verified TOTP code.

---

## 🧩 Key Features

| Feature                  | Description                                                            |
| ------------------------ | ---------------------------------------------------------------------- |
| **Maintenance Mode**     | Toggleable via `MAINTENANCE_MODE=True` (returns 503 for all requests). |
| **Healthcheck Endpoint** | `/ping/` → returns `{"status": "ok"}` for monitoring.                  |
| **Custom User Model**    | Centralized in `accounts.User`, integrated across admin and auth.      |
| **Static Files**         | Served efficiently with **WhiteNoise**.                                |
| **Security**             | JWT authentication, CORS management, and optional 2FA admin.           |

---

## 🧪 Quick Checks

**Healthcheck:**
`GET /ping/ → {"status": "ok"}`

**Enable maintenance mode:**
`.env → MAINTENANCE_MODE=True`

**Admin (Prod):**
2FA-enabled via TOTP app (e.g. Google Authenticator).

---

**In short:**
The Core app ties together system-wide behavior — configuration, security (2FA admin), middleware, and monitoring — providing a stable foundation for the entire backend.