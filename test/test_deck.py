import unittest
from src.deck import Deck

# tests for deck implementation
class DeckTestCase(unittest.TestCase):

    def setUp(self):  
        self.deck = Deck()

    def tearDown(self): 
        pass

    def test_deck_creation(self):
        """Test that a deck is created with 52 cards """
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_shuffle_is(self):
        """Test that the deck is shuffled"""
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle()
        self.assertNotEqual(deck.cards, original_order)

    def test_shuffle_twice(self):
        """Test that the deck is shuffled twice"""
        self.deck.shuffle()
        first_shuffle = self.deck.cards.copy()
        self.deck.shuffle()
        second_shuffle = self.deck.cards.copy()
        self.assertNotEqual(first_shuffle, second_shuffle)

    # deal tests
    def test_deal(self):
        """ Check that a card is removed from the deck when dealt """
        card = self.deck.deal_card()
        self.assertEqual(len(self.deck.cards), 51)
        self.assertNotIn(card, self.deck.cards)

    def test_deal_multiple(self):
        """ Check that multiple cards are removed from the deck when dealt """
        for _ in range(5):
            cards = self.deck.deal_card()
        self.assertEqual(len(self.deck.cards), 47)
        self.assertNotIn(cards, self.deck.cards)

    def test_deal_empty_deck(self): 
        """ Check that an error is raised when dealing from an empty deck"""
        for _ in range(52):
            self.deck.deal_card()

        with self.assertRaises(ValueError):
            self.deck.deal_card()
            self.assertEqual(len(self.deck.cards), 0)

    def test_deal_specific_card(self):
        """ Check that a specific card is removed from the deck when dealt"""
        card = self.deck.deal_specific_card('A', 'Hearts')

        self.assertEqual(len(self.deck.cards), 51)
        self.assertNotIn(card, self.deck.cards)

    def test_deal_specific_card_not_in_deck(self):
        """ Check that an error is raised when dealing a card not in the deck"""
        card = self.deck.deal_specific_card('A', 'Hearts')
        
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'Hearts')

        with self.assertRaises(ValueError):
            self.deck.deal_specific_card('A', 'Hearts')
    
    def test_deal_specific_card_empty_deck(self):
        """ Check that an error is raised when dealing from an empty deck"""
        for _ in range(52):
            self.deck.deal_card()

        with self.assertRaises(ValueError):
            self.deck.deal_specific_card('A', 'Hearts')
            self.assertEqual(len(self.deck.cards), 0)

    
if __name__ == '__main__':
    unittest.main()
