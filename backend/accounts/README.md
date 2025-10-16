# 🧩 Accounts App Docs

This app handles user authentication, JWT token management, and profile-related functionality for the backend.

---

## 🔐 Features

- Custom `User` model extending Django’s `AbstractUser`
- JWT-based authentication using **djangorestframework-simplejwt**
- `/api/accounts/me/` endpoint for retrieving current authenticated user info
- Full test coverage for models, serializers, views, and JWT integration

---

## 🧱 Main Components

### **Models**
`accounts/models.py`
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
````

A minimal custom user model, ready to be extended later.

---

### **Serializers**

`accounts/serializers.py`

```python
from rest_framework import serializers
from .models import User

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username", "email", "first_name", "last_name"]
```

This serializer is **read-only**, used by the `/me/` endpoint to expose safe user data.

---

### **Views**

`accounts/views.py`

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import MeSerializer

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

* Authenticated users can fetch their own profile (`GET /api/accounts/me/`).
* Unauthenticated requests return `401 Unauthorized`.

---

### **URLs**

`accounts/urls.py`

```python
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from accounts.views import UserView

urlpatterns = [
    # JWT endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Current user endpoint
    path("me/", UserView.as_view(), name="me"),
]
```

---

## 🧪 Tests

Tests cover:

* **Model:** basic user creation and validation.
* **Serializer:** correct data serialization and read-only behavior.
* **View:** `/me/` endpoint for authenticated and unauthenticated users.
* **JWT:** token obtain, refresh, verify, and protected route access.

Example test command:

```bash
python manage.py test accounts
```

---

## 🚀 Example Usage

### Obtain tokens

```bash
POST /api/accounts/token/
{
  "username": "player1",
  "password": "supersecret123"
}
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Get current user info

```bash
GET /api/accounts/me/
Authorization: Bearer <access_token>
```

Response:

```json
{
  "id": 1,
  "username": "player1",
  "email": "player1@example.com",
  "first_name": "Alex",
  "last_name": "Stone"
}
```