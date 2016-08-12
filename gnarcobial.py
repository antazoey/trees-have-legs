import pygame
import time
import random
#with notes as template

#initialization
x = pygame.init()

#RGB colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

#get surface
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))

#give game title
pygame.display.set_caption('Crukt VenNim')

#other constants
clock = pygame.time.Clock()
block_size = 10
FPS = 20
font = pygame.font.SysFont(None, 25)

def snake(snakeList,block_size):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def getSnakeHead(lead_x,lead_y):
    snakeHead = []
    snakeHead.append(lead_x)
    snakeHead.append(lead_y)
    return snakeHead

def getSnakeList(lead_x,lead_y):
    sList = []
    for i in range(10):
        sList.append(getSnakeHead(lead_x,lead_y-(i*10)))
    return sList
    
#send user text function
def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [display_width/2, display_height/2])

def gameLoop():
    
    #game variables
    gameExit = False
    gameOver = False

    #ensures start of snake is correct
    lead_x = display_width/2
    lead_y = display_height/2
    snakeList = getSnakeList(lead_x,lead_y)
    lead_x = snakeList[-1][0]
    lead_y = snakeList[-1][1]
    
    snakeLength = block_size
    lead_x_change = 0
    lead_y_change = -block_size
    randAppleX = random.randrange(20,display_width-block_size-10,10)
    randAppleY = random.randrange(20,display_height-block_size-10,10)

    #game loop
    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, prcess C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        #draw background + apple
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [randAppleX,randAppleY,block_size,block_size])
                    
        #movement event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        #edge of the map = Game Over               
        if lead_x >= display_width-10 or lead_x < 10 or lead_y >= display_height-10 or lead_y < 10:
            gameOver = True

        #add snake movement change based on event
        lead_x += lead_x_change
        lead_y += lead_y_change
            
        #snake growth
        snakeHead = getSnakeHead(lead_x,lead_y)
        
        #when snake hits itself, you lose
        for body in snakeList:
            if body[0] == snakeHead[0] and body[1] == snakeHead[1]:
                    gameOver = True
                    
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
        snake(snakeList, block_size)
        
        pygame.display.update()
        
        #when the apple is eaten, move apple
        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = random.randrange(20,display_width-block_size-10,10)
            randAppleY = random.randrange(20,display_height-block_size-10,10)
            snakeLength += 4

        clock.tick(FPS)

    #quits game
    pygame.quit()

    #quits python
    quit()

gameLoop()
