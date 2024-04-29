import pygame
import random
import time


# Initialize pygame
pygame.init()

# Constants   [ To adjust the features of the games easily ]
screen_width = 700
screen_height = 700
card_size = 175
grid_size = 4
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
flip_delay = 0.5
button_width = 140
button_height = 40
timer = 100

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Puzzle Game")

# Local file paths for PNG images
png_image_files = [
    "hyd.png",
    "tirupati.png",
    "roorkee.png",
    "pkd.png",
    "kgp.png",
    "madras.png",
    "guwahati.png",
    "bombay.png"
]

# Load into pygame card back image from local file
card_back_file = "back.png"
card_back = pygame.image.load(card_back_file)

# Load card images from local files
card_images = []
for file in png_image_files:
    card_images.append(pygame.image.load(file))


# Duplicate card images to create pairs
card_images *= 2

# Shuffle the cards
random.shuffle(card_images)

# Create a list to store the state of each card (True: flipped up , False: flipped down)
card_state = [False]*(grid_size ** 2)

# Variables to track flipped cards, matched pairs, moves, and timer
flipped_cards = []
matched_pairs = 0
moves = 0
timer_start = time.time()

# Font for displaying text
font = pygame.font.Font("Tropical County.ttf", 20)

# Function to check if a point is within a rectangle


def point_in_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx < x < rx + rw and ry < y < ry + rh

# Function to draw restart game button


def draw_restart_button():
    # coordinates of restart button
    restart_button_rect = (screen_width - button_width - 20, 20, button_width, button_height)
    pygame.draw.rect(screen, white, restart_button_rect)
    # Specify text color (black)
    restart_text = font.render("Restart Game", True, (0, 0, 0))
    text_rect = restart_text.get_rect(center=
                                      (restart_button_rect[0] + button_width / 2, restart_button_rect[1] + button_height / 2))
    screen.blit(restart_text, text_rect)

# Function to draw timer


def draw_timer():
    elapsed_time = max(0, int(time.time() - timer_start))
    remaining_time = max(0, timer - elapsed_time)
    timer_text = font.render(f"Time: {remaining_time}s", True, black)
    screen.blit(timer_text, (screen_width - 150, 10))

# Function to display message on the window


def display_message(message):
    message_text = font.render(message, True, black)
    text_rect = message_text.get_rect(
        center=(screen_width // 2, screen_height // 2))
    screen.blit(message_text, text_rect)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            restart_button_rect = (
                screen_width - button_width - 20, 20, button_width, button_height)
            if point_in_rect((mouse_x, mouse_y), restart_button_rect):
                random.shuffle(card_images)
                card_state = [False] * (grid_size ** 2)
                flipped_cards = []
                matched_pairs = 0
                moves = 0
                timer_start = time.time()  # Restart the timer
            else:
                col = mouse_x // card_size
                row = mouse_y // card_size
                index = row * grid_size + col
                if not card_state[index] and len(flipped_cards) < 2:
                    card_state[index] = True
                    flipped_cards.append(index)
                    moves += 1

    screen.fill(white)

    # Draw grid of cards
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            pygame.draw.rect(screen, grey, (j * card_size,
                                             i * card_size, card_size, card_size))
            if card_state[index] or index in flipped_cards:
                card = card_images[index]
            else:
                card = card_back
            card = pygame.transform.scale(card, (card_size - 10, card_size - 10))
            screen.blit(card, (j * card_size + 5, i * card_size + 5))

    # Render moves counter
    moves_text = font.render(f"Moves: {moves}", True, black)
    screen.blit(moves_text, (10, 10))

    # Draw restart game button
    draw_restart_button()

    # Draw timer
    draw_timer()

    # Check for matched pairs
    if len(flipped_cards) == 2:
        time.sleep(flip_delay)
        if card_images[flipped_cards[0]] == card_images[flipped_cards[1]]:
            matched_pairs += 1
            flipped_cards = []
        else:
            card_state[flipped_cards[0]] = False
            card_state[flipped_cards[1]] = False
            flipped_cards = []

    # Check for game over
    if matched_pairs == grid_size ** 2 // 2:
        display_message("Congratulations! You found all the pairs!")
        pygame.display.flip()
        time.sleep(5)  # Display the message for 5 seconds
        running = False

    # Check for time limit reached
    elapsed_time = time.time() - timer_start
    if elapsed_time >= timer:
        display_message("Time's up! You lost the game.")
        pygame.display.flip()
        time.sleep(5)  # Display the message for 5 seconds
        running = False

    pygame.display.flip()

pygame.quit()
