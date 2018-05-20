from powergrid import ResourceType
from powergrid import powergrid_utils

class Plant(object):
    """
    Plant
    a: Value
    a: Type
    a: Needed fuel
    a: Output
    a: IsStep3?
    a: Primary storage
    a: Secondary storage


    m: Add resources to plant
    m: Remove resources from plant
    m: Get stored resources
    """

    def __init__(self, value, type, fuel, output, step3=False):

        self.value = value
        self.type = type
        self.fuel = fuel
        self.output = output

        # Determines if this is a Step 3 card or not
        self.step3 = step3


    def get_value(self):
        return self.value

    def get_resource_type(self):
        return self.type

    def get_output(self):
        return self.output

    def get_required_fuel(self):
        return self.fuel

    def is_step3(self):
        return self.step3

    def __repr__(self):

        if self.step3:
            return "Step 3"

        rep_str = "Val: {self.value}. {self.fuel} {0:s} -> {self.output} Cities. ".format(powergrid_utils.string_from_type(self.type), self=self)

        return rep_str

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash((self.value, self.step3))





