from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from accounts.models import GameToken
from minecraft.models import MinecraftAccount
from accounts.auth import HasMinecraftServerKey



class LinkMinecraftAccountView(APIView):
    """
    2 modes:
    - GET (authenticated user): pre-create a MinecraftAccount shell and bind the next available token.
    - POST (server with X-Server-Key): attach UUID for an existing account later.
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [HasMinecraftServerKey()]
        return [IsAuthenticated()]

    @transaction.atomic
    def get(self, request):
        user = request.user

        # 1. pick an available token for this user
        # "available" means:
        #   - user owns it
        #   - it's still active
        #   - it is NOT already attached to a MinecraftAccount
        token = (
            GameToken.objects
            .filter(user=user, is_active=True, minecraft_account__isnull=True)
            .order_by("generated_at")
            .first()
        )

        if token is None:
            return Response(
                {"detail": _("No available tokens. Generate one first.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. generate nickname placeholder
        # TODO: replace with RP name generator later (male/female etc.)
        # for now something deterministic like "Citizen<ID>" so it's unique
        base_nickname = f"Citizen{user.id}-{token.id}"

        if MinecraftAccount.objects.filter(nickname=base_nickname).exists():
            base_nickname = f"Citizen{user.id}-{token.id}-x"

        # 3. create MinecraftAccount shell with no uuid yet
        account = MinecraftAccount.objects.create(
            owner=user,
            nickname=base_nickname,
            uuid=None,  # will be filled in by POST from server
            token=token,
            is_dead=False,
            dead_at=None,
            is_active=True,
            deactivated_at=None,
        )

        # 4. burn token so it can't be reused elsewhere
        token.is_active = False
        token.save(update_fields=["is_active"])

        # 5. return the shell info
        return Response(
            {
                "ok": True,
                "account_id": account.id,
                "nickname": account.nickname,
                "uuid": account.uuid,  # will be None for now
                "created_at": account.created_at,
            },
            status=status.HTTP_201_CREATED,
        )