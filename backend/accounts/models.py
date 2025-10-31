from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class LanguageChoices(models.TextChoices):
        ENGLISH = "en", "English"
        UKRAINIAN = "uk", "Ukrainian"

    preferred_language = models.CharField(max_length=10, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH)
    slots = models.PositiveIntegerField(default=1) # VALUE TO INDICATE HOW MANY TOKENS THE USER CAN HAVE
    
    def __str__(self):
        return self.username
    

class GameToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_tokens')
    value = models.CharField(max_length=64, unique=True, db_index=True)
    generated_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True) # VALUE TO REVEAL IF IT IS ALREADY USED OR NOT

    def __str__(self):
        return f"{self.user}'s Token #{self.id}"