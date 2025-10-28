from django.test import TestCase
from django.db import IntegrityError

from accounts.models import GameToken
from .factories import GameTokenFactory, MinecraftAccountFactory


class MinecraftAccountModelTests(TestCase):
    """Behavior of MinecraftAccount model."""

    def test_create_account(self):
        """
        Factory can create a valid MinecraftAccount with a linked GameToken.
        Default flags should be sane.
        """
        mc_account = MinecraftAccountFactory(
            nickname="NotchLike",
            uuid="123e4567-e89b-12d3-a456-426614174000",
        )

        # basic fields set
        self.assertEqual(mc_account.nickname, "NotchLike")
        self.assertEqual(
            mc_account.uuid, "123e4567-e89b-12d3-a456-426614174000"
        )

        # is_active / is_dead defaults
        self.assertTrue(mc_account.is_active)
        self.assertFalse(mc_account.is_dead)

        # token relation exists
        self.assertIsInstance(mc_account.token, GameToken)
        self.assertTrue(mc_account.token.is_active)

        # account's token points back via related_name
        self.assertEqual(
            mc_account.token.minecraft_account,
            mc_account,
        )

    def test_str_representation(self):
        """
        __str__ should return nickname.
        """
        mc_account = MinecraftAccountFactory(nickname="DiamondLord42")
        self.assertEqual(str(mc_account), "DiamondLord42")

    def test_unique_nickname(self):
        """
        nickname must be unique.
        """
        MinecraftAccountFactory(nickname="SameNick")
        with self.assertRaises(IntegrityError):
            MinecraftAccountFactory(nickname="SameNick")

    def test_unique_uuid(self):
        """
        uuid must be unique.
        """
        MinecraftAccountFactory(uuid="deadbeef-dead-beef-dead-beefdeadbeef")
        with self.assertRaises(IntegrityError):
            MinecraftAccountFactory(uuid="deadbeef-dead-beef-dead-beefdeadbeef")

    def test_token_is_one_to_one(self):
        """
        A single GameToken can't be used to create two MinecraftAccount rows,
        because token is OneToOneField.
        """
        token = GameTokenFactory()

        # First account with this token works:
        MinecraftAccountFactory(
            token=token,
            nickname="FirstDude",
            uuid="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        )

        # Second account with the SAME token should violate OneToOne.
        with self.assertRaises(IntegrityError):
            MinecraftAccountFactory(
                token=token,
                nickname="SecondDude",
                uuid="ffffffff-1111-2222-3333-444444444444",
            )