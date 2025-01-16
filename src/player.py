
# Player created as a class to encapsulate data for each player, and allow me to keep score calculation logic here
class Player:
    
    def __init__(self, ace_value):
        self.hand = []
        self.stand = False
        self.busted = False
        self.score = 0
        self.ace_value = ace_value

        self.values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': self.ace_value}

    def add_card(self, card):
        if self.stand:
            return
        
        self.hand.append(card)

    def set_ace_value(self, value):
        self.ace_value = value
        self.values['A'] = value


    def get_card_rank(self, card):
        """Helper method to get the rank of a card, pythons dyamic type system means we have either card or dict"""
        if isinstance(card, dict): 
            return card['rank']
        else: 
            return card.rank

    def calculate_score(self):
        score = 0
        num_aces = 0

        for card in self.hand:
            rank = self.get_card_rank(card) 
            score += self.values[rank]
            if rank == 'A':
                num_aces += 1

        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1

        self.score = score

        return score
    
    def print_hand(self):
        for card in self.hand:
            print(card)
        
        print("Score: ", self.calculate_score())