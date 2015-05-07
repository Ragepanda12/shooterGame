import pygame, os, random
from pygame.locals import *
from random import randint
 
WIDTH, HEIGHT = 800, 800
RELOAD_SPEED = 500
MULTISHOT_TIMER = 50
DEFAULT_MISSILES = 5
SHIELD_TIME = 1500
SHIELD_RELOAD_TIME = 10000
POWERUP_DELAY = 10000
MISSILE_DAMAGE = 20
DEFAULT_POWERUP_STATE = True
BLACK = (0, 0, 0)
YELLOW = pygame.Color("yellow")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
 
keys = {}
 
class PlayerOne():
    def __init__(self):
        self.speed = 6
        self.health = 100  
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "ship2mini.png")
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 100
        self.rect.centerx = WIDTH/2
        self.reloaded = True
        self.reloadTime = RELOAD_SPEED
        self.numBullets = DEFAULT_MISSILES 
        self.multishotTimer = MULTISHOT_TIMER
        self.multishotCheck = False
        self.hasUnlimShotPower = DEFAULT_POWERUP_STATE
        self.unlimShotMode = False
        self.powerUpTimer = 0
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
        if keys[K_UP] and self.reloaded == True and self.multishotCheck == False:
            if self.unlimShotMode == False:
                self.numBullets -= 1
                self.multishotCheck = True
                objects.append(BulletOne(self.rect.centerx, self.rect.top))
                if self.numBullets == 0:
                    self.reloaded = False
            else:
                objects.append(BulletOne(self.rect.centerx, self.rect.top))               
        if keys[K_LSHIFT] and self.hasUnlimShotPower == True:
            self.unlimShotMode = True
            self.powerUpTimer = pygame.time.get_ticks()
        if self.unlimShotMode == True:
            if pygame.time.get_ticks() - self.powerUpTimer >= 5000:
                self.unlimShotMode = False
class PlayerTwo():
    def __init__(self):
        self.speed = 6
        self.health = 100  
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "ship2Flipmini.png")
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
        if self.health <= 0:
            Playertwo = None
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
            Playertwo.health -= MISSILE_DAMAGE
            if self in objects:
                objects.remove(self)
            if Playertwo.health < 0 and Playertwo in players:
                players.remove(Playertwo)

                
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
            Playerone.health -= MISSILE_DAMAGE
            if self in objects:
                objects.remove(self)
            if(Playerone.health < 0 and Playerone in players):
                players.remove(Playerone)
                playerone = None
    def draw(self):
        screen.blit(self.image, self.rect)
        
"""class powerUp():
    def __init__(self):
        objects.append(self)
        self.speed = 6
        basepath = os.path.dirname(__file__)
        imagepath = os.path.join(basepath, "ship5mini.png")
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        self.rect.centery = pygame.Surface(screen.get_size()).get_rect().centery
        self.moveLeft = False;
    def think(self):
        if(self.moveLeft):
            if self.rect.left == 0:
                self.moveLeft = False
            self.rect.left -= self.speed
        else:
            self.rect.right += self.speed
            if self.rect.right == WIDTH:
                self.moveLeft = True
        if self.rect.colliderect(BulletOne.rect):
            Playerone.unlimShotMode = True
            objects.remove(self)
        elif self.rect.colliderect(BulletTwo.rect):
            Playertwo.unlimShotMode = True
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
 """
Playerone = PlayerOne()
Playertwo = PlayerTwo()
#enemies = []
objects = []
players = [Playerone, Playertwo]
#for x in range(3):
#    enemies.append(Enemy()) 
pygame.font.init()
myfont = pygame.font.SysFont("monospace", 15, bold=False, italic=False)
startText = myfont.render("Game Start!", 1, (255,255,0))
textpos = startText.get_rect()
textpos.centerx = pygame.Surface(screen.get_size()).get_rect().centerx
textpos.centery = pygame.Surface(screen.get_size()).get_rect().centery
screen.blit(startText, textpos)
pygame.display.update()
pygame.time.delay(2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()
    screen.fill((0,0,0))
    """if(pygame.time.get_ticks() % 1000 == 0):
        rngesus = randint(0, 9)
        if(rngesus < 10):
            powah = powerUp()"""
    #Playerone.think()
    #Playertwo.think()
    #for enemy in enemies:
    #    enemy.think()
     
    screen.fill(BLACK)
     
    for object in objects:                                              # new
        object.think()                                                  # new
        object.draw()                                                   # newme
    for object in players:
        if(object != None):
            object.think()
            object.draw()
    #Playerone.draw()
    #Playertwo.draw()
    #for enemy in enemies:
    #    enemy.draw()
    pygame.display.update()
