import unittest
import json

from aiof.car.core import *


class CarTestCase(unittest.TestCase):
    """Car unit tests"""

    def test_truth(self):
        assert test() == "car"