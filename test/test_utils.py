import unittest
import pygame
from unittest.mock import Mock, patch
from src.utils import draw_buttons, render_cards, render_dealer_cards, display_game_over

class TestUtils(unittest.TestCase):

    # Had never used mocks in python before, documentation isnt too bad! 
    # https://docs.python.org/3/library/unittest.mock.html

    # patch was something quite interesting as it allows you to much objects and modules from libraries! 

    @patch('src.utils.pygame')
    def test_draw_buttons(self, mock_pygame):
        """Test draw_buttons function"""
        
        screen = Mock()
        hit_button = pygame.Rect(50, 50, 100, 50)
        stand_button = pygame.Rect(200, 50, 100, 50)
        font = Mock()

        # mocked mouse pos to allow .collidepoint to work
        mock_pygame.mouse.get_pos.return_value = (60, 60)
        draw_buttons(screen, hit_button, stand_button, font)

        self.assertTrue(mock_pygame.draw.rect.called)
        self.assertTrue(font.render.called)
        self.assertTrue(screen.blit.called)

    @patch('src.utils.pygame')
    def test_render_cards(self, mock_pygame):
        """Test render_cards function"""

        screen = Mock()
        hand = [Mock(rank='A', suit='Hearts'), Mock(rank='10', suit='Spades')]
        x, y = 100, 100

        label = "Player"
        player = Mock()
        player.calculate_score.return_value = 21

        card_images = {('A', 'Hearts'): Mock(), ('10', 'Spades'): Mock()}
        font = Mock()

        render_cards(screen, hand, x, y, label, player, card_images, font)

        self.assertTrue(screen.blit.called)
        self.assertTrue(font.render.called)

    @patch('src.utils.pygame')
    def test_render_dealer_cards(self, mock_pygame):
        """Test render_dealer_cards function"""
        screen = Mock()
        dealer = Mock()
        dealer.hand = [Mock(rank='A', suit='Hearts'), Mock(rank='10', suit='Spades')]
        card_images = {('A', 'Hearts'): Mock(), ('10', 'Spades'): Mock(), ('back', 'yellow'): Mock()}
        font = Mock()
        game_over = False

        render_dealer_cards(screen, dealer, card_images, font, game_over)

        self.assertTrue(screen.blit.called)
        self.assertTrue(font.render.called)

    @patch('src.utils.pygame')
    def test_display_game_over(self, mock_pygame):
        """Test display_game_over function"""

        screen = Mock()
        dealer = Mock()
        dealer.calculate_score.return_value = 20
        players = [Mock(), Mock()]
        
        players[0].calculate_score.return_value = 18
        players[1].calculate_score.return_value = 21
        winner = "Player 2"
        font = Mock()

        display_game_over(screen, dealer, players, winner, font)

        self.assertTrue(screen.fill.called)
        self.assertTrue(font.render.called)
        self.assertTrue(screen.blit.called)
        self.assertTrue(mock_pygame.display.flip.called)

if __name__ == '__main__':
    unittest.main()