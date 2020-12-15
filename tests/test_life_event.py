import unittest

from aiof.data.life_event import LifeEvent


class LifeEventTestCase(unittest.TestCase):
    """
    Life event unit tests
    """

    def test_life_event_definition_issuccessful(self):
        le = LifeEvent(
            type = "buying a house",
            amount = 15000.00,
            plannedDate = None)

        assert le is not None
        assert le.type is not None
        assert le.amount > 0
    
    def test_life_event_definition_type_isinvalid(self):
        with self.assertRaises(ValueError): 
            LifeEvent(
                type = "definitelydoesntexist",
                amount = 15000.00,
                plannedDate = None)

    def test_life_event_definition_type_isnone(self):
        with self.assertRaises(ValueError): 
            LifeEvent(
                type = None,
                amount = 15000.00,
                plannedDate = None)