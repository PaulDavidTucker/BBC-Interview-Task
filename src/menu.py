import pygame
from .constants import COLOURS, RULES

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.num_players = 1
        self.ace_value = 1

    def display_rules(self, screen):
        """Display the rules of Blackjack."""
        
        y_offset = 100
        for line in RULES:
            text = self.small_font.render(line, True, COLOURS["WHITE"])
            screen.blit(text, (100, y_offset))
            y_offset += 30

    def draw_button(self, screen, text, x, y, width, height, active=False):
        """Draw a button with hover effects."""

        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)
        color = COLOURS["BLUE"] if button_rect.collidepoint(mouse_pos) else COLOURS["RED"]

        if active:
            color = COLOURS["GREEN"]

        pygame.draw.rect(screen, color, button_rect)

        text_surface = self.font.render(text, True, COLOURS["WHITE"])
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
        return button_rect

    def run(self, screen):
        """Run the menu loop."""
        running = True
        while running:
            screen.fill(COLOURS["GREEN"])

            self.display_rules(screen)

            # Draw buttons for number of players and Ace value
            players_button = self.draw_button(screen, f"Players: {self.num_players}", 100, 400, 200, 50)
            ace_button = self.draw_button(screen, f"Ace Value: {self.ace_value}", 350, 400, 200, 50)
            start_button = self.draw_button(screen, "Start Game", 600, 400, 200, 50)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None, None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if players_button.collidepoint(event.pos):
                        self.num_players = min(self.num_players + 1, 4)  # Max 4 players
                    elif ace_button.collidepoint(event.pos):
                        self.ace_value = 1 if self.ace_value == 11 else 11
                    elif start_button.collidepoint(event.pos):
                        running = False

            pygame.display.flip()

        return self.num_players, self.ace_value