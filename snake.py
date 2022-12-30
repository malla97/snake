"""
This is a classic snake game I made with the intention of learning
pygame and also brush up my rusty python skills.

Rules: You lose if you run into a wall or to snake itself
and win if you get score to 300. Your size increases every time
by 1 when collecting an apple.
The snake moves constantly but the player can decide which way
by pressing the arrow keys to determine the direction.

Malla nyrhinen
 
"""

import pygame, random, sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption('🐍SNAKE🐍')

# Colours
DARKBLUE = (8, 30, 51)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
LIGHTGREY = (232, 232, 232)
WHITE = (255, 255, 255)
SNAKEGREEN = (0, 181, 26)
APPLERED = (230, 10, 10)

# Setup
FPS = pygame.time.Clock()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 520
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
SPEED = 12
STARTX = 300
STARTY = 260
XCENTER = WINDOW_WIDTH // 2

# Main
def main():
    loop = True
    while loop:
        startWindow()

# Window at the start
def startWindow():
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        WINDOW.fill(BLACK)
        
        addText('READY TO PLAY?', GREEN, 28, XCENTER, 100)
        addText('You can quit the game by pressing ESC or', GREEN, 26, XCENTER, 150)
        addText('pause the game by pressing SPACE.', GREEN, 26, XCENTER, 185)
        addText('Change snakes directions with arrow keys.', GREEN, 26, XCENTER, 240)

        button('START', WHITE, 100, 420, 100, 50, GREEN, BRIGHT_GREEN, runGame)
        button('QUIT', BLACK, 400, 420, 100, 50, WHITE, LIGHTGREY, quitGame)

        pygame.display.update()

# Window when player loses
def gameOverWindow(txt, score):
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitGame()
        
        WINDOW.fill(BLACK)

        scoreTxt = "Your score was: {}".format(score)

        if score == 300:
            addText('YOU WON!', GREEN, 34, XCENTER, 100)
            addText(scoreTxt, GREEN, 28, XCENTER, 200)
        else:
            addText('GAME OVER', GREEN, 32, XCENTER, 100)
            addText(txt, GREEN, 28, XCENTER, 150)
            addText(scoreTxt, GREEN, 28, XCENTER, 200)

        button('PLAY AGAIN', WHITE, 100, 420, 150, 50, GREEN, BRIGHT_GREEN, runGame)
        button('QUIT', BLACK, 400, 420, 100, 50, WHITE, LIGHTGREY, quitGame)

        pygame.display.update()

# Function to pause the game
def pauseGame():
    paused = True

    addText('PAUSED', WHITE, 32, XCENTER, 100)
    addText('Press ESC or SPACE to continue', WHITE, 32, XCENTER, 150)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                if event.key == pygame.K_SPACE:
                    paused = False
        pygame.display.update()
        FPS.tick(SPEED)

