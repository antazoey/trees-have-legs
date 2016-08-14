import pygame
import time
import random

#DICTIONARY OF TERMS
#Phrens : each individual section of the snake
#Pharma : a creature that is like just 1 section of a snake from classic 'Snake'

#RGB colors
rgbDict = {'white':(255,255,255),'black':(0,0,0),'red':(255,0,0),'green':(0,155,0)}

class theGame:
    
    def __init__(self):

        init_game = pygame.init()

        #get surface
        self.display_width = 800
        self.display_height = 600
        self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        #give game title
        pygame.display.set_caption('Pharcobial')

        #other constants
        self.clock = pygame.time.Clock()
        self.block_size = 10
        self.FPS = 20
        self.font = pygame.font.SysFont(None, 25)

        self.gameExit = False
        self.gameOver = False

        self.clock = pygame.time.Clock()
        self.block_size = 10
        self.FPS = 20
        self.font = pygame.font.SysFont(None, 25)

    def message_to_screen(self,msg,color,x,y):
        screen_text = self.font.render(msg, True, color)
        self.gameDisplay.blit(screen_text, [x, y])

    def getBlock_size(self):
        return self.block_size

    def getDisplay_width(self):
        return self.display_width

    def getDisplay_height(self):
        return self.display_height

    def getGameDisplay(self):
        return self.gameDisplay

    def gameOverMethod(self):
        self.gameDisplay.fill(rgbDict['white'])
        self.message_to_screen("Game over, prcess C to play again or Q to quit", rgbDict['red'])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.gameExit = True
                    self.gameOver = False
                if event.key == pygame.K_c:
                    gameLoop()
        

class Pharma(pygame.sprite.Sprite):
    
    def __init__(self,block_size,gd,dw,dh):
        #necessary game variables
        self.block_size = block_size
        self.gameDisplay = gd
        self.display_width = dw
        self.display_height = dh
        
        #ensures start of snake is correct by
        #putting start in the middle of screen,
        self.lead_x = self.getDisplay_width()/2
        self.lead_y = self.getDisplay_height()/2
        self.head = [self.lead_x,self.lead_y]

        #movement variables
        self.delta_x = 0
        self.delta_y = 0

        super().__init__()

    def __repr__(self):
        return self.cordList

    def getDisplay_width(self):
        return self.display_width

    def getDisplay_height(self):
        return self.display_height

    def getDisplay_height(self):
        return self.display_height

    def drawPharma(self):
        pharmaRect = [self.lead_x,self.lead_y,self.block_size,self.block_size]
        pygame.draw.rect(self.gameDisplay, rgbDict['green'], pharmaRect)

    def gameShutDown(self,game,event):
        if event.type == pygame.QUIT:
            game.gameExit = True
        
    def movementHandling(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.delta_x = -self.block_size
                self.delta_y = 0
            elif event.key == pygame.K_RIGHT:
                self.delta_x = self.block_size
                self.delta_y = 0
            elif event.key == pygame.K_UP:
                self.delta_y = -self.block_size
                self.delta_x = 0
            elif event.key == pygame.K_DOWN:
                self.delta_y = self.block_size
                self.delta_x = 0

        #stops moving when KEYUP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.delta_x = 0
                self.delta_y = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.delta_x = 0
                self.delta_y = 0
                

    def move(self):
        self.lead_x += self.delta_x
        self.lead_y += self.delta_y

    def eat(self,edible,game):
        if self.lead_x == edible.randAppleX and self.lead_y == edible.randAppleY:
            edible.moveEdible()
            edible.edibleMessage(game)
            

class Edible:
    
    def __init__(self,bs,gd,dw,dh):
        self.block_size = bs
        self.gameDisplay = gd
        self.display_width = dw
        self.display_height = dh
        
        self.randAppleX = random.randrange(20,self.display_width-self.block_size-10,10)
        self.randAppleY = random.randrange(20,self.display_height-self.block_size-10,10)

    def drawEdible(self):
        ediRect = [self.randAppleX,self.randAppleY,self.block_size,self.block_size]
        pygame.draw.rect(self.gameDisplay, rgbDict['red'], ediRect)

    def moveEdible(self):
        self.randAppleX = random.randrange(20,self.display_width-self.block_size-10,10)
        self.randAppleY = random.randrange(20,self.display_height-self.block_size-10,10)
        self.drawEdible()

    def edibleMessage(self,game):
        
        game.message_to_screen("You've eaten an edible!",rgbDict['black'],game.display_width/10,game.display_height/10)
        
#*****game loop starts here*****

def gameLoop():
    pGame = theGame()
    block_size = pGame.getBlock_size()
    gameDisplay = pGame.getGameDisplay()
    game_width = pGame.getDisplay_width()
    game_height = pGame.getDisplay_height()
    player = Pharma(block_size,gameDisplay,game_width,game_height)
    edible = Edible(block_size,gameDisplay,game_width,game_height)
    #game loop variables
    while pGame.gameExit == False:
        while pGame.gameOver == True:           
            pGame.gameOverMethod()
        pGame.gameDisplay.fill(rgbDict['white'])
        edible.drawEdible()
        #print(player.cordList)
        for event in pygame.event.get():
        #player acts to shut down game
            #player.gameShutDown(pGame,event)
            player.movementHandling(event)
        player.move()
        player.drawPharma()
        player.eat(edible,pGame)
        pygame.display.update()
        pGame.clock.tick(pGame.FPS)
    pygame.quit()
    quit()
    
gameLoop()
