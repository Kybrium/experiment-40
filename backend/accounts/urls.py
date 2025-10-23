from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from accounts.views import (
    UserView, CookieTokenObtainPairView, LogoutView
)

urlpatterns = [

    # JWT
    path("token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # User
    path("me/", UserView.as_view(), name="me"),
    path("register/", UserView.as_view(), name="register_user")
    
]