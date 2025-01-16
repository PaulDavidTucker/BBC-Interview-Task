import unittest
import pygame
from src.game import Game
from src.dealer import Dealer
from src.deck import Deck
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Mock classes
class MockMenu:
    def run(self, screen):
        return 1, 11  # num_players, ace_value

class MockCard:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

         # Disable menu for testing
        self.game = Game(menu_enabled=False) 
        self.game.menu = MockMenu()

    def test_initialization(self):
        """Test that the game initializes correctly."""

        self.assertEqual(len(self.game.players), 1)
        self.assertEqual(self.game.ace_value, 11)

        self.assertIsInstance(self.game.deck, Deck)
        self.assertIsInstance(self.game.dealer, Dealer)

        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)

    def test_deal_initial_cards(self):
        """Test that initial cards are dealt correctly."""

        self.assertEqual(len(self.game.players[0].hand), 2)
        self.assertEqual(len(self.game.dealer.hand), 2)

    def test_next_player(self):
        """Test that the next player is correctly selected."""

        self.game.next_player()
        self.assertEqual(self.game.current_player, 0)

    def test_handle_events_hit(self):
        """Test that hitting adds a card to the player's hand."""

        initial_hand_size = len(self.game.players[0].hand)

        # mocked a mouse click on the hit button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=self.game.hit_button.center)
        pygame.event.post(event)

        self.game.handle_events()
        self.assertEqual(len(self.game.players[0].hand), initial_hand_size + 1)

    def test_handle_events_stand(self):
        """Test that standing sets the player's stand flag"""

        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=self.game.stand_button.center)
        pygame.event.post(event)

        self.game.handle_events()
        self.assertTrue(self.game.players[0].stand)

    def test_evaluate_game_state_player_bust(self):
        """Test that the game evaluates correctly when the player busts"""

        self.game.players[0].add_card(MockCard('10', 'Hearts'))
        self.game.players[0].add_card(MockCard('10', 'Diamonds'))
        self.game.players[0].add_card(MockCard('5', 'Clubs'))

        self.game.evaluate_game_state()

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Dealer")

    def test_evaluate_game_state_dealer_bust(self):
        """Test that the game evaluates correctly when the dealer busts"""

        self.game.dealer.add_card(MockCard('10', 'Hearts'))
        self.game.dealer.add_card(MockCard('10', 'Diamonds'))
        self.game.dealer.add_card(MockCard('5', 'Clubs'))

        self.game.evaluate_game_state()

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Player(s)")

    def test_final_dealer_turn_hit_on_soft_17(self):
        """Test that the dealer hits on soft 17"""

        self.game.dealer.hit_on_soft_17 = True
        self.game.dealer.add_card(MockCard('A', 'Hearts'))  
        self.game.dealer.add_card(MockCard('6', 'Diamonds'))  

        self.game.final_dealer_turn()
        self.assertTrue(len(self.game.dealer.hand) > 2)

    def test_evaluate_game_state_player_wins(self):
        """Test that the game evaluates correctly when the player wins"""

        # Clear hands
        self.game.players[0].hand = []  
        self.game.dealer.hand = []

        self.game.players[0].add_card(MockCard('10', 'Hearts'))
        self.game.players[0].add_card(MockCard('7', 'Diamonds')) 
        self.game.dealer.add_card(MockCard('10', 'Hearts'))
        self.game.dealer.add_card(MockCard('6', 'Diamonds')) 

        self.game.evaluate_game_state()

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Player(s)")

    def test_evaluate_game_state_push(self):
        """Test that the game evaluates correctly when there is a tie"""

        # Clear hands
        self.game.players[0].hand = [] 
        self.game.dealer.hand = []  

        self.game.players[0].add_card(MockCard('10', 'Hearts'))
        self.game.players[0].add_card(MockCard('7', 'Diamonds'))
        self.game.dealer.add_card(MockCard('10', 'Hearts'))
        self.game.dealer.add_card(MockCard('7', 'Diamonds'))

        self.game.evaluate_game_state()

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Push (Tie)")

    def test_final_dealer_turn_no_hit_on_soft_17(self):
        """Test that the dealer does not hit on soft 17 when hit_on_soft_17 is False"""

        self.game.dealer.hand = [] 
        self.game.dealer.hit_on_soft_17 = False

        self.game.dealer.add_card(MockCard('A', 'Hearts')) 
        self.game.dealer.add_card(MockCard('6', 'Diamonds'))  

        self.game.final_dealer_turn()
        self.assertEqual(len(self.game.dealer.hand), 2)  

    def test_calculate_score_excluding_first_card(self):
        """Test that the dealer's score is calculated correctly excluding the first card"""

        self.game.dealer.hand = []  # Clear the dealer's hand

        self.game.dealer.add_card(MockCard('10', 'Hearts')) 
        self.game.dealer.add_card(MockCard('7', 'Diamonds'))  
        self.game.dealer.add_card(MockCard('7', 'Clubs')) 

        score = self.game.dealer.calculate_score_excluding_first_card()
        self.assertEqual(score, 14)  

    def test_reset_game(self):
        """Test that the game resets correctly"""

        self.game.players[0].add_card(MockCard('10', 'Hearts'))
        self.game.dealer.add_card(MockCard('10', 'Diamonds'))

        self.game.game_over = True
        self.game.reset_game()

        self.assertFalse(self.game.game_over)
        self.assertEqual(len(self.game.players[0].hand), 2)
        self.assertEqual(len(self.game.dealer.hand), 2)

    def test_handle_game_over_events_restart(self):
        """Test that the game restarts when 'R' is pressed"""

        self.game.game_over = True

        # Simulate a key press for restart
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        # add to pygame event queue
        pygame.event.post(event)

        result = self.game.handle_game_over_events()
        self.assertTrue(result) 

    def test_handle_game_over_events_quit(self):
        """Test that the game quits when 'Q' is pressed"""

        self.game.game_over = True
        
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)
        pygame.event.post(event)

        result = self.game.handle_game_over_events()
        self.assertFalse(result) 

if __name__ == "__main__":
    unittest.main()