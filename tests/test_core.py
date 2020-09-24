import unittest
import json

from aiof.core import *


class CoreTestCase(unittest.TestCase):
    """Core unit tests"""

    def test_frequencies(self):
        assert len(frequencies()) > 0