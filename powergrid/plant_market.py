from powergrid import PlantDeck
from powergrid import Plant
from powergrid import GameStep
from powergrid import MARKET_ACT_SIZE, MARKET_FUT_SIZE, MARKET_S3_ACT_SIZE

class PlantMarket(object):
    """
    This class is not responsible for enforcing any of the policy of the game.
    It only provides the mechanisms to have a plant market.
    It is up to the game moderator object to enforce all the policy.
    For example, the market will not automatically add a new card once a plant
    is up for auction. It is up to the moderator to make sure that the market is
    properly organized.

    """

    def __init__(self):

        self.market = []
        self.actual = []
        self.future = []

        self.game_step = GameStep.STEP1

    def remove_highest(self):
        """
        Remove highest card from actual/future market and add to bottom of deck
        :return: The highest value power plant in the market
        """
        plant = self.market.pop(-1)
        self.layout()
        return plant

    def remove_lowest(self):
        """
        Remove lowest plant from actual/future market and discard
        :return: The lowest value power plant in the market
        """
        plant = self.market.pop(0)
        self.layout()
        return plant

    def auction_plant(self, plant):
        """
        Buy the specified plant from the actual market
        :param plant: The plant to buy from the market
        """
        self.market.remove(plant)

    def get_actual_market(self):
        """
        Get the actual market
        :return: The actual market
        """
        return self.actual

    def get_future_market(self):
        """
        Get the futures market
        :return: The future market
        """

        return self.future

    def get_market_size(self):
        """
        Get size of the actual + future market
        :return: Size of the market
        """
        return len(self.market)

    def add_plant_to_market(self, new_plant):
        """
        Adds a new power plant to the market
        :param new_plant: The plant to be added of type Plant
        """

        # If the new plant is empty, it means the draw stack is empty.
        # Don't do anything in this case.
        if new_plant is None:
            self.layout()
            return

        self.market.append(new_plant)
        self.layout()


    def set_game_step(self, step):
        """
        Sets the game step for the plant market so it knows how to reorganize
        :param step: The GameStep enum
        """
        self.game_step = step


    def layout(self):
        """
        Layout the plant market based on the current game step
        :return: True if everything is okay, False if there is some error (too many plants)
        """

        # Sort the market to order by increasing value
        self.market.sort()

        # Layout the market based on the step of the game
        if self.game_step == GameStep.STEP3:
            return self.layout_step3()
        else:
            return self.layout_step1_2()


    def layout_step1_2(self):
        """
        Layout actual and future markets based on steps 1 and 2 of game
        :return: False if the number of plants in market don't equal actual + future size. True otherwise
        """

        if len(self.market) != MARKET_FUT_SIZE + MARKET_ACT_SIZE:
            return False

        # Actual market is lowest cards, future market is everything else
        self.actual = self.market[0:MARKET_ACT_SIZE]
        self.future = self.market[-MARKET_FUT_SIZE:]

        return True

    def layout_step3(self):
        """
        Layout the actual market for step 3
        :return: False if market size is not equal to s3 actual size. True otherwise
        """

        # We do this to make a deep copy.
        # In step 3, there is no future market.
        self.actual = self.market[:]

        return True

    def remove_plants_below_value(self, value):
        """
        Get the number of plants below a given value.
        This is used in phase 4 when removing small plants.
        Only plants from the actual market are removed
        :param value: The value to check
        :return: The number of plants removed
        """

        # Get number of plants to remove from actual market
        self.layout()

        num_removed = 0
        for plant in self.actual:

            # If the value of plant in actual market is less than specified,
            # remove from main market and add one to the counter
            if plant.get_value() <= value:
                num_removed += 1
                self.market.remove(plant)

        return num_removed





