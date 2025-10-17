# 🧩 Accounts App Overview

The **Accounts** app manages user authentication, profiles, and JWT-based access control for the backend.

---

## 🔐 Key Features

* Custom `User` model extending Django’s `AbstractUser`
* JWT authentication via **SimpleJWT** (`token`, `refresh`, `verify` endpoints)
* `/api/accounts/me/` for fetching current user info
* Integrated test coverage for user, JWT, and auth flows

---

## 🧱 Structure

| Component      | Purpose                                                      |
| -------------- | ------------------------------------------------------------ |
| **Model**      | Minimal custom `User`, extendable for future profile fields. |
| **Serializer** | `MeSerializer` — read-only, exposes basic user info.         |
| **View**       | `UserView` — returns current authenticated user data.        |
| **URLs**       | JWT routes + `/me/` endpoint under `/api/accounts/`.         |

---

## 🚀 Usage

**Get Tokens**
`POST /api/accounts/token/` → returns `access` + `refresh` JWTs

**Get Current User**
`GET /api/accounts/me/` with `Authorization: Bearer <access_token>`

Response:

```json
{"id": 1, "username": "player1", "email": "player1@example.com"}
```

---

✅ **Summary:**
Lightweight authentication layer with a customizable `User` model, secure JWT login, and a simple `/me/` profile endpoint — ready for extension with roles or 2FA integration.