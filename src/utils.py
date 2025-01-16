import pygame
from .constants import COLOURS, CARD_WIDTH, CARD_HEIGHT, SCREEN_WIDTH


def get_card_image(sprite_sheet, card_width, card_height, SCALE_FACTOR):
    """Slices a given sprite sheet for individual cards and returns a dictionary indexed by rank and suit"""

    if sprite_sheet is None or card_width <= 0 or card_height <= 0 or SCALE_FACTOR <= 0:
        raise ValueError("Invalid sprite sheet")

    # hard coded for this specific asset sheet
    CARDS_PER_ROW = 13

    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']

    # Using a dictionary to store card images and index them by rank and suit
    card_images = {}

    x = 0
    y = 0

    # Int conversion here to avoid conversion errors
    scaled_width = int(card_width * SCALE_FACTOR)
    scaled_height = int(card_height * SCALE_FACTOR)

    # nested loop isnt very efficient :(
    for suit in suits:
         for rank in ranks:
            # Calculate the position of the card in the sprite sheet
            card_rect = pygame.Rect(x, y, card_width, card_height)

            card_image = sprite_sheet.subsurface(card_rect)

            scaled_card_image = pygame.transform.scale(card_image, (scaled_width, scaled_height))
            card_images[(rank, suit)] = scaled_card_image

            # Move across to the next card
            x += card_width

            # if we've reached the edge of the row, move to the next column
            if x >= CARDS_PER_ROW * card_width:
                x = 0  # Reset x to the left
                y += card_height  # Move to the next col

    # get card back and index in dictionary
    card_rect = pygame.Rect(128, 480, card_width, card_height)
    card_images['back', 'yellow'] = pygame.transform.scale(sprite_sheet.subsurface(card_rect), (scaled_width, scaled_height))

    # return the images and their scaled dimensions as they can change based on given scalar
    return card_images, scaled_width, scaled_height


def draw_buttons(screen, hit_button, stand_button, font):
    """Draw the Hit and Stand buttons."""

    mouse_pos = pygame.mouse.get_pos()

    # hit button
    hit_color = COLOURS["RED"] if hit_button.collidepoint(mouse_pos) else COLOURS["BLUE"]
    pygame.draw.rect(screen, hit_color, hit_button)

    # hit button label
    hit_text = font.render("Hit", True, COLOURS["WHITE"])
    screen.blit(hit_text, (hit_button.x + 30, hit_button.y + 15))

    # stand button
    stand_color = COLOURS["RED"] if stand_button.collidepoint(mouse_pos) else COLOURS["BLUE"]
    pygame.draw.rect(screen, stand_color, stand_button)

    # stand button label
    stand_text = font.render("Stand", True, COLOURS["WHITE"])
    screen.blit(stand_text, (stand_button.x + 20, stand_button.y + 15))

def render_cards(screen, hand, x, y, label, player, card_images, font):
    """Render a hand of cards to the screen."""

    x_temp = x
    
    for card in hand:
        card_image = card_images[(card.rank, card.suit)]
        screen.blit(card_image, (x, y))
        x += CARD_WIDTH + 30

        if x + CARD_WIDTH > SCREEN_WIDTH:
            x = x_temp
            y += CARD_HEIGHT + 30

    score = player.calculate_score()

    score_text = font.render(f"{label}: {score}", True, COLOURS.get("WHITE"))
    screen.blit(score_text, (x_temp, y))

def render_dealer_cards(screen, dealer, card_images, font, game_over):
    """Render the dealer's hand to the screen."""

    x, y = SCREEN_WIDTH / 3, 100
    for i, card in enumerate(dealer.hand):
        if i == 0 and not game_over: 
            card_image = card_images['back', 'yellow']
        else:
            card_image = card_images[(card.rank, card.suit)]
        screen.blit(card_image, (x, y))
        x += CARD_WIDTH + 30

    # Display the dealer's score (excluding the face-down card during the game)
    dealer_score = dealer.calculate_score_excluding_first_card() if not game_over else dealer.calculate_score()
    score_text = font.render(f"Dealer: {dealer_score}", True, COLOURS.get("WHITE"))
    screen.blit(score_text, (x, y))

def display_game_over(screen, dealer, players, winner, font):
    """Display the final scores and the winner."""
    screen.fill(COLOURS.get("GREEN"))

    # Final scores
    dealer_score = dealer.calculate_score()
    dealer_text = font.render(f"Dealer: {dealer_score}", True, COLOURS.get("WHITE"))
    screen.blit(dealer_text, (100, 100))

    for i, player in enumerate(players):
        player.calculate_score()
        player_text = font.render(f"Player {i + 1}: {player.score}", True, COLOURS.get("WHITE"))
        screen.blit(player_text, (100, 150 + i * 50))

    winner_text = font.render(f"Winner: {winner}", True, COLOURS.get("WHITE"))
    screen.blit(winner_text, (100, 400))

    # Restart option
    restart_text = font.render("Press R to restart or Q to quit", True, COLOURS.get("WHITE"))
    screen.blit(restart_text, (100, 450))

    pygame.display.flip()