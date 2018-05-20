import json
from powergrid import powergrid_utils, GameStep

class PowerGridSettings(object):

    def __init__(self, num_players, settings_file):

        settings = None
        with open(settings_file, 'r') as f:
            settings = json.loads(f.read())

        settings = settings[str(num_players)]

        # Set up the easy things
        self.num_regions = settings["Regions"]
        self.discard_num = settings["Discard"]
        self.max_plants = settings["MaxPlants"]
        self.step2_trigger = settings["Step2Trigger"]
        self.end_condition = settings["GameEnd"]

        replenish = settings["Replenish"]

        self.replenish_rates = {}
        for step, rates in replenish.items():

            step_rates = {}
            for resource, resource_rate in rates.items():

                resource_type = powergrid_utils.resource_type_from_string(resource)
                step_rates[resource_type] = resource_rate

            if step == "1":
                step_enum = GameStep.STEP1
            elif step == "2":
                step_enum = GameStep.STEP2
            else:
                step_enum = GameStep.STEP3

            self.replenish_rates[step_enum] = step_rates
