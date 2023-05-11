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
    # TODO: Update direction based on button presses
    # If button_y is pressed and direction is not RIGHT, set direction to LEFT
    # If button_b is pressed and direction is not LEFT, set direction to RIGHT
    # Remember to add a delay after each button press to avoid multiple rotations on a single press
    # Hint 1: You can check if a button is pressed with the `value()` method.
    # Hint 2: You can change the direction by using the `index()` method to find the current direction in the directions list,
    # subtracting 1 from the index, and using the result as a new index for the directions list.

    # Move the snake
    new_head = (snake[0][0] + direction[0]*10, snake[0][1] + direction[1]*10)
    snake.insert(0, new_head)
    if new_head == food:
        # Eat the food: place a new food item and don't remove the last snake segment
        food = (random.randint(0, WIDTH//10-1)*10, random.randint(0, HEIGHT//10-1)*10)
    else:
        # Don't eat the food: remove the last snake segment
        snake.pop()

    # TODO: Check for collisions (You need to check if the new head of the snake has gone out of the screen bounds or collided with the snake itself.)
    # Hint 1: Remember that the coordinates for the screen range from 0 to WIDTH-1 for the x-axis and 0 to HEIGHT-1 for the y-axis.
    # Hint 2: Check if the new head of the snake is in the list of snake's body segments (excluding the head).
    
    # TODO: If a collision occurred, reset the game
    # Hint 3: If a collision occurred, call the `game_over` function, reset the snake to its initial position, reset the direction, and place a new food item.

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

