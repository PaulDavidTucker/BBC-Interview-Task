import unittest
from src.dealer import Dealer
from src.card import Card

class TestDealer(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer(ace_value=11)

    def test_should_hit_under_17(self):
        """Test that the dealer should hit if the score is under 17."""

        self.dealer.add_card(Card('10', 'Hearts'))
        self.dealer.add_card(Card('6', 'Diamonds'))

        self.assertTrue(self.dealer.should_hit())

    def test_should_hit_on_soft_17(self):
        """Test that the dealer should hit on soft 17 if hit_on_soft_17 is True."""

        self.dealer.add_card(Card('A', 'Hearts'))
        self.dealer.add_card(Card('6', 'Diamonds'))
        
        self.assertTrue(self.dealer.should_hit())

    def test_should_not_hit_on_hard_17(self):
        """Test that the dealer should not hit on hard 17."""

        self.dealer.add_card(Card('10', 'Hearts'))
        self.dealer.add_card(Card('7', 'Diamonds'))

        self.assertFalse(self.dealer.should_hit())

    def test_should_not_hit_above_17(self):
        """Test that the dealer should not hit if the score is above 17."""

        self.dealer.add_card(Card('10', 'Hearts'))
        self.dealer.add_card(Card('8', 'Diamonds'))

        self.assertFalse(self.dealer.should_hit())

    def test_calculate_score_excluding_first_card(self):
        """Test score calculation excluding the first card."""

        self.dealer.add_card(Card('10', 'Hearts'))
        self.dealer.add_card(Card('7', 'Diamonds'))
        self.dealer.add_card(Card('4', 'Clubs'))

        self.assertEqual(self.dealer.calculate_score_excluding_first_card(), 11)

    def test_calculate_score_excluding_first_card_with_ace(self):
        """Test score calculation excluding the first card with an Ace."""

        self.dealer.add_card(Card('A', 'Hearts'))
        self.dealer.add_card(Card('7', 'Diamonds'))
        self.dealer.add_card(Card('4', 'Clubs'))

        self.assertEqual(self.dealer.calculate_score_excluding_first_card(), 11)

    def test_calculate_score_excluding_first_card_with_multiple_aces(self):
        """Test score calculation excluding the first card with multiple Aces."""

        self.dealer.add_card(Card('A', 'Hearts'))
        self.dealer.add_card(Card('A', 'Diamonds'))
        self.dealer.add_card(Card('9', 'Clubs'))

        # score calculation of 11 + 9
        self.assertEqual(self.dealer.calculate_score_excluding_first_card(), 20)

    def test_calculate_score_excluding_first_card_with_multiple_aces_bust(self):
        """Test score calculation excluding the first card with multiple Aces and bust."""

        self.dealer.add_card(Card('A', 'Hearts'))
        self.dealer.add_card(Card('A', 'Diamonds'))
        self.dealer.add_card(Card('9', 'Clubs'))
        self.dealer.add_card(Card('10', 'Clubs'))

        # score calculation of 11 + 1 + 9 + 10, we should reduce two aces to 1 as per blackjack rules
        self.assertEqual(self.dealer.calculate_score_excluding_first_card(), 20)

if __name__ == '__main__':
    unittest.main()