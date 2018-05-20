import json
import os
from random import shuffle
from powergrid import PlayerBoard, PlantDeck, PlantMarket, ResourceType, ResourceMarket, PowerGridSettings, GameStep
from simulation import PowerGridSimulator

class ResourceAnalysisSim(PowerGridSimulator):

    def __init__(self, num_players, config_file):
        """
        The simulator that will track resource usage and cost over time

        :param num_players: Number of players in this simulation
        :param settings_file: Path to the game settings file
        :param resource_file: Path to resource file
        :param plant_deck_file: Path to the plant deck file
        :param player_file: Path to the player names file (optional)
        """
        PowerGridSimulator.__init__(num_players, config_file)


    def simulate(self):

        # Continue going until the game is over
        game_end = False
        first_turn = True
        step_3_wait = False
        round = 0

        cost_report = {
            ResourceType.COAL : 0,
            ResourceType.OIL : 0,
            ResourceType.TRASH : 0,
            ResourceType.URANIUM : 0
        }

        for resource, cost in cost_report.items():
            cost_report[resource] = self.resource_market.get_available_resources(resource)

        self.results[round] = cost_report.copy()



        while not game_end:

            round += 1

            # Check to redo resupply rates if step 3 happened in phase 5
            if self.current_step == GameStep.STEP3 and step_3_wait:
                self.replenish_rates = self.settings.replenish_rates[GameStep.STEP3]
                self.plant_market.set_game_step(GameStep.STEP3)


            # Phase 1
            # Determine player order based on number of cities/plant value
            # If it's the first turn, the turn order is determined randomly.
            self.phase_1(first_turn)


            # Phase 2
            # Starting with player one, go around and buy the highest plant in market
            # If they need to replace a plant, replace the lowest one.
            # There are no auctions. The players always buy a new plant.
            # Check for step 3
            self.phase_2()

            # Phase 3
            # Going in reverse, buy only the resources needed to power all the plants
            # If it is not possible to buy them, do not.
            # Assume the player has enough Elektro to make purchase
            self.phase_3()

            self.phase_4()


            for resource, cost in cost_report.items():
                cost_report[
                    resource] = self.resource_market.get_available_resources(
                    resource)
            self.results[round] = cost_report.copy()

            # Check for end of game
            if self.check_game_end():
                break

            # Phase 5
            # Power plants
            # Get money
            # Resupply
            step_3_wait = self.phase_5()

            if first_turn:
                first_turn = False


        return self.results



    def phase_1(self, first_turn):
        """
        Arrange player order based on cities/plants
        If first turn, randomly arrange players
        """
        if first_turn:
            shuffle(self.players)
        else:
            self.players.sort()

    def phase_2(self):

        step3_trigger = False
        for player in self.players:

            # Relatively simple here. We're just going to have each player
            # take the most valuable plant (no actual auctioning)

            actual_market = self.plant_market.get_actual_market()

            if not actual_market:
                break

            plant = actual_market[-1]

            self.plant_market.auction_plant(plant)

            # First try to add the plant
            if len(player.get_plants()) < self.settings.max_plants:
                player.add_plant(plant)
            else:
                # If we can't add it, we have to replace. Replace
                # the least valuable plant.
                current_plants = player.get_plants()
                old_plant = current_plants[0]

                player.replace_plant(plant, old_plant)


            # Draw a replacement
            card = self.plant_deck.draw()

            # Again, step 3 check.
            if card is not None and card.is_step3():
                self.plant_deck.shuffle()
                step3_trigger = True

            self.plant_market.add_plant_to_market(card)

        if step3_trigger:

            self.plant_market.remove_lowest()
            self.plant_market.remove_highest()

            self.replenish_rates = self.settings.replenish_rates[GameStep.STEP3]
            self.current_step = GameStep.STEP3
            self.plant_market.set_game_step(GameStep.STEP3)






    def phase_3(self):

        for player in reversed(self.players):

            # For each plant in a player's board, we want to add minimum needed fuel
            for plant in player.get_plants():

                # Check fuel type and required fuel (handle hybrids later)
                resource_type = plant.get_resource_type()
                fuel_required = plant.get_required_fuel()

                plant_cost = 0



                if resource_type == ResourceType.HYBRID:

                    hybrid_sols = self.determine_hybrid_combinations(fuel_required)

                    # find the lowest cost of all solutions
                    min_cost = 1000
                    used_solution = {}
                    for solution in hybrid_sols:

                        cost = self.resource_market.calculate_cost_dict(solution)

                        if cost < min_cost:
                            used_solution = solution
                            min_cost = cost

                    self.resource_market.buy_multiple(used_solution)

                    # Now that we have the solution to use, just add it to the plant
                    for resource, amount in used_solution.items():

                        player.add_resources_to_plant(plant, resource, amount)
                        player.add_resource_usage_to_plan(plant, resource, amount)

                    plant_cost = min_cost

                elif resource_type != ResourceType.RENEWABLE:

                    # Note the cost for analysis
                    plant_cost = self.resource_market.calculate_cost(resource_type, fuel_required)

                    # Actually buy the resources to remove them from the market
                    self.resource_market.buy(resource_type, fuel_required)

                    # Add to storage
                    player.add_resources_to_plant(plant, resource_type, fuel_required)
                    player.add_resource_usage_to_plan(plant, resource_type, fuel_required)




    def phase_4(self):
        """
        Perform phase 4 actions
        :return:
        """

        # Phase 4
        # Add dummy cities to the player based on the plants they have
        # in their plant list

        max_cities = -1
        for player in reversed(self.players):

            # Get the difference between number of cities and total output
            delta = player.get_num_cities() - player.get_total_output()

            if delta < 0:
                player.add_cities([0] * abs(delta))

            max_cities = max(max_cities, player.get_num_cities())

        plants_removed = 1
        while plants_removed != 0:
            plants_removed = self.plant_market.remove_plants_below_value(
                max_cities)

            # We removed x plants, so add them back in. Check for step 3
            for _ in range(plants_removed):
                card = self.plant_deck.draw()

                # Check for step 3
                if card is not None and card.is_step3():
                    self.plant_market.remove_lowest()
                    self.plant_deck.shuffle()
                    self.replenish_rates = self.settings.replenish_rates[
                        GameStep.STEP3]
                    self.current_step = GameStep.STEP3
                    self.plant_market.set_game_step(GameStep.STEP3)
                else:
                    self.plant_market.add_plant_to_market(card)


    def phase_5(self):

        step_3_wait = False
        usage_report = {
            ResourceType.COAL: 0,
            ResourceType.OIL: 0,
            ResourceType.TRASH: 0,
            ResourceType.URANIUM: 0
        }
        for player in self.players:

            # Use previously generated usage plans to power plants
            report, cities_powered = player.power_plants()
            # player.earn_elektro(self.settings.payout[cities_powered])

            # Update how many resources can go back in the pool
            for resource, usage in report.items():
                usage_report[resource] += usage

        # Remove highest power plant
        if self.current_step == GameStep.STEP3:
            self.plant_market.remove_lowest()
        else:
            removed_plant = self.plant_market.remove_highest()
            self.plant_deck.add_to_bottom(removed_plant)

        # Add new plant
        plant = self.plant_deck.draw()

        # Check for step 3
        if plant is not None and plant.is_step3():
            self.plant_market.remove_lowest()
            self.plant_deck.shuffle()
            step_3_wait = True
            self.current_step = GameStep.STEP3
        else:
            self.plant_market.add_plant_to_market(plant)

        # Update available pool of resources and
        # Re-supply the resource market
        self.resource_market.add_available_resources(usage_report)
        self.resource_market.replenish_market(self.replenish_rates)


        return step_3_wait
