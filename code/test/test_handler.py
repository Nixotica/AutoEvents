import unittest
from src.handler import add_one

class TestHandler(unittest.TestCase):
    def test_add_one(self):
        self.assertEqual(add_one(1), 2)