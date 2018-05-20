from powergrid import ResourceType


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

    def get_type(self):
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

        rep_str = "Val: {self.value}. {self.fuel} {self.type.value[1]} -> {self.output} Cities. ".format(self=self)

        if self.type == ResourceType.HYBRID:
            rep_str += "Coal: {self.storage}. Oil: {self.sec_storage}".format(self=self)

        else:
            rep_str += "Storage: {self.storage}".format(self=self)

        return rep_str

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash((self.value, self.step3))





