from django.contrib import admin
from django.urls import path, include
from core.views import ping


urlpatterns = [

    # Core
    path('admin/', admin.site.urls),
    path("ping/", ping, name="ping"),

    # Apps
    path("api/accounts/", include('accounts.urls'))

]