import pygame
import random
import requests
from io import BytesIO

# Initialize pygame
pygame.init()

# Set display dimensions
width, height = 800, 600
block_size = 20

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set font for text
font_style = pygame.font.SysFont(None, 50)

# Function to display message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    return mesg

# Function to draw snake
def draw_snake(display, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(display, green, [x, y, block_size, block_size])

# Function to display score
def show_score(display, score):
    # Draw white UI box
    score_rect = pygame.Rect(5, 5, 150, 60)
    pygame.draw.rect(display, white, score_rect)

    # Draw outline for the UI box
    outline_rect = pygame.Rect(3, 3, 154, 64)  # Slightly smaller than the UI box
    pygame.draw.rect(display, black, outline_rect, 2)  # Outline in black

    score_text = font_style.render("Score: " + str(score), True, black)
    text_rect = score_text.get_rect(center=score_rect.center)  # Center the text within the UI box
    display.blit(score_text, text_rect)

# Function to display buttons
def draw_button(display, text, color, x, y, width, height):
    pygame.draw.rect(display, color, [x, y, width, height])
    text_surface = font_style.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width / 2, y + height / 2)
    display.blit(text_surface, text_rect)

# Function to check if button is clicked
def is_button_clicked(mouse_pos, button_rect):
    if button_rect.collidepoint(mouse_pos):
        return True
    return False

# Function to load an image from the internet
def load_image(url):
    response = requests.get(url)
    image = pygame.image.load(BytesIO(response.content))
    return image

# Main game loop
def gameLoop():
    # Set display surface
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ussimäng')

    # Set clock for managing frame rate
    clock = pygame.time.Clock()

    # Initial position of snake
    x1, y1 = width / 2, height / 2

    # Initial change in position
    x1_change, y1_change = 0, 0

    # Initial snake length
    snake_list = []
    length_of_snake = 1

    # Load apple image from the internet
    apple_url = "https://clipart-library.com/images/dT9Kjoe6c.png"  # Replace with actual URL
    apple_img = load_image(apple_url)
    apple_img = pygame.transform.scale(apple_img, (block_size, block_size))

    # Initial position of food
    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size

    # Initial score
    score = 0

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change, y1_change = -block_size, 0
                elif event.key == pygame.K_RIGHT:
                    x1_change, y1_change = block_size, 0
                elif event.key == pygame.K_UP:
                    x1_change, y1_change = 0, -block_size
                elif event.key == pygame.K_DOWN:
                    x1_change, y1_change = 0, block_size

        # Check if snake hits the wall
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change

        display.fill(blue)
        display.blit(apple_img, (foodx, foody))

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        draw_snake(display, snake_list)
        show_score(display, score)
        pygame.display.update()

        # Check if snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            length_of_snake += 1
            score += 1

        clock.tick(5)  # Adjust snake speed here

    display.fill(blue)
    death_msg = message("Sa kaotasid! Su score: " + str(score), red)
    display.blit(death_msg, [width / 6, height / 3])

    # Draw buttons
    continue_button = pygame.Rect(width // 4, height * 2 // 3, width // 4, 50)
    quit_button = pygame.Rect(width // 2 + width // 4, height * 2 // 3, width // 4, 50)
    draw_button(display, "Restart", green, continue_button.x, continue_button.y, continue_button.width, continue_button.height)
    draw_button(display, "Quit", red, quit_button.x, quit_button.y, quit_button.width, quit_button.height)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_button_clicked(mouse_pos, continue_button):
                    gameLoop()
                elif is_button_clicked(mouse_pos, quit_button):
                    pygame.quit()
                    quit()

gameLoop()

