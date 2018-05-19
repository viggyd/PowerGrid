from powergrid import ResourceType


class Plant(object):
    """
    Plant
    -> Value
    -> Powered cities
    -> Primary Resource
    -> Secondary Resource
    -> Resources on Plant
    """

    def __init__(self, value, type, fuel, output, step3=False):

        self.value = value
        self.type = type
        self.fuel = fuel
        self.output = output

        self.storage = 0

        # Determines if this is a Step 3 card or not
        self.step3 = step3

        # Used for hybrid plants.
        # Secondary storage is always oil
        self.sec_storage_type = ResourceType.OIL
        self.sec_storage = 0 # Used for hybrid plants

    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def get_output(self):
        return self.output

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





