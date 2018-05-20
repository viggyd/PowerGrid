import unittest
from nose import with_setup
from powergrid import ResourcePool, ResourceType, ResourceMarket

class TestResourceMarket(unittest.TestCase):


    def setUp(self):
        self.market = ResourceMarket(
            resource_settings="../powergrid/settings/initial_resources.json")

        self.replenish_rates = {
            ResourceType.COAL: 3,
            ResourceType.OIL: 2,
            ResourceType.TRASH: 1,
            ResourceType.URANIUM: 1
        }

    def tearDown(self):
        pass

    def test_setup_market(self):

        self.assertEqual(self.market.get_available_resources(ResourceType.COAL) , 24)
        self.assertEqual(self.market.get_available_resources(ResourceType.OIL) , 18)
        self.assertEqual(self.market.get_available_resources(ResourceType.TRASH) , 6)
        self.assertEqual(self.market.get_available_resources(ResourceType.URANIUM) , 2)

        pool = self.market.get_available_pool()
        self.assertEqual(pool[ResourceType.COAL] , 0)
        self.assertEqual(pool[ResourceType.OIL] , 6)
        self.assertEqual(pool[ResourceType.TRASH] , 18)
        self.assertEqual(pool[ResourceType.URANIUM] , 10)

    def test_replenish_rates(self):

        self.market.replenish_market(self.replenish_rates)
        self.assertEqual(self.market.get_available_resources(ResourceType.COAL) , 24)
        self.assertEqual(self.market.get_available_resources(ResourceType.OIL) , 20)
        self.assertEqual(self.market.get_available_resources(ResourceType.TRASH) , 7)
        self.assertEqual(self.market.get_available_resources(ResourceType.URANIUM) , 3)

        # Check to make sure that the available pool is decreasing
        pool = self.market.get_available_pool()
        self.assertEqual(pool[ResourceType.COAL] , 0)
        self.assertEqual(pool[ResourceType.OIL] , 4)
        self.assertEqual(pool[ResourceType.TRASH] , 17)
        self.assertEqual(pool[ResourceType.URANIUM] , 9)

        self.market.replenish_market(self.replenish_rates)
        self.assertEqual(self.market.get_available_resources(ResourceType.COAL) , 24)
        self.assertEqual(self.market.get_available_resources(ResourceType.OIL) , 22)
        self.assertEqual(self.market.get_available_resources(ResourceType.TRASH) , 8)
        self.assertEqual(self.market.get_available_resources(ResourceType.URANIUM) , 4)

        pool = self.market.get_available_pool()
        self.assertEqual(pool[ResourceType.COAL] , 0)
        self.assertEqual(pool[ResourceType.OIL] , 2)
        self.assertEqual(pool[ResourceType.TRASH] , 16)
        self.assertEqual(pool[ResourceType.URANIUM] , 8)


    def test_replenish_resource_not_available(self):


        # Someone buys a resource
        self.market.buy(ResourceType.COAL, 3)

        # But oh no! They don't use it, and it's time to replenish.
        self.market.replenish_market(self.replenish_rates)

        # Since they didn't release it back into the market, we assume that there's
        # no coal left to use.
        self.assertEqual(self.market.get_available_resources(ResourceType.COAL) , 21)

        # Now let's say that someone adds them back in, but not all of it.
        self.market.add_available_resources(
            {
                ResourceType.COAL : 2
            }
        )

        # And we again replenish...
        self.market.replenish_market(self.replenish_rates)

        # Although the replenish rate increases coal by 3, we only have 2 in the pool.
        self.assertEqual(self.market.get_available_resources(ResourceType.COAL) , 23)


    def test_available_pool_never_negative(self):


        # Replenish many many times and make sure that the available market
        # is always positive
        for _ in range(100):

            self.market.replenish_market(self.replenish_rates)

            pool = self.market.get_available_pool()

            for resource, available in pool.items():
                self.assertGreaterEqual(available, 0)
