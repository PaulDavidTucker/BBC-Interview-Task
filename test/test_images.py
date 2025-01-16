import unittest
import pygame
from src.utils import get_card_image
from src.constants import CARD_WIDTH, CARD_HEIGHT

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""

        # Create a dummy sprite sheet for testing
        self.sprite_sheet = pygame.Surface((832, 576))  # 13 ranks x 4 suits
        self.card_width = CARD_WIDTH
        self.card_height = CARD_HEIGHT
        self.scale_factor = 2

    def test_get_card_image(self):
        """Test that get_card_image returns the correct card images"""

        card_images, scaled_width, scaled_height = get_card_image(
            sprite_sheet=self.sprite_sheet,
            card_width=self.card_width,
            card_height=self.card_height,
            SCALE_FACTOR=self.scale_factor
        )

        self.assertEqual(scaled_width, self.card_width * self.scale_factor)
        self.assertEqual(scaled_height, self.card_height * self.scale_factor)

        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

        # 13 ranks x 4 suits + 1 card back
        self.assertEqual(len(card_images), (len(ranks) * len(suits)) + 1)

        for key, image in card_images.items():
            # tuple of rank and suit
            self.assertIsInstance(key, tuple)  
            self.assertEqual(len(key), 2)  

            # need the instance of any image object returned to be a surface, otherwise we cannot blitz with pygame
            self.assertIsInstance(image, pygame.Surface)

            # check our image scales to the correct dimensions after scale
            self.assertEqual(image.get_width(), scaled_width)
            self.assertEqual(image.get_height(), scaled_height)

    def test_get_card_image_with_invalid_input(self):

        """Test that get_card_image handles invalid input gracefully"""

        with self.assertRaises(ValueError):
            # pass in None here to check if we ever get the pathing to assets wrong etc
            get_card_image(
                sprite_sheet=None,
                card_width=self.card_width,
                card_height=self.card_height,
                SCALE_FACTOR=self.scale_factor
            )

        with self.assertRaises(ValueError):
            # invalid card dimensions
            get_card_image(
                sprite_sheet=self.sprite_sheet,
                card_width=0,  # Invalid width
                card_height=self.card_height,
                SCALE_FACTOR=self.scale_factor
            )

        with self.assertRaises(ValueError):
            # invalid scale factor
            get_card_image(
                sprite_sheet=self.sprite_sheet,
                card_width=self.card_width,
                card_height=self.card_height,
                SCALE_FACTOR=0  # Invalid scale factor
            )

if __name__ == "__main__":
    unittest.main()