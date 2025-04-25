from pygame import *
from random import *
import time as tm 
font.init()

#Main_Wind
windowW = 1280
windowH = 720

mainWindow = display.set_mode((windowW, windowH))
display.set_caption('Лаб')
mainWindow.fill((255, 255, 255))
bg = transform.scale(image.load('bg_shroom.png'), (windowW, windowH))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show(self):
        mainWindow.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def __init__(self,img, x, y, width, height, speed):
        GameSprite.__init__(self, img, x, y, width, height)
        self.speed = speed
        self.gravity = 15
        self.JumpCount = 4
        self.isJump = False
        self.isD = False
        self.MoveSpeed = 3
        self.standImage = transform.scale(image.load('alienBlue.png'), (width, height))
        self.jumpImage = transform.scale(image.load('alienBlue_jump.png'), (width, height))
        self.rightImage = transform.scale(image.load('alienBlue_walk2.png'), (width, height))
        self.leftImage = transform.flip(self.rightImage, True, False)
        self.leftJump = transform.flip(self.jumpImage, True, False)
        self.doorOpen = False
        self.haveaKey = False
        self.dead = False

    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x += self.MoveSpeed ** 2
            if self.isJump:
                self.image = self.jumpImage
            else:
                self.image = self.rightImage
        elif keys[K_a]:
            self.rect.x -= self.MoveSpeed ** 2
            if self.isJump:
                self.image = self.leftJump
            else:
                self.image = self.leftImage
            
        else:
            if self.isJump:
                pass
            else:
                self.image = self.standImage

    def jump(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            self.isJump = True
            self.image = self.jumpImage

        if self.isJump:
            self.rect.y -= self.JumpCount ** 2
            self.JumpCount -= 0.2
            if self.JumpCount <= 0:
                self.isJump = False
                self.JumpCount = 5
                


    def falling(self):
        if sprite.spritecollide(self, walls, False):
            platformTouched = sprite.spritecollide(self, walls, False)
            for platform in platformTouched:
                if platform.rect.top < self.rect.bottom:
                    self.gravity = 0
                    if self.image == self.jumpImage:
                        self.image = self.standImage
        else:
            if self.isJump == False:
                self.gravity = 10
class Enemy(GameSprite):
    def __init__(self,img, x, y, width, height, speed, PointLeft, PointRight):
        GameSprite.__init__(self, img, x, y, width, height)
        self.speed = speed
        self.direction = 'LEFT'
        self.PointLeft = PointLeft
        self.PointRight = PointRight
        self.LeftIm = transform.scale(image.load('bee.png'), (width, height))
        self.RightIm = transform.flip(self.LeftIm, True, False)

    def update(self):
        if self.rect.x <= self.PointLeft:
            self.direction = 'RIGHT'
            self.image = self.RightIm
        elif self.rect.x >= self.PointRight:
            self.direction = 'LEFT'
            self.image = self.LeftIm

        if self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed

player = Hero('alienBlue.png', 200, 200 , 66, 92, 15)
bee1 = Enemy('bee.png', 400, 250, 56, 48, 2, 400, 500)
bee2 = Enemy('bee.png', 600, 300, 56, 48, 2, 600, 700)
point = GameSprite('hud_keyGreen.png', 1200, 200, 44, 40)
door = GameSprite('door_closedMid.png', 1000, 400, 70, 70)

walls = sprite.Group()
platformX = 0
for i in range(5):
    wall = GameSprite('beamNarrow.png', platformX, 600, 70, 70)
    wall.add(walls)
    platformX += 70
platformX = 500
for i in range(5):
    wall = GameSprite('beamNarrow.png', platformX, 400, 70, 70)
    wall.add(walls)
    platformX += 70
platformX = 800
for i in range(1):
    wall = GameSprite('beamNarrow.png', platformX, 200, 70, 70)
    wall.add(walls)
    platformX += 70
platformX = 1000
for i in range(1):
    wall = GameSprite('beamNarrow.png', platformX, 110, 70, 70)
    wall.add(walls)
    platformX += 70
platformX = 1000
for i in range(10):
    wall = GameSprite('beamNarrow.png', platformX, 650, 70, 70)
    wall.add(walls)
    platformX += 70
    

fps = 60
clock = time.Clock()
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    mainWindow.blit(bg, (0, 0))
    point.show()
    point.update()
    door.show()
    door.update()
    bee1.show()
    bee1.update()
    bee2.show()
    bee2.update()
    if not player.dead:
        player.show()
        player.falling()
        player.jump()
        player.update()
        player.rect.y += player.gravity

    walls.draw(mainWindow)
    
    if sprite.collide_rect(player, point):
        player.haveaKey = True

    if player.haveaKey:
        if point.rect.y > 20:
            point.rect.y -= 15

    if sprite.collide_rect(player, door):
        if player.haveaKey:
            player.doorOpen = True
    
    if player.doorOpen:
        keys = key.get_pressed()

        door.image = image.load('door_openMid.png')
        if sprite.collide_rect(player, door):
            exitText = font.SysFont('Comic Sans', 33).render('Press ENTER to leave', True, (255, 255, 255))
            mainWindow.blit(exitText, (door.rect.left - 100, door.rect.top - 100))
        if keys[K_RETURN]:
            game = False

    if sprite.collide_rect(player, bee1) or sprite.collide_rect(player, bee2) :
        player.dead = True

    display.update()
    clock.tick(fps)