from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
import requests

from minecraft.utils import generate_unique_nickname


def make_randomuser_response(names):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "results": [{"name": {"first": f, "last": l}} for (f, l) in names]
    }
    return mock_resp


class GenerateUniqueNicknameTests(SimpleTestCase):

    @patch("minecraft.utils.MinecraftAccount")
    @patch("minecraft.utils.requests.get")
    def test_returns_first_unique_name(self, mock_get, MockMinecraftAccount):
        mock_get.return_value = make_randomuser_response([
            ("Alex", "Stone"),
            ("John", "Doe"),
        ])

        MockMinecraftAccount.objects.filter.return_value.exists.return_value = False

        result = generate_unique_nickname(10, "male", "US")

        self.assertEqual(result, "alex_stone")
        mock_get.assert_called_once()
        MockMinecraftAccount.objects.filter.assert_called_with(nickname="alex_stone")

    @patch("minecraft.utils.MinecraftAccount")
    @patch("minecraft.utils.requests.get")
    def test_skips_taken_name_and_returns_next_free(self, mock_get, MockMinecraftAccount):
        mock_get.return_value = make_randomuser_response([
            ("Alex", "Stone"),
            ("John", "Doe"),
        ])

        MockMinecraftAccount.objects.filter.return_value.exists.side_effect = [
            True,   # alex_stone taken
            False,  # john_doe free
        ]

        result = generate_unique_nickname(10, None, None)

        self.assertEqual(result, "john_doe")
        mock_get.assert_called_once()

    @patch("minecraft.utils.MinecraftAccount")
    @patch("minecraft.utils.requests.get")
    def test_multiple_batches_until_found(self, mock_get, MockMinecraftAccount):
        first_batch = make_randomuser_response([
            ("Alex", "Stone"),
            ("John", "Doe"),
            ("Maria", "Lopez"),
        ])
        second_batch = make_randomuser_response([
            ("Sasha", "Petrenko"),
        ])
        mock_get.side_effect = [first_batch, second_batch]

        MockMinecraftAccount.objects.filter.return_value.exists.side_effect = [
            True, True, True,
            False,
        ]

        result = generate_unique_nickname(6, "female", "UA")

        self.assertEqual(result, "sasha_petrenko")
        self.assertEqual(mock_get.call_count, 2)

        first_call_args, first_call_kwargs = mock_get.call_args_list[0]
        self.assertEqual(first_call_args[0], "https://randomuser.me/api/")
        self.assertEqual(first_call_kwargs["params"]["gender"], "female")
        self.assertEqual(first_call_kwargs["params"]["nat"], "UA")
        self.assertEqual(first_call_kwargs["params"]["results"], 5)

        second_call_args, second_call_kwargs = mock_get.call_args_list[1]
        self.assertEqual(second_call_kwargs["params"]["results"], 1)

    @patch("minecraft.utils.MinecraftAccount")
    @patch("minecraft.utils.requests.get")
    def test_returns_none_if_all_exhausted(self, mock_get, MockMinecraftAccount):
        mock_get.return_value = make_randomuser_response([
            ("Alex", "Stone"),
            ("John", "Doe"),
        ])
        MockMinecraftAccount.objects.filter.return_value.exists.return_value = True

        result = generate_unique_nickname(2, None, None)

        self.assertIsNone(result)
        self.assertGreaterEqual(mock_get.call_count, 1)

    @patch("minecraft.utils.requests.get")
    def test_raises_if_requests_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("network down")

        with self.assertRaises(requests.RequestException):
            generate_unique_nickname(10, None, None)

    @patch("minecraft.utils.requests.get")
    def test_raises_if_non_200_response(self, mock_get):
        bad_resp = MagicMock()
        bad_resp.status_code = 500
        mock_get.return_value = bad_resp

        with self.assertRaises(RuntimeError) as ctx:
            generate_unique_nickname(10, None, None)

        self.assertIn("identity_provider_error", str(ctx.exception))