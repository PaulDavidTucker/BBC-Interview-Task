import unittest
from src.card import Card

class TestCard(unittest.TestCase):

    def test_card_creation(self):
        """Test that a card is created with a rank and suit """
        card = Card('A', 'Spades')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'Spades')

    def test_card_representation(self):
        
        """Test that the card is represented as a string correcrly."""
        card = Card('10', 'Hearts')
        self.assertEqual(repr(card), '10 of Hearts')
    
    def test_card_representation_ace(self):
        """Test a non number card is represented as a string correctly"""
        card = Card('A', 'Diamonds')
        self.assertEqual(repr(card), 'A of Diamonds')

    