# 🧩 Accounts App Overview

The **Accounts** app manages user authentication, profiles, and JWT-based access control for the backend.

---

## 🚀 Usage

### 🧾 Register a New User

`POST /api/accounts/register/` → creates a new user and returns JWT tokens.

**Request Body**

```json
{
  "username": "player1",
  "email": "player1@example.com",
  "first_name": "Alex",
  "last_name": "Stone",
  "password": "supersecret123",
  "password2": "supersecret123"
}
```

**Response (201 Created)**

```json
{
  "ok": true,
  "user": {
    "id": 1,
    "username": "player1",
    "email": "player1@example.com",
    "first_name": "Alex",
    "last_name": "Stone"
  },
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

✅ Notes:

* `password` and `password2` must match.
* Password must be **at least 8 characters**.
* `email` and `username` must be **unique**.
* Tokens can immediately be used to authorize further requests.

---

### 🔑 Get Tokens

`POST /api/accounts/token/` → obtain JWT token pair for an existing user.

**Request Body**

```json
{
  "username": "player1",
  "password": "supersecret123"
}
```

**Response**

```json
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

✅ Notes:

* The `access` token expires after a short period (usually minutes).
* Use the `refresh` token to obtain a new `access` token without logging in again.

---

### 🔁 Refresh Token

`POST /api/accounts/refresh/` → obtain a new `access` token using a valid `refresh` token.

**Request Body**

```json
{
  "refresh": "<jwt_refresh_token>"
}
```

**Response**

```json
{
  "access": "<new_jwt_access_token>"
}
```

✅ Notes:

* The old `access` token becomes invalid once it expires, but the `refresh` token remains valid (until its own expiry).
* You can safely refresh tokens on the frontend whenever a 401 Unauthorized is returned.

---

### 🧩 Verify Token

`POST /api/accounts/verify/` → check if a given token (access or refresh) is valid.

**Request Body**

```json
{
  "token": "<jwt_access_token>"
}
```

**Response (Valid Token)**

```json
{}
```

**Response (Invalid Token)**

```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

✅ Notes:

* This endpoint is useful for background validation (e.g., confirming user sessions).
* If the token is expired or tampered with, you’ll get a `401 Unauthorized` response.

---

### 👤 Get Current User

`GET /api/accounts/me/` → retrieve current user profile.
Requires header:
`Authorization: Bearer <access_token>`

**Response**

```json
{
  "id": 1,
  "username": "player1",
  "email": "player1@example.com",
  "first_name": "Alex",
  "last_name": "Stone"
}
```

✅ Notes:

* Returns the authenticated user linked to the provided JWT access token.
* If the token is missing or invalid → returns `401 Unauthorized`.

---