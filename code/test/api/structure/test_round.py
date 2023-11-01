from datetime import datetime
import unittest

from src.api.structure.round.round import Round


class TestRound(unittest.TestCase):
    def test_create_round_without_configs(self):
        round = Round(
            "my_round",
            datetime(1999, 11, 17, 0),
            datetime(1999, 11, 17, 1),
        )
        self.assertEqual(round._name, "my_round")
        self.assertEqual(round._start_date, datetime(1999, 11, 17, 0))
        self.assertEqual(round._end_date, datetime(1999, 11, 17, 1))
        self.assertIsNone(round._config)
        self.assertIsNone(round._qualifier)
        self.assertFalse(round.has_qualifier())
