import json
import os
from random import shuffle
from powergrid import PlayerBoard, PlantDeck, PlantMarket, ResourceType, ResourceMarket, PowerGridSettings, GameStep

class PowerGridSimulator(object):

    def __init__(self, num_players, config_file):
        """
        The simulator that will track resource usage and cost over time

        :param num_players: Number of players in this simulation
        :param settings_file: Path to the game settings file
        :param resource_file: Path to resource file
        :param plant_deck_file: Path to the plant deck file
        :param player_file: Path to the player names file (optional)
        """

        config_path = os.path.dirname(config_file)
        with open(config_file, 'r') as f:
            config_map = json.loads(f.read())

            settings_file = os.path.join(config_path, config_map["MainSettings"])
            resource_file = os.path.join(config_path, config_map["InitResources"])
            plant_deck_file = os.path.join(config_path, config_map["PlantDeck"])
            player_file = os.path.join(config_path, config_map["Players"])
            payout_file = os.path.join(config_path, config_map["Payout"])

        self.num_players = num_players

        self.settings = PowerGridSettings(num_players, settings_file)

        self.resource_file = resource_file

        self.plant_deck = PlantDeck(plant_deck_file)
        self.plant_market = PlantMarket()

        self.current_step = GameStep.STEP1
        self.replenish_rates = self.settings.replenish_rates[self.current_step]

        self.resource_market = ResourceMarket(resource_file)
        self.initialize_plant_market()

        # These players don't actually mean anything, but we need it to know which
        # player was which.
        player_list = list(range(num_players))
        if player_file is not None:
            with open(player_file, 'r') as f:
                profiles = json.loads(f.read())

                # Shuffle the players around then get the first few
                shuffle(profiles)
                player_list = profiles[0:num_players]

        self.players = []
        for player in player_list:
            self.players.append(PlayerBoard(self.settings.max_plants, player))

        self.results = {}


    def initialize_plant_market(self):

        base_market = self.plant_deck.setup_deck()
        for plant in base_market:
            self.plant_market.add_plant_to_market(plant)

    def trigger_step2(self):
        """
        Check if conditions have been met to trigger step 2
        :return: True if conditions met for step 2. False otherwise
        """

        # First see if conditions have been met to trigger the step
        step2_condition = False
        for name, player in self.players:

            if player.get_num_cities() >= self.settings.step2_trigger:
                step2_condition = True
                break

        # Return false if we can't go to step 2 yet.
        if not step2_condition:
            return False

        # Perform step 2 trigger actions:
        # Update replenish rates and remove the lowest plant and repopulate market
        self.replenish_rates = self.settings.replenish_rates[GameStep.STEP2]
        self.plant_market.remove_lowest()
        card = self.plant_deck.draw()
        self.plant_market.add_plant_to_market(card)


    def trigger_step3(self, update_rates=True):
        """
        Check if conditions have been met to trigger step 3
        :update_rates: Flag to tell whether or not the game should update its rates
        :return: True if conditions met for step 3. False otherwise
        """

        self.plant_market.remove_lowest()
        self.plant_deck.shuffle()
        self.current_step = GameStep.STEP3
        self.plant_market.set_game_step(GameStep.STEP3)

        if update_rates:
            self.replenish_rates = self.settings.replenish_rates[GameStep.STEP3]


    def determine_hybrid_combinations(self, required_fuel):
        """
        Determine all combinations of fuel that will satisfy the hybrid fuel requirement
        :param required_fuel: The amount of fuel needed to power the plant
        :return: All combinations of conditions to satisfy the fuel reqs
        """

        hybrid_combinations =  []
        rsc_usage = {
            ResourceType.COAL: 0,
            ResourceType.OIL: 0
        }
        for coal_usage in range(1, required_fuel + 1):

            rsc_usage[ResourceType.COAL] = coal_usage
            rsc_usage[ResourceType.OIL] = required_fuel - coal_usage
            hybrid_combinations.append(rsc_usage)

            if coal_usage != required_fuel - coal_usage:
                rsc_usage[ResourceType.COAL] = required_fuel - coal_usage
                rsc_usage[ResourceType.OIL] = coal_usage
                hybrid_combinations.append(rsc_usage)

        return hybrid_combinations


    def check_game_end(self):
        """
        Check if condition met to end the game
        :return:
        """

        for player in self.players:

            # If any player has enough cities to end the game, do set the end condition
            if player.get_num_cities() >= self.settings.end_condition:
                return True

        return False


    def simulate(self):
        raise NotImplementedError()

    def phase_1(self, first_turn):
        raise NotImplementedError()

    def phase_2(self):
        raise NotImplementedError()

    def phase_3(self):
        raise NotImplementedError()

    def phase_4(self):
        raise NotImplementedError()

    def phase_5(self):
        raise NotImplementedError()


