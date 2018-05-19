import unittest
from nose import with_setup
from powergrid import ResourcePool, ResourceType

class TestResourcePool(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_oil_pool(self):

        oil = ResourcePool(ResourceType.OIL, 24, 18)

        # Check prices on some oil
        assert oil.calculate_cost(3) == 9
        assert oil.calculate_cost(4) == 13

        # Buy 3 oil
        assert oil.buy(3)

        # Replenish the oil a bit
        oil.replenish(2)


        # Since we didn't fully replenish, expect prices to go up
        assert oil.calculate_cost(3) == 10
        assert oil.calculate_cost(4) == 14
