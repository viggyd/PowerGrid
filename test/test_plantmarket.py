import unittest
from nose import with_setup
from powergrid import PlantMarket, Plant, ResourceType, PlantDeck

class TestPlantMarket(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_market(self):

        market = PlantMarket()

        assert market.get_market_size() == 0

        # market.add_plant_to_market()
