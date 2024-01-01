import unittest
import pytest

from delta_bracket_v1.src.create_event import create_event
from nadeo_event_api.api.structure.event import Event

class TestCreateEvent(unittest.TestCase):
    @pytest.mark.integration
    def test_create_event(self):
        event: Event = create_event()
        self.assertIsNotNone(event._registered_id)
        event.delete()
        self.assertIsNone(event._registered_id)
