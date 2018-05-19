import json
import powergrid

if __name__ == '__main__':

    deck = powergrid.PlantDeck('power_plants.csv')
    deck.setup_deck()