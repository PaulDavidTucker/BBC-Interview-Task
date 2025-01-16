import unittest
from src.player import Player
from src.card import Card

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(ace_value=11)

    def test_add_card(self):
        """Test that a card is added to the player's hand"""

        card = Card('10', 'Hearts')
        self.player.add_card(card)
        
        self.assertIn(card, self.player.hand)

    def test_stand_prevents_adding_card(self):
        """Test that no card is added when the player stands"""

        self.player.stand = True
        initial_hand_length = len(self.player.hand)

        # attempt to add a card after standing, see the length is unchanged
        self.player.add_card(Card('5', 'Hearts'))
        self.assertEqual(len(self.player.hand), initial_hand_length)

    def test_calculate_score_with_ace(self):
        """Test score calculation with an ace"""

        self.player.add_card(Card('A', 'Hearts'))
        self.player.add_card(Card('9', 'Diamonds'))

        # score calculation of 11 + 9
        self.assertEqual(self.player.calculate_score(), 20)

    def test_calculate_score_with_two_aces(self):
        """Test score calculation with multiple aces"""

        self.player.add_card(Card('A', 'Hearts'))
        self.player.add_card(Card('A', 'Diamonds'))
        self.player.add_card(Card('9', 'Clubs'))

        # score calculation of 11 + 1 + 9, we should reduce one Ace to 1 as per blackjack rules
        self.assertEqual(self.player.calculate_score(), 21)

    def test_calculate_score_with_multiple_aces(self):
        """Test score calculation with multiple aces"""

        self.player.add_card(Card('A', 'Hearts'))
        self.player.add_card(Card('A', 'Diamonds'))
        self.player.add_card(Card('A', 'Clubs'))
        self.player.add_card(Card('8', 'Clubs'))

        # score calculation of 11 + 1 + 1 + 8, we should reduce two aces to 1 as per blackjack rules
        self.assertEqual(self.player.calculate_score(), 21)

    def test_bust(self):
        """Test that the player busts when score exceeds 21"""

        self.player.add_card(Card('10', 'Hearts'))
        self.player.add_card(Card('10', 'Diamonds'))
        self.player.add_card(Card('5', 'Clubs'))

        self.assertTrue(self.player.calculate_score() > 21)

    def test_set_ace_value(self):
        """Test setting a new value for ace"""

        self.player.set_ace_value(1)
        self.assertEqual(self.player.values['A'], 1)

    def test_get_aces_value_one(self):
        """Test creating a player with an ace value of 1"""

        self.player = None
        self.player = Player(ace_value=1)

        self.player.add_card(Card('A', 'Hearts'))
        self.player.add_card(Card('9', 'Diamonds'))

        self.assertEqual(self.player.calculate_score(), 10)

if __name__ == '__main__':
    unittest.main()
