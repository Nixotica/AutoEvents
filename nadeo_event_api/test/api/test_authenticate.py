import unittest
from unittest.mock import MagicMock, patch
from src.api.enums import NadeoService
from src.api.authenticate import authenticate


class TestAuthenticate(unittest.TestCase):
    @patch("requests.post")
    def test_authenticate(self, mock_request_post):
        mock_response = MagicMock()
        mock_response.json.side_effect = [
            {"ticket": "my_ticket"},
            {"accessToken": "my_token"},
        ]
        mock_request_post.return_value = mock_response
        self.assertEqual(authenticate(NadeoService.CLUB, "auth"), "my_token")
