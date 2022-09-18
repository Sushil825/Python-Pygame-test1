from email.mime import image
import pygame
from pygame.locals import *
import setting
import sys

clock=pygame.time.Clock()
player_grp=pygame.sprite.Group()
bullet_grp=pygame.sprite.Group()
cooldown=setting.bulletcd

screen=pygame.display.set_mode((setting.WIDTH,setting.HEIGHT))

#Loading images
bg=pygame.image.load("../src/img/bg.jpg")
bg=pygame.transform.scale(bg,(setting.WIDTH,setting.HEIGHT))

class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/bullet.png')
        self.image=pygame.transform.scale(self.image,(10,10))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        
    def update(self):
        self.rect.y-=setting.bullet_speed


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/spaceship.png')
        self.image=pygame.transform.scale(self.image,(setting.shipsizex,setting.shipsizey))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.time=pygame.time.get_ticks()

    def update(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x-=setting.spaceship_speed
        if key[pygame.K_RIGHT]:
            self.rect.x+=setting.spaceship_speed
        if key[pygame.K_SPACE] and pygame.time.get_ticks()-self.time>cooldown:
            bullet=Bullets(self.rect.centerx,self.rect.top)
            bullet_grp.add(bullet)
            self.time=pygame.time.get_ticks()

#Functs
def draw_bg():
    screen.blit(bg,(0,0))

player=Player((setting.WIDTH//2),(setting.HEIGHT-100))
player_grp.add(player)

while setting.run:
    clock.tick(setting.fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Drawing
    draw_bg()
    player_grp.draw(screen)
    bullet_grp.draw(screen)


    #Updaing grps
    player_grp.update()
    bullet_grp.update()

    pygame.display.update()