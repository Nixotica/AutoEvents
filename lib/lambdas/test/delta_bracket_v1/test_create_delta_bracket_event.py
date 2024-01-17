import unittest
import pytest

from src.delta_bracket_v1.create_event import create_event


class TestCreateEvent(unittest.TestCase):
    @pytest.mark.integration
    def test_create_delta_bracket_event(self):
        event = create_event()
        self.assertIsNotNone(event._registered_id)
        event.delete()
        self.assertIsNone(event._registered_id)