# Function for adding wanted buttons to given coordinates
def button(text, textColour, x, y, width, height, colour, activeColour, function = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(WINDOW, activeColour, (x, y, width, height))
        if click[0] == 1 and function != None:
            function()
    else:
        pygame.draw.rect(WINDOW, colour, (x, y, width, height))

    addText(text, textColour, 20, x + (width / 2), y + (height / 2))
    
# Function for running the game
def runGame():
    # At the start snake moves downwards
    direction = DOWN
    score = 0
    # Snake is at the start 3 blocks long, keeping track of the coordinates
    # in a list
    snakeBodyCoordinates = [{'x': STARTX, 'y': STARTY}, #head
                            {'x': STARTX, 'y': STARTY - 10},
                            {'x': STARTX, 'y': STARTY - 20}]
    length = 3
    snakePos = [STARTX, STARTY]
    
    # Apple at a random spot
    appleCoordinates = getRandomApple(snakeBodyCoordinates)
   
    while True:
        # Get the key press
        for event in pygame.event.get():
            if event.type == QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                # Snake is unable to move to the opposite direction it is
                # currently moving because it would break its neck
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                elif event.key == pygame.K_ESCAPE:
                    quitGame()
                elif event.key == pygame.K_SPACE:
                    pauseGame()

        if direction == UP:
            snakePos[1] -= 10
        if direction == DOWN:
            snakePos[1] += 10
        if direction == LEFT:
            snakePos[0] -= 10
        if direction == RIGHT:
            snakePos[0] += 10

        # If snakes head collides with apple, grow snakesize by 1 and spawn
        # a new apple, increase score and length
        # Adding a snakecoordinate to the front to the direction of moving
        # and taking the last snakecoordinate out, creates the sense of moving
        snakeBodyCoordinates.insert(0, {'x': snakePos[0], 'y': snakePos[1]})
        if (snakeBodyCoordinates[0]['x'] == appleCoordinates['x']
            and snakeBodyCoordinates[0]['y'] == appleCoordinates['y']):
            score += 1
            length += 1
            appleCoordinates = getRandomApple(snakeBodyCoordinates)
        else:
            snakeBodyCoordinates.pop()

        WINDOW.fill(DARKBLUE)

        # Adding some padding to show score and snakes length
        pygame.draw.rect(WINDOW, BLACK, (0, 0, 600, 30))
        
        scoreTxt = "Score: {}".format(score)
        addText(scoreTxt, WHITE, 26, WINDOW_WIDTH // 4, 15)

        lenTxt = "Snake length: {}".format(length)
        addText(lenTxt, WHITE, 26, (WINDOW_WIDTH // 4) * 3, 15)

        drawSnake(snakeBodyCoordinates)
        drawApple(appleCoordinates)

        # If snake hits a wall end game
        if(snakeBodyCoordinates[0]['x'] == -10 or
            snakeBodyCoordinates[0]['x'] == WINDOW_WIDTH or
            snakeBodyCoordinates[0]['y'] == 20 or 
            snakeBodyCoordinates[0]['y'] == WINDOW_HEIGHT):
            gameOverWindow('YOU HIT A WALL!', score)

        # If snake hits itself end game
        for coords in snakeBodyCoordinates[1:]:
            if(snakeBodyCoordinates[0]['x'] == coords['x']
                and snakeBodyCoordinates[0]['y'] == coords['y']):
                gameOverWindow('YOU TRIED TO EAT YOURSELF!', score)

        # If snake gets 300 apples, player wins and game ends
        if score == 300:
            gameOverWindow('', score)

        pygame.display.update()
        FPS.tick(SPEED)

# Function to add text to given coordinates
def addText(txt, colour, size, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
        
    text = font.render(txt, True, colour)
    textRect = text.get_rect()
    textRect.center = (x, y)
    WINDOW.blit(text, textRect)


# Random coordinates for apple, must be divisible by 10 so that it
# lines up with snakes coordinates and not withing snakes coordinates
def getRandomApple(snakeBodyCoordinates):
    x = random.randint(10, WINDOW_WIDTH - 10)
    y = random.randint(30, WINDOW_HEIGHT - 10)
    # Checking that the random coordinates are not where snakes body coordinates are
    for coord in snakeBodyCoordinates:
        if coord['x'] == x and coord['y'] == y:
            return getRandomApple(snakeBodyCoordinates)
    if x % 10 == 0 and y % 10 == 0:
        return {'x': x, 'y': y}
    else:
        return getRandomApple(snakeBodyCoordinates)


# Draws snake to the window
def drawSnake(snakeBodyCoordinates):
    for coord in snakeBodyCoordinates:
        x = coord['x']
        y = coord['y']
        cellRect = pygame.Rect(x, y, 10, 10)
        pygame.draw.rect(WINDOW, SNAKEGREEN, cellRect)

# Draws the apple to the window
def drawApple(appleCoordinates):
    x = appleCoordinates['x']
    y = appleCoordinates['y']
    cellRect = pygame.Rect(x, y, 10, 10)
    pygame.draw.rect(WINDOW, APPLERED, cellRect)

# Funxtion to quit game and exit
def quitGame():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
