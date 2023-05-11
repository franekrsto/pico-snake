# Import the necessary modules
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
import utime
import random
from machine import Pin

# Screen width and height
WIDTH = 240
HEIGHT = 135

# Initialize the display
display = PicoGraphics(display = DISPLAY_PICO_DISPLAY, pen_type = PEN_RGB332, rotate = 0)

# Set up the buttons
button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

# Setting up colours
WHITE  = display.create_pen(255, 255, 255)
BLACK  = display.create_pen(0, 0, 0)
RED    = display.create_pen(255, 0, 0)
YELLOW = display.create_pen(255, 255, 0)

# Define directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

directions = [UP, RIGHT, DOWN, LEFT]

# Initial game state
snake = [(200, 60), (210, 60), (220, 60)]
direction = LEFT
food = (random.randint(0, WIDTH//10-1)*10, random.randint(0, HEIGHT//10-1)*10)

# Define game over function
def game_over():
    display.set_pen(RED) # Set color to red
    text = "GAME OVER"
    text_width = 72
    text_height = 8
    x = (WIDTH - text_width) // 2
    y = (HEIGHT - text_height) // 2
    display.text(text, x, y)
    display.update()
    utime.sleep(3) # Delay before the next game starts

# Main game loop
while True:
    # Update direction based on button presses
    if not button_y.value():
        # Rotate direction to the right
        direction = directions[(directions.index(direction) + 1) % len(directions)]
        utime.sleep(0.2) # Adding a delay to avoid multiple rotations on a single button press
    elif not button_b.value():
        # Rotate direction to the left
        direction = directions[(directions.index(direction) - 1) % len(directions)]
        utime.sleep(0.2) # Adding a delay to avoid multiple rotations on a single button press

    # Move the snake
    new_head = (snake[0][0] + direction[0]*10, snake[0][1] + direction[1]*10)
    snake.insert(0, new_head)
    if new_head == food:
        # Eat the food: place a new food item and don't remove the last snake segment
        food = (random.randint(0, WIDTH//10-1)*10, random.randint(0, HEIGHT//10-1)*10)
    else:
        # Don't eat the food: remove the last snake segment
        snake.pop()

    # Check for collisions
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake[1:]):
        # Game over: display the game over text and reset the game state
        game_over()
        snake = [(200, 60), (210, 60), (220, 60)]
        direction = LEFT
        food = (random.randint(0, WIDTH//10-1)*10, random.randint(0, HEIGHT//10-1)*10)

    # Draw everything
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    for segment in snake:
        display.rectangle(segment[0], segment[1], 10, 10)
    display.set_pen(RED)
    display.rectangle(food[0], food[1], 10, 10)
    display.update()

    # Pause before the next frame
    utime.sleep(0.1)
