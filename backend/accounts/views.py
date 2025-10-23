from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import MeSerializer, UserRegistrationSerializer



class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        # read tokens
        access = data.get("access")
        refresh = data.get("refresh")

        # remove from JSON body
        response.data.pop("access", None)
        response.data.pop("refresh", None)

        # set cookies
        cookie_params = {
            "httponly": True,
            "secure": not settings.DEBUG,
            "samesite": "Lax",
        }
        response.set_cookie("access_token", access, **cookie_params)
        response.set_cookie("refresh_token", refresh, **cookie_params)

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class UserView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "ok": True,
                "user": MeSerializer(user).data,
                "access": str(access),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED,
        )