import unittest
import json

from aiof.fi.health import bmi_imperial, bmi_metric


class FiHealthTestCase(unittest.TestCase):
    """Fi health unit tests"""


    def test_bmi_imperial_defaults(self):
        bmi = bmi_imperial(
            weight=None,
            feet=None,
            inches=None
        )           
        assert bmi > 22

    def test_bmi_imperial(self):
        bmi = bmi_imperial(
            weight=250,
            feet=6,
            inches=6
        )
        assert bmi > 28


    def test_bmi_metric_defaults(self):
        bmi = bmi_metric(
            weight=None,
            height=None
        )
        assert bmi > 22

    def test_bmi_metric(self):
        bmi = bmi_metric(
            weight=120,
            height=201
        )
        assert bmi > 29