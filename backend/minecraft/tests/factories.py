import secrets
import factory

from accounts.models import User, GameToken
from minecraft.models import MinecraftAccount


class UserFactory(factory.django.DjangoModelFactory):
    """
    Minimal usable User instance.
    We duplicate it here so tests in this app don't have to import test utils
    from another app (keeps tests isolated).
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
    A valid GameToken belonging to a user.
    """
    class Meta:
        model = GameToken

    user = factory.SubFactory(UserFactory)
    value = factory.LazyFunction(lambda: secrets.token_urlsafe(16))
    is_active = True


class MinecraftAccountFactory(factory.django.DjangoModelFactory):
    """
    A valid, linked MinecraftAccount.
    """
    class Meta:
        model = MinecraftAccount

    nickname = factory.Faker("user_name")
    uuid = factory.LazyFunction(
        # looks like a MC UUID-ish string, not enforced, just unique
        lambda: secrets.token_hex(16)
    )
    token = factory.SubFactory(GameTokenFactory)
    is_dead = False
    is_active = True