from aenum import IntEnum

class ResourceType(IntEnum):

    # COAL = 0, 'Coal'
    # OIL = 1, 'Oil'
    # TRASH = 2, 'Trash'
    # URANIUM = 3, 'Uranium'
    # RENEWABLE = 4, 'Renewable'
    # HYBRID = 5, 'Hybrid'

    COAL = 0
    OIL = 1
    TRASH = 2
    URANIUM = 3
    RENEWABLE = 4
    HYBRID = 5

    # print(ResourceType.OIL.value[1])