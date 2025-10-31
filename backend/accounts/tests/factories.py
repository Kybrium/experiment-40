import secrets
import factory
from accounts.models import User, GameToken



class UserFactory(factory.django.DjangoModelFactory):
    """
    Minimal factory for the project's User model.
    Provides a valid, ready-to-use user with a hashed password.
    """
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    password = factory.PostGenerationMethodCall("set_password", "StrongPass123")


class GameTokenFactory(factory.django.DjangoModelFactory):
    """
    Factory for GameToken.
    By default: creates a new user and a unique secure token value.
    """
    class Meta:
        model = GameToken

    user = factory.SubFactory(UserFactory)

    value = factory.LazyFunction(lambda: secrets.token_urlsafe(16))

    is_active = True