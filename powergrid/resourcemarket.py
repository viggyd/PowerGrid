import json
from powergrid import ResourceType, ResourcePool

"""
Resource Market
    a: Oil Resource Pool
    a: Coal Resource Pool
    a: Trash Resource Pool
    a: Uranium Resource Pool
    
    a: Available resource pool
    
    m: Add to available resources
    m: Replenish from available resources
    m: Get available resources for type
    m: Buy resource type
    m: Replenish resource type
"""

class ResourceMarket(object):
    """
    Create the 4 resource pools to be used.
    This class acts as a wrapper and simply keeps track of all four resource pools
    in one place, rather than having the moderator keep track of it all.

    The methods here are the same as the ones in the ResourcePool class, they just
    require a resource argument to look at the specific type.

    As with the PlantMarket, there is no policy provided by this class, only
    the mechanisms. It will not force you to give a certain amount before
    buying the resource. That is up to the moderator to enforce.
    """

    def __init__(self, resource_settings):

        self.resource_settings = None
        with open(resource_settings, 'r') as f:
            self.resource_settings = json.loads(f.read())

        # Set up the resource pools
        coal_pool = ResourcePool(
            ResourceType.COAL,
            self.resource_settings["Total"]["Coal"],
            self.resource_settings["Initial"]["Coal"]
            )


        oil_pool = ResourcePool(
            ResourceType.OIL,
            self.resource_settings["Total"]["Oil"],
            self.resource_settings["Initial"]["Oil"]
            )

        trash_pool = ResourcePool(
            ResourceType.TRASH,
            self.resource_settings["Total"]["Trash"],
            self.resource_settings["Initial"]["Trash"]
            )

        uranium_pool = ResourcePool(
            ResourceType.URANIUM,
            self.resource_settings["Total"]["Uranium"],
            self.resource_settings["Initial"]["Uranium"]
            )

        # Set up the market.
        self.market = {
            ResourceType.COAL    : coal_pool,
            ResourceType.OIL     : oil_pool,
            ResourceType.TRASH   : trash_pool,
            ResourceType.URANIUM : uranium_pool
        }

        self.available_pool = {
            ResourceType.COAL    : coal_pool.get_total_size()    - coal_pool.get_available_resources(),
            ResourceType.OIL     : oil_pool.get_total_size()     - oil_pool.get_available_resources(),
            ResourceType.TRASH   : trash_pool.get_total_size()   - trash_pool.get_available_resources(),
            ResourceType.URANIUM : uranium_pool.get_total_size() - uranium_pool.get_available_resources()
        }


    def replenish_market(self, replenish_rates):
        """
        Replenish each of the resources in the market
        :param replenish_rates: A dictionary of the replenish rates
        :return: None
        """

        # Always replenish based on rates, but do not do so if there are no
        # resources left for us to replenish

        # Iterate over replenish rates
        for resource, rate in replenish_rates.items():

            # Determine the actual replenish rate by taking the min of the
            # settings replenish rate and the actual resources available to use
            actual_rate = min(rate, self.available_pool[resource])

            # Replenish the market
            self.market[resource].replenish(actual_rate)

            # Since we know that the actual rate is <= available resources,
            # we can perform this operation without fear of going into the negatives.
            self.available_pool[resource] -= actual_rate


    def calculate_cost(self, resource, amount):
        """
        Calculate the cost to buy a certain resource
        :param resource: The resource to check
        :param amount: The amount of the resource in consideration
        :return: The cost to buy :amount of :resource
        """

        return self.market[resource].calculate_cost(amount)

    def buy(self, resource, amount):
        """
        Buy a given amount of a given resource
        :param resource: The resource to buy
        :param amount: The amount of the resource to buy
        :return: True if the resource can be bought, False otherwise
        """

        return self.market[resource].buy(amount)

    def get_available_resources(self, resource):
        """
        Get available resources of a certain type
        :param resource: The resource to check
        :return: The amount of resources left of this type
        """

        return self.market[resource].get_available_resources()

    def add_available_resources(self, usage_report):
        """
        Add resources to the available pool based on the usage report
        :param usage_report: A dictionary of how many of each resource to add back
        :return: None
        """

        for resource, usage in usage_report.items():
            self.available_pool[resource] += usage

    def get_available_pool(self):
        """
        Get the pool of resources not yet in the market
        :return: The pool of available resource as a dictionary
        """
        return self.available_pool