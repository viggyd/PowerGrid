from powergrid import ResourceType

def resource_type_from_value(value):
    if value == 0:
        return ResourceType.COAL
    elif value == 1:
        return ResourceType.OIL
    elif value == 2:
        return ResourceType.TRASH
    elif value == 3:
        return ResourceType.URANIUM
    elif value == 4:
        return ResourceType.RENEWABLE
    elif value == 5:
        return ResourceType.HYBRID
    else:
        return ResourceType.COAL

def resource_type_from_string(in_string):

    resource_string = in_string.upper()

    if resource_string == "COAL":
        return ResourceType.COAL
    elif resource_string == "OIL":
        return ResourceType.OIL
    elif resource_string == "TRASH":
        return ResourceType.TRASH
    elif resource_string == "URANIUM":
        return ResourceType.URANIUM
    elif resource_string == "RENEWABLE":
        return ResourceType.RENEWABLE
    elif resource_string == "HYBRID":
        return ResourceType.HYBRID
    else:
        return ResourceType.COAL

def string_from_type(resource_type):

    if resource_type == ResourceType.COAL:
        return "Coal"
    elif resource_type == ResourceType.OIL:
        return "Oil"
    elif resource_type == ResourceType.TRASH:
        return "Trash"
    elif resource_type == ResourceType.URANIUM:
        return "Uranium"
    elif resource_type == ResourceType.RENEWABLE:
        return "Renewable"
    elif resource_type == ResourceType.HYBRID:
        return "Hybrid"
    else:
        return "Unknown"