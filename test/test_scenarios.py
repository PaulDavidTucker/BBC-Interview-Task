import unittest
from src.player import Player
from src.deck import Deck
from src.game import Game
from src.card import Card


class ScenarioTests(unittest.TestCase):
    def setUp(self):
        self.player = Player(ace_value=11)
        self.deck = Deck()
        self.game = Game(menu_enabled=False)

    # Scenario 1: Opening Hand

    def test_deal_initial_hand(self):
        """Test that a player is dealt two cards initially"""

        self.assertEqual(len(self.game.players[0].hand), 2)

    # Scenario 2: Hitting

    def test_hit(self):
        """Test that hitting adds a card and updates the score"""

        initial_score = self.game.players[0].calculate_score()
        self.game.players[0].add_card(Card('5', 'Hearts'))

        self.assertEqual(len(self.game.players[0].hand), 3)
        self.assertNotEqual(self.game.players[0].calculate_score(), initial_score)

    # Scenario 3: Standing

    def test_stand(self):
        """Test that standing does not add a card and evaluates the score"""

        self.game.players[0].stand = True
        initial_score = self.game.players[0].calculate_score()
        self.game.players[0].add_card(Card('5', 'Hearts'))

        self.assertEqual(len(self.game.players[0].hand), 2)
        self.assertEqual(self.game.players[0].calculate_score(), initial_score)

    # Scenario 4: Valid hand (Score <= 21)

    def test_valid_hand(self):
        """Test that a score of 21 or less is valid"""

        self.player.add_card(Card('10', 'Hearts'))
        self.player.add_card(Card('7', 'Diamonds'))

        self.assertLessEqual(self.player.calculate_score(), 21)
        self.assertTrue(self.player.calculate_score() > 0)

    # Scenario 5: Bust (Score > 21)

    def test_bust(self):
        """Test that a score of 22 or more is a bust"""

        self.player.add_card(Card('10', 'Hearts'))
        self.player.add_card(Card('9', 'Diamonds'))
        self.player.add_card(Card('5', 'Clubs'))

        self.assertGreater(self.player.calculate_score(), 21)

    # Scenario 6: King and ace (Score = 21)

    def test_king_and_ace(self):
        """Test that a hand with a king and an ace scores 21"""

        self.player.add_card(Card('K', 'Hearts'))
        self.player.add_card(Card('A', 'Diamonds'))

        self.assertEqual(self.player.calculate_score(), 21)

    # Scenario 7: King, queen, and ace (Score = 21)

    def test_king_queen_ace(self):
        """Test that a hand with a king, queen, and ace scores 21"""

        self.player.add_card(Card('K', 'Hearts'))
        self.player.add_card(Card('Q', 'Diamonds'))
        self.player.add_card(Card('A', 'Clubs'))

        self.assertEqual(self.player.calculate_score(), 21)

    # Scenario 8: Nine, ace, and ace (Score = 21)

    def test_nine_and_two_aces(self):
        """Test that a hand with a nine and two aces scores 21"""

        self.player.add_card(Card('9', 'Hearts'))
        self.player.add_card(Card('A', 'Diamonds'))
        self.player.add_card(Card('A', 'Clubs'))

        self.assertEqual(self.player.calculate_score(), 21)

if __name__ == "__main__":
    unittest.main()