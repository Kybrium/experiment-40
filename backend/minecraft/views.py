from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from accounts.models import GameToken
from minecraft.models import MinecraftAccount
from accounts.auth import HasMinecraftServerKey