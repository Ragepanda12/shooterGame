import pygame, os, random
from pygame.locals import *
 
WIDTH, HEIGHT = 800, 800
RELOAD_SPEED = 500
MULTISHOT_TIMER = 50
DEFAULT_MISSILES = 5
BLACK = (0, 0, 0)
YELLOW = pygame.Color("yellow")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
 
keys = {}
 
class PlayerOne():
    def __init__(self):
        self.speed = 6
        self.health = 100  
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "ship2.png")
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 100
        self.rect.centerx = WIDTH/2
        self.reloaded = True
        self.reloadTime = RELOAD_SPEED
        self.numBullets = DEFAULT_MISSILES 
        self.multishotTimer = MULTISHOT_TIMER
        self.multishotCheck = False
    def draw(self):
        if self.health > 0:
            screen.blit(self.image, self.rect)
     
    def think(self):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.speed
        elif keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.right += self.speed
        if self.reloaded == False:
            self.reloadTime -= 1
            if self.reloadTime == 0:
                self.reloaded = True
                self.reloadTime = RELOAD_SPEED
                self.numBullets = DEFAULT_MISSILES
        if self.multishotCheck == True:
            self.multishotTimer -= 1
            if self.multishotTimer == 0:
                self.multishotTimer = MULTISHOT_TIMER
                self.multishotCheck = False
        if keys[K_SPACE] and self.reloaded == True and self.multishotCheck == False:
            self.numBullets -= 1
            self.multishotCheck = True
            objects.append(BulletOne(self.rect.centerx, self.rect.top))    # new
            if self.numBullets == 0:
                self.reloaded = False
            
class PlayerTwo():
    def __init__(self):
        PlayerTwo.speed = 6
        PlayerTwo.health = 100  
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "ship2Flip.png")
        PlayerTwo.image = pygame.image.load(imagepath)
        PlayerTwo.rect = self.image.get_rect()
        self.rect.top = 100
        self.rect.centerx = WIDTH/2
        self.reloaded = True
        self.reloadTime = RELOAD_SPEED 
        self.numBullets = DEFAULT_MISSILES    
        self.multishotCheck = False
        self.multishotTimer = MULTISHOT_TIMER
    def draw(self):
        if self.health > 0:
            screen.blit(self.image, self.rect)
    
    def think(self):
        if keys[K_a] and self.rect.left > 0:
            self.rect.left -= self.speed
        elif keys[K_d] and self.rect.right < WIDTH:
            self.rect.right += self.speed
        if self.reloaded == False:
            self.reloadTime -= 1
            if self.reloadTime == 0:
                self.reloaded = True
                self.reloadTime = RELOAD_SPEED
                self.numBullets = DEFAULT_MISSILES
        if self.multishotCheck == True:
            self.multishotTimer -= 1
            if self.multishotTimer == 0:
                self.multishotTimer = MULTISHOT_TIMER
                self.multishotCheck = False
        if keys[K_w] and self.reloaded == True and self.multishotCheck == False:
            self.numBullets -= 1
            self.multishotCheck = True
            objects.append(BulletTwo(self.rect.centerx, self.rect.top))    # new
            if self.numBullets == 0:
                self.reloaded = False

class BulletOne():                                                         # new object
    def __init__(self, x, y):
        self.speed = 10
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "missile.png")
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        
    def think(self):
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            objects.remove(self)
        if self.rect.colliderect(Playertwo.rect):
            Playertwo.health -= 100
            if self in objects:
                objects.remove(self)
                
                
    def draw(self):
        screen.blit(self.image, self.rect)
                                            # new loop

                
class BulletTwo():                                                         # new object
    def __init__(self, x, y):
        self.speed = 10
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "missileFlip.png")
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        
    def think(self):
        self.rect.top += self.speed
        if self.rect.top < 0:
            objects.remove(self)
        if self.rect.colliderect(Playerone.rect):
            Playerone.health -= 100
            if self in objects:
                objects.remove(self)
             
    def draw(self):
        screen.blit(self.image, self.rect)
        
class Enemy():
    def __init__(self):
        enemies.append(self)
        self.speed = 0
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "ship5.png")
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.jumpToStart()
     
    def think(self):
        self.rect.top += self.speed
        if self.rect.top > HEIGHT:
            self.jumpToStart()
     
    def jumpToStart(self):
        self.rect.bottom = 0
        self.rect.centerx = (random.randint(0,WIDTH-100)) +50
        self.speed = random.randint(2, 5)
     
    def draw(self):
        screen.blit(self.image, self.rect)
 
Playerone = PlayerOne()
Playertwo = PlayerTwo()
#enemies = []
objects = []                                                            # new
#for x in range(3):
#    enemies.append(Enemy()) 
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15, bold=False, italic=False)
startText = myfont.render("Game Start!", 1, (255,255,0))
screen.blit(startText, (WIDTH/2, HEIGHT/2))
pygame.display.update()
pygame.time.delay(2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()
     
    Playerone.think()
    Playertwo.think()
    #for enemy in enemies:
    #    enemy.think()
     
    screen.fill(BLACK)
     
    for object in objects:                                              # new
        object.think()                                                  # new
        object.draw()                                                   # new
     
    Playerone.draw()
    Playertwo.draw()
    #for enemy in enemies:
    #    enemy.draw()
    pygame.display.update()
