# 🧩 Accounts App Overview

The **Accounts** app manages user registration, authentication, JWT access control, and profile retrieval for the backend.

---

## 🚀 Available Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/accounts/register/` | **POST** | Register a new user account. |
| `/api/accounts/token/` | **POST** | Obtain a new JWT access and refresh token pair. |
| `/api/accounts/refresh/` | **POST** | Refresh the JWT access token using a valid refresh token. |
| `/api/accounts/verify/` | **POST** | Verify if a given JWT token is valid and not expired. |
| `/api/accounts/logout/` | **POST** | Invalidate the user’s active tokens (logout). |
| `/api/accounts/me/` | **GET** | Retrieve the currently authenticated user’s profile. |

---