from .player import Player

class Dealer(Player):
    def __init__(self, ace_value, hit_on_soft_17=True):
        super().__init__(ace_value)
        self.hit_on_soft_17 = hit_on_soft_17

    def should_hit(self):
        """Determine if the dealer should hit based on their current hand"""
        score = self.calculate_score()
        if score < 17:
            return True
        elif score == 17 and self.hit_on_soft_17:
            # Check if the hand is a soft 17 (contains an Ace counted as 11)
            return self._is_soft_17()
        return False

    def _is_soft_17(self):
        """Check if the dealer's hand is a soft 17"""
        score = 0
        aces = 0
        for card in self.hand:
            if card.rank == 'A':
                aces += 1
            score += self.values[card.rank]

        # Adjust for Aces if score > 21
        while score > 21 and aces:
            score -= 10
            aces -= 1

        # If the score is 17 and there's at least one Ace counted as 11, it's a soft 17
        return score == 17 and any(card.rank == 'A' and self.values[card.rank] == 11 for card in self.hand)

    def calculate_score_excluding_first_card(self):
        """Calculate the score excluding the first card in the hand"""
        if not self.hand:
            return 0

        score = sum(self.values[card.rank] for card in self.hand[1:])
        aces = sum(1 for card in self.hand[1:] if card.rank == 'A')

        # Adjust for Aces if score > 21
        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score