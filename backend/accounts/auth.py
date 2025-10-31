from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission
from django.conf import settings
import hmac



class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            # fallback to cookie
            raw_token = request.COOKIES.get("access_token")
            if raw_token is None:
                return None
        else:
            raw_token = self.get_raw_token(header)

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
    

class HasMinecraftServerKey(BasePermission):
    """
    Allows access only if request contains the correct server key header.
    This is *not* per-user auth. This is per-server auth.
    """

    # Incoming header should be:  X-Server-Key: <key>
    # Django/DRF exposes that as request.META["HTTP_X_SERVER_KEY"]
    header_name = "HTTP_X_SERVER_KEY"

    def has_permission(self, request, view):
        provided = request.META.get(self.header_name)
        expected = getattr(settings, "MINECRAFT_API_KEY", None)

        if not expected:
            return False

        if provided is None:
            return False

        return hmac.compare_digest(provided, expected)