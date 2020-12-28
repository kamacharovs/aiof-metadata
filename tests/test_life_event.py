import unittest

from aiof.data.asset import Asset
from aiof.data.liability import Liability
from aiof.data.life_event import LifeEventRequest


class LifeEventTestCase(unittest.TestCase):
    """
    Life event unit tests
    """
    _assets = [
        Asset(name="asset 1",
            typeName="cash",
            value=35000),
        Asset(name="asset 2",
            typeName="cash",
            value=8000),
        Asset(name="asset 3",
            typeName="stock",
            value=24999)
    ]
    _liabilities = [
        Liability(name="l1",
            typeName="personal loan",
            value=1685.50,
            years=5,
            monthlyPayment=35),
        Liability(name="l2",
            typeName="student loan",
            value=25000,
            years=10,
            monthlyPayment=208),
        Liability(name="l3",
            typeName="car loan",
            value=34000,
            years=6,
            monthlyPayment=500)
    ]

    def test_life_event_definition_issuccessful(self):
        le = LifeEventRequest(
            assets = self._assets,
            liabilities = self._liabilities,
            type = "buying a house",
            amount = 15000.00,
            plannedDate = None)

        assert le is not None
        assert le.type is not None
        assert le.amount > 0
    
    def test_life_event_definition_type_isinvalid(self):
        with self.assertRaises(ValueError): 
            LifeEventRequest(
                assets = self._assets,
                liabilities = self._liabilities,
                type = "definitelydoesntexist",
                amount = 15000.00,
                plannedDate = None)

    def test_life_event_definition_type_isnone(self):
        with self.assertRaises(ValueError): 
            LifeEventRequest(
                assets = self._assets,
                liabilities = self._liabilities,
                type = None,
                amount = 15000.00,
                plannedDate = None)