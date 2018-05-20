from powergrid import ResourceType

"""
    Although in PowerGrid, a player does not have a specific board that is theirs,
    like in Viticulture, there is undeniably a board state for each player. For
    the purposes of our initial analysis, this board is all we really need.
    Everything else will be strategy. The board, for example, is not allowed to see
    what the actual/future markets are. That is the job of the intelligence behind
    the board.

    In this manner, I again try to separate policy from mechanism.

    a: Cities owned
    a: Plants owned
    a: Current elektro
    a: Resource Map (Plant : Resources on plant)

    m: Get number of cities
    m: Remove elektro

    Phase 2: Auction Power Plants
    m: Get power plants
    m: Add plant to board
    m: Replace plant

    Phase 3: Buying Resources
    m: Get resources on each plant
    m: Add resources to plant

    Phase 4: Building
    m: Add cities to network

    Phase 5: Bureaucracy
    m: Remove resources from plant
    m: Get elektro for plants powered
"""

class PlayerBoard(object):

    def __init__(self, max_plants):

        self.cities = []
        self.plants = []
        self.elektro = 0
        self.max_plants = max_plants
        self.resource_map = {}


    def spend_elektro(self, amount):
        """
        Spend elektro for whatever purpose
        :param amount: The amount of money to spend
        :return: True if the money was spent, false if board doesn't have enough
        """

        # Return false if we can't spend that much money
        if self.elektro < amount:
            return False

        self.elektro -= amount
        return True


    def earn_elektro(self, amount):
        """
        Add elektro to the board
        :param amount: The amount of elektro to add
        """
        self.elektro += amount


    def get_num_cities(self):
        """
        Get number of cities on board
        :return: The number of cities owned by this player
        """
        return len(self.cities)


    def get_plants(self):
        """
        Get the power plants on the board
        :return: The list of plants on the board
        """
        return self.plants


    def get_cities(self):
        """
        Get the cities owned on board
        :return: The list of cities owned
        """
        return self.cities


    def add_plant(self, plant):
        """
        Add a power plant to the board
        :param plant:
        :return: True if plant could be added, False otherwise
        """

        # Return early if the number of plants equals or exceeds our quota
        if len(self.plants) >= self.max_plants:
            return False

        self.plants.append(plant)

        # Add the new plant to the resource map
        resource_dict = {}

        if plant.get_resource_type() == ResourceType.HYBRID:
            resource_dict[ResourceType.COAL] = 0
            resource_dict[ResourceType.OIL] = 0
        else:
            resource_dict[plant.get_resource_type()] = 0

        self.resource_map[plant] = resource_dict

        self.plants.sort()

        return True


    def replace_plant(self, new_plant, old_plant):
        """
        Replace the old plant with the new one
        :param new_plant: The new plant to add to the board
        :param old_plant: The plant to remove from the board
        :return: None
        """

        # Remove old plant from list and from dictionary.
        self.plants.remove(old_plant)
        del self.resource_map[old_plant]


        self.add_plant(new_plant)

    def get_resources_on_plants(self):
        return self.resource_map

    def add_resources_to_plant(self, plant, resource_type, amount):
        """
        Add certain number of resources to a given plant
        :param plant: The plant to add resources to
        :param resource_type: The type of resource to add
        :param amount: The amount of the resource to add
        """

        self.resource_map[plant][resource_type] += amount


    def add_cities(self, city):
        self.cities.append(city)

    def power_plants(self, plant_resource_map):
        """
        Power the plants in the given plant list. This requires
        :param plant_resource_map: A dictionary containing the plants to power
            and the resources need if the plant is hybrid

            {
                Plant 3: None,
                Plant 5: {ResourceType.COAL : 1, ResourceType.OIL : 1}
            }

        :return: None
        """

        usage_report = {
            ResourceType.COAL : 0,
            ResourceType.OIL : 0,
            ResourceType.TRASH : 0,
            ResourceType.URANIUM : 0
        }

        for plant, usage in plant_resource_map.items():

            storage = self.resource_map[plant]
            plant_type = plant.get_resource_type()


            if usage is None and plant_type != ResourceType.HYBRID:
                current_storage = storage[plant_type]
                current_storage -= plant.get_required_fuel()
                usage_report[plant_type] += plant.get_required_fuel()
                self.resource_map[plant][plant_type] = current_storage

            elif plant_type == ResourceType.HYBRID:

                storage[ResourceType.COAL] -= usage[ResourceType.COAL]
                usage_report[ResourceType.COAL] += usage[ResourceType.COAL]

                storage[ResourceType.OIL] -= usage[ResourceType.OIL]
                usage_report[ResourceType.OIL] += usage_report[ResourceType.OIL]

                self.resource_map[plant] = storage

        return usage_report


    def can_power_plant(self, plant):
        """
        Determine if the plant can be powered
        :param plant: The plant to check
        :return: True if plant can be powered, false otherwise
        """

        storage = self.resource_map[plant]
        if plant.get_resource_type() == ResourceType.HYBRID:
            total_storage = storage[ResourceType.COAL] + storage[ResourceType.OIL]
        else:
            total_storage = storage[plant.get_resource_type()]

        if total_storage >= plant.get_required_fuel():
            return True
        else:
            return False