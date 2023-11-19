import os

import pytest
from src.constants import CLUB_AUTO_EVENTS_STAGING
from src.api.club.campaign import Campaign
from src.api.structure.maps import PlaylistMap
from src.environment import UBI_AUTH
import unittest


class TestCampaign(unittest.TestCase):
    @pytest.mark.integration
    def test_get_campaign_map_playlist(self):
        # Auto Events Staging / Test Campaign
        test_club_id = CLUB_AUTO_EVENTS_STAGING
        test_campaign_id = 55190

        auth = os.getenv(UBI_AUTH)

        test_campaign = Campaign(test_club_id, test_campaign_id, auth)

        expected = [
            PlaylistMap("UGGBkWkQrVhRN_A21iPrC7N1vzl", 0),
            PlaylistMap("rWQJGIHxjigGa0yB8KiNmwBLMCe", 1),
            PlaylistMap("55swQ8IfqZCkloLBFnMDQjOGRii", 2),
            PlaylistMap("qixNDvlk9TPcStquClVVoSftNwj", 3),
            PlaylistMap("fdArnftBTYFWzhqfiGIgjjl3XJ3", 4),
        ]

        self.assertEqual(expected, test_campaign._playlist)
