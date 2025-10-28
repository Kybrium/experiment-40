from django.db import models
from accounts.models import GameToken, User

class MinecraftAccount(models.Model):
    nickname = models.CharField(max_length=255, unique=True)
    uuid = models.CharField(max_length=64, unique=True, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="minecraft_accounts")
    token = models.OneToOneField(GameToken, on_delete=models.CASCADE, related_name='minecraft_account')

    is_dead = models.BooleanField(default=False)
    dead_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    deactivated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname