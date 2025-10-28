from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class LanguageChoices(models.TextChoices):
        ENGLISH = "en", "English"
        UKRAINIAN = "uk", "Ukrainian"

    preferred_language = models.CharField(max_length=10, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH)
    
    def __str__(self):
        return self.username