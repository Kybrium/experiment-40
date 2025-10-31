from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from accounts.models import GameToken
from .factories import GameTokenFactory, MinecraftAccountFactory


class MinecraftAccountModelTests(TestCase):
    """Behavior of MinecraftAccount model."""

    def test_create_account(self):
        """
        Factory can create a valid MinecraftAccount with a linked GameToken.
        Default flags and timestamps should be sane.
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

        # default booleans
        self.assertTrue(mc_account.is_active)
        self.assertFalse(mc_account.is_dead)

        # default timestamps
        self.assertIsNotNone(mc_account.created_at)
        self.assertIsNone(mc_account.dead_at)
        self.assertIsNone(mc_account.deactivated_at)

        # token relation exists
        self.assertIsInstance(mc_account.token, GameToken)
        self.assertTrue(mc_account.token.is_active)

        # related_name works
        self.assertEqual(
            mc_account.token.minecraft_account,
            mc_account,
        )

    def test_str_representation(self):
        """__str__ should return nickname."""
        mc_account = MinecraftAccountFactory(nickname="DiamondLord42")
        self.assertEqual(str(mc_account), "DiamondLord42")

    def test_unique_nickname(self):
        """nickname must be unique."""
        MinecraftAccountFactory(nickname="SameNick")
        with self.assertRaises(IntegrityError):
            MinecraftAccountFactory(nickname="SameNick")

    def test_unique_uuid(self):
        """uuid must be unique."""
        MinecraftAccountFactory(uuid="deadbeef-dead-beef-dead-beefdeadbeef")
        with self.assertRaises(IntegrityError):
            MinecraftAccountFactory(uuid="deadbeef-dead-beef-dead-beefdeadbeef")

    def test_token_is_one_to_one(self):
        """
        A single GameToken can't be used for two MinecraftAccount rows,
        because token is OneToOneField.
        """
        token = GameTokenFactory()

        # First account creation works fine
        MinecraftAccountFactory(
            token=token,
            nickname="FirstDude",
            uuid="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        )

        # Second with same token should violate constraint
        with self.assertRaises(IntegrityError):
            MinecraftAccountFactory(
                token=token,
                nickname="SecondDude",
                uuid="ffffffff-1111-2222-3333-444444444444",
            )

    def test_dead_and_deactivated_timestamps_optional(self):
        """
        dead_at and deactivated_at should allow null until explicitly set.
        """
        mc_account = MinecraftAccountFactory()

        self.assertFalse(mc_account.is_dead)
        self.assertTrue(mc_account.is_active)
        self.assertIsNone(mc_account.dead_at)
        self.assertIsNone(mc_account.deactivated_at)

        # simulate marking account dead
        now = timezone.now()
        mc_account.is_dead = True
        mc_account.dead_at = now
        mc_account.save(update_fields=["is_dead", "dead_at"])

        refreshed = mc_account.__class__.objects.get(pk=mc_account.pk)
        self.assertTrue(refreshed.is_dead)
        self.assertEqual(refreshed.dead_at, now)

        # simulate deactivation
        now2 = timezone.now()
        refreshed.is_active = False
        refreshed.deactivated_at = now2
        refreshed.save(update_fields=["is_active", "deactivated_at"])

        refreshed2 = mc_account.__class__.objects.get(pk=mc_account.pk)
        self.assertFalse(refreshed2.is_active)
        self.assertEqual(refreshed2.deactivated_at, now2)