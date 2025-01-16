# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CARD_HEIGHT = 96
CARD_WIDTH = 64

BUTTON_POSITIONS = {
    "HIT": (SCREEN_WIDTH / 4 , 500, 100, 50),
    "STAND": (SCREEN_WIDTH / 2, 500, 100, 50),
}

COLOURS = {
    "GREEN": (0, 128, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "YELLOW": (255, 255, 0),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
}

RULES = [
            "Welcome to Blackjack!",
            "Rules:",
            "- Get as close to 21 as possible without going over.",
            "- Number cards are worth their face value.",
            "- Face cards (J, Q, K) are worth 10.",
            "- Aces can be worth 1 or 11.",
            "- Dealer must hit until their score is at least 17."
            "- If you bust with an ace/s in your hand, 10 will be subtracted from the score from your score."
        ]