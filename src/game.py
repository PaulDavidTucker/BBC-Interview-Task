import time
import pygame
from .deck import Deck
from .player import Player
from .dealer import Dealer
from .utils import get_card_image, draw_buttons, render_cards, render_dealer_cards, display_game_over
from .constants import CARD_HEIGHT, CARD_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_POSITIONS, COLOURS
from .menu import Menu

class Game:
    def __init__(self, menu_enabled=True):
        pygame.init()
        pygame.display.set_caption("BlackJack")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        if not menu_enabled:
            self.ace_value = 11
            self.menu = None
            self.num_players = 1
        else:
            self.menu = Menu()
            self.num_players, self.ace_value = self.menu.run(self.screen)

        if self.num_players is None:
            pygame.quit()
            return

        # Required game objects
        self.players = [Player(ace_value=self.ace_value) for _ in range(self.num_players)]
        self.deck = Deck()
        self.current_player = 0
        self.dealer = Dealer(ace_value=self.ace_value)

        # Sprite sheet from assets folder
        self.sprite_sheet = pygame.image.load("assets/playingCards.png")

        self.game_over = False
        self.winner = None

        self.hit_button = pygame.Rect(*BUTTON_POSITIONS.get("HIT"))
        self.stand_button = pygame.Rect(*BUTTON_POSITIONS.get("STAND"))
        self.font = pygame.font.Font(None, 36)

        self.card_images, self.scaled_width, self.scaled_height = get_card_image(
            sprite_sheet=self.sprite_sheet,
            card_width=CARD_WIDTH,
            card_height=CARD_HEIGHT,
            SCALE_FACTOR=2
        )

        self.deal_initial_cards()

    def deal_initial_cards(self):
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())

    def next_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if not self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hit_button.collidepoint(event.pos):
                        self.players[self.current_player].add_card(self.deck.deal_card())
                    elif self.stand_button.collidepoint(event.pos):
                        self.players[self.current_player].stand = True
                
        return True

    def evaluate_game_state(self):
        """Evaluate the game state and determine the winner."""

        dealer_score = self.dealer.calculate_score()

        all_players_busted = all(player.calculate_score() > 21 for player in self.players)

        if all_players_busted:
            self.game_over = True
            self.winner = "Dealer"
            return
        
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal_card())
            dealer_score = self.dealer.calculate_score()

        if dealer_score > 21:
            self.game_over = True
            self.winner = "Player(s)"
            return

        # Compare scores
        for i, player in enumerate(self.players):
            player_score = player.calculate_score()
            if player_score <= 21 and (dealer_score > 21 or player_score > dealer_score):
                self.game_over = True
                self.winner = f"Player {i + 1}"
            elif player_score == dealer_score:
                self.game_over = True
                self.winner = "Push (Tie)"

    def final_dealer_turn(self):
        """Simulate the dealer's turn if all players bust or stand."""

        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal_card())

            self.screen.fill(COLOURS.get("GREEN"))
            render_dealer_cards(self.screen, self.dealer, self.card_images, self.font, self.game_over)
            for i, player in enumerate(self.players):
                render_cards(self.screen, player.hand, 100, 300 + i * 150, f"Player {i + 1}", player, self.card_images, self.font)

            pygame.display.flip()

            # dealer thinking time
            time.sleep(1)

        self.evaluate_game_state()

    def reset_game(self):
        """Reset the game state for a new game."""
        self.game_over = False
        self.current_player = 0
        self.deck = Deck()
        self.dealer.hand.clear()
        for player in self.players:
            player.hand.clear()
            player.stand = False
            player.busted = False
        self.deal_initial_cards()
        self.num_players, self.ace_value = self.menu.run(self.screen)

    def handle_game_over_events(self):
        """Handle events during the game-over screen."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                # restart with new game object
                if event.key == pygame.K_r:  
                    self.reset_game()
                    return True
                # quit game
                if event.key == pygame.K_q:  # Quit
                    return False
        return True

    def run(self):
        running = True

        # ensure ace value set for all players
        for player in self.players:
            player.set_ace_value(self.ace_value)

        while running:
            if self.game_over:
                display_game_over(self.screen, self.dealer, self.players, self.winner, self.font)
                running = self.handle_game_over_events()
                if not running:
                    break
                continue

            running = self.handle_events()

            self.screen.fill(COLOURS.get("GREEN"))

            # Check if the current player has busted or stood
            current_player = self.players[self.current_player]
            if current_player.calculate_score() > 21 or current_player.stand:
                self.next_player()

            # Evaluate game state if all players have finished
            if all(player.stand or player.calculate_score() > 21 for player in self.players):
                self.final_dealer_turn()
                self.evaluate_game_state()
                self.game_over = True
                
            # Display current player's turn
            font = pygame.font.Font(None, 36)
            text = font.render(f"Player {self.current_player + 1}'s turn", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            # Starting position for current hand on screen
            current_x = 100
            for i, player in enumerate(self.players):
                hand_length = len(player.hand)
                hand_width = hand_length * CARD_WIDTH

                if i == self.current_player:
                    pygame.draw.rect(self.screen, COLOURS.get("YELLOW"), (current_x - 10, 290, 150, 40), 3)

                render_cards(self.screen, player.hand, current_x, 300, f"Player {i + 1}", player, self.card_images, self.font)
                current_x += hand_width + (CARD_WIDTH + 50)

            render_dealer_cards(self.screen, self.dealer, self.card_images, self.font, self.game_over)

            draw_buttons(self.screen, self.hit_button, self.stand_button, self.font)

            # display updates to screen
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()