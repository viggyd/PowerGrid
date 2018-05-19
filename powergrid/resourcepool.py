import math
from powergrid import ResourceType, GameStep

"""
Resource Pool
    -> Resource Type
    -> Total Resources
    -> Resources available
    -> Replenish rate
    -> Game Phase
    -> Num Players
"""


class ResourcePool(object):

    def __init__(self, type, pool_size, initial):

        self.type = type
        self.total_resources = pool_size
        self.available = self.total_resources

        self.pool = [False] * self.total_resources
        self.pool[-initial:] = [True] * initial


    def replenish(self, amount):

        pos = -1
        while amount > 0 and pos >= -len(self.pool):

            if not self.pool[pos]:
                self.pool[pos] = True
                amount -= 1

            pos -= 1


    def calculate_cost(self, amount):

        # For most resources, the cost goes up by 1 every 3.
        # Thus, the price of a given one is floor((pos/3)) + 1
        # Uranium is different, it goes up by 1 every resource until 7,
        # then it does 8, 10, 12, 14, 16
        # (8, 10) (9, 12) (10, 14) (11, 16) -> 2x - 6

        cost = 0
        for i in range(len(self.pool)):

            if self.pool[i]:

                if self.type == ResourceType.URANIUM:
                    if i > 7:
                        cost += 2 * i - 6
                    else:
                        cost += i

                else:
                    cost += math.floor(i/3) + 1

                amount -= 1

                if not amount:
                    break

        else: # We were not able to buy all the resources. :(
            return -1


        return cost


    def buy(self, amount):

        available = self.get_available_resources()

        if available < amount:
            return False

        removed = 0

        for i in range(len(self.pool)):

            if self.pool[i]:
                self.pool[i] = False

                removed += 1

            if removed == amount:
                break

        return True

    def get_available_resources(self):
        return self.pool.count(True)

    def get_type(self):
        return self.type

    def __repr__(self):

        rep_str = str(self.type)
        rep_str += ': '

        for i in range(len(self.pool)):

            if self.pool[i]:

                if self.type == ResourceType.URANIUM:
                    if i > 7:
                        rep_str += str(2 * i - 6)
                    else:
                        rep_str += str(i)

                else:
                    rep_str += str(math.floor(i/3) + 1)

        return rep_str
