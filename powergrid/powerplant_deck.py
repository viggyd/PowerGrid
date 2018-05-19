import csv
import random
from powergrid import Plant, ResourceType

class PlantDeck(object):


    def __init__(self, plant_def):
        self.discard = []
        self.deck = []
        self.exile = []
        self.base_market = []

        self.construct_deck(plant_def)


    def construct_deck(self, plant_def_file):
        """
        Construct the deck of power plant cards

        Read the given definition file and add to the deck
        Make exceptions for the base market

        :param plant_def_file: Path to csv definition file
        """

        with open(plant_def_file, 'r') as f:

            PlantReader = csv.DictReader(f, delimiter=',')

            for row in PlantReader:

                card = Plant(
                        value=int(row['value']),
                        type=self._typefromvalue(int(row['type'])),
                        fuel=int(row['fuel']),
                        output=int(row['output'])
                    )

                # The values from 3--10 and 13 are special because they always
                # form the starting market.
                if 3 <= card.get_value() <= 10 or card.get_value() == 13:
                    self.base_market.append(card)
                else:
                    self.deck.append(card)



    def discard_cards(self, num_discard):

        """
        Discard cards from deck (based on settings)

        :param num_discard: Number of cards to exile
        """

        while num_discard > 0:

            card = random.choice(self.deck)

            self.exile.append(card)
            self.deck.remove(card)

            num_discard -= 1


    def shuffle(self):
        """
        Shuffle the deck of power plants
        """
        random.shuffle(self.deck)


    def setup_deck(self):
        """
        Set up the deck for a game
        """

        self.shuffle()

        # Remove the #13 card from base market and put it on top of the deck
        card_13 = self.base_market.pop(-1)
        self.deck.insert(0, card_13)

        self.deck.append(Plant(0, ResourceType.COAL, 0, 0, True))


    def add_to_bottom(self, plant):
        """
        Add power plant to bottom of deck

        :param plant: The plant to add to the bottom
        """

        self.deck.append(plant)

    def add_to_discard(self, plant):
        """
        Add card to discard pile
        :param plant: Plant to add to discard
        """

        self.discard.append(plant)

    def draw(self):
        """
        Draw a card from the deck
        :return: The next card in the deck to draw
        """
        return self.deck.pop(0)



    def _typefromvalue(self, value):

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
