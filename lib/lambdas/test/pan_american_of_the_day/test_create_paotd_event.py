import unittest
import pytest

from src.pan_american_of_the_day.create_event import create_event


class TestCreateEvent(unittest.TestCase):
    @pytest.mark.integration
    def test_create_paotd_event(self):
        event = create_event()
        self.assertIsNotNone(event._registered_id)
        event.delete()
        self.assertIsNone(event._registered_id)
