import random
from .card import Card

# Deck object here has an array comprised of card objects created from two defined arrays of ranks and suits. 
class Deck:
    def __init__(self):
        self.cards = self._create_deck()
        self.shuffle()

    def _create_deck(self):
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']
        return [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        # To show off a little algorithm knowledge here, I used the Fisher-Yates shuffle algorithm!
        # https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle

        # Start from the last element and swap one by one
        # don't need to run for the first element that's why i = len(arr) - 1

        for i in range(len(self.cards) - 1, 0, -1):
            # random index
            j = random.randint(0, i)
            # Swap arr[i] with the element at random index
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    # pops the last index card object from deck array
    def deal_card(self):
        if self.cards == [] or len(self.cards) == 0:
            raise ValueError("Deck is empty")
        
        return self.cards.pop()
    
    def deal_specific_card(self, rank, suit):
        for card in self.cards:
            if card.rank == rank and card.suit == suit:
                self.cards.remove(card)
                return card
            
        raise ValueError("Card not in deck")
        
    def __str__(self):
        deckString = ""

        for card in self.cards:
            deckString += " " + str(card) + "\n"

        return deckString