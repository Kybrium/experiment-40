from django.urls import path
from minecraft.views import (
    LinkMinecraftAccountView
)

urlpatterns = [
    path('link-token/', LinkMinecraftAccountView.as_view())
]