from aenum import Enum

class ResourceType(Enum):

    COAL = 0, 'Coal'
    OIL = 1, 'Oil'
    TRASH = 2, 'Trash'
    URANIUM = 3, 'Uranium'
    RENEWABLE = 4, 'Renewable'
    HYBRID = 5, 'Hybrid'

    # print(ResourceType.OIL.value[1])