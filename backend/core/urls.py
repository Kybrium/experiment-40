from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from core.views import ping

from accounts.models import User
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin


# ========== ADMIN MODULE REGISTRATION ==========
class OTPAdmin(OTPAdminSite):
    pass

otp_admin_site = OTPAdmin(name="OTPAdmin")
otp_admin_site.register(User)
otp_admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site = admin.site if settings.DEBUG else otp_admin_site
# ===============================================


urlpatterns = [

    # Admin
    path("admin/", admin_site.urls),

    # Core
    path("ping/", ping, name="ping"),

    # Apps
    path("api/accounts/", include("accounts.urls")),
    path("api/minecraft/", include("minecraft.urls")),
    
]