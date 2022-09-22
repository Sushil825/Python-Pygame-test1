import imp
from pygame import mixer
import random
import pygame
from pygame.locals import *
import setting
import sys
import levels.level1

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()


#Loading sounds

explosion_s=pygame.mixer.Sound("../src/sounds/small.wav")
explosion_s.set_volume(0.25)

explosion_b=pygame.mixer.Sound("../src/sounds/big.wav")
explosion_b.set_volume(0.25)

laser=pygame.mixer.Sound("../src/sounds/laser.wav")
laser.set_volume(0.25)

laserb=pygame.mixer.Sound("../src/sounds/laserbig.wav")
laserb.set_volume(0.25)


clock=pygame.time.Clock()
alien_grp=pygame.sprite.Group()
player_grp=pygame.sprite.Group()
bullet_grp=pygame.sprite.Group()
alien_bullet_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
thunderbolt_group=pygame.sprite.Group()
cooldown=setting.bulletcd

screen=pygame.display.set_mode((setting.WIDTH,setting.HEIGHT))

#vars

last_alien_shot=pygame.time.get_ticks()
alien_shoot_cd=1000
red=(255,0,0)
green=(0,255,0)

#Loading images
bg=pygame.image.load("../src/img/bg.jpg")
bg=pygame.transform.scale(bg,(setting.WIDTH,setting.HEIGHT))

class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/bullet.png')
        self.image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        
    def update(self):
        self.rect.y-=setting.bullet_speed
        if self.rect.bottom<0:
            self.kill()

        if pygame.sprite.spritecollide(self,alien_grp,True):
            self.kill()
            explosion=Explosion(self.rect.centerx,self.rect.centery,2)
            explosion_group.add(explosion)
            explosion_s.play()


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/bullet1.png')
        self.image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        
    def update(self):
        self.rect.y+=setting.alien_bullet_speed
        if self.rect.bottom>setting.HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self,player_grp,False,pygame.sprite.collide_mask):
            self.kill()
            player.health_remaining-=10
            if player.health_remaining>0:
                explosion=Explosion(self.rect.centerx,self.rect.centery,1)
                explosion_group.add(explosion)
                explosion_s.play()
                

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for num in range(0,9):
            img=pygame.image.load(f'../src/img/Flash/flash0{num}.png')
            if size==1:
                img=pygame.transform.scale(img,(20,20))
            if size==2:
                img=pygame.transform.scale(img,(40,40))
            if size==3:
                img=pygame.transform.scale(img,(160,160))
            self.images.append(img)

        self.index=0
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.counter=0


    def update(self):
        explosion_speed=3
        self.counter+=1

        if self.counter>=explosion_speed and self.index<len(self.images)-1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]

        if self.index>=len(self.images)-1 and self.counter >=explosion_speed:
            self.kill()

class Thunderbolt(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/thunderbolt.png')
        self.image=pygame.transform.scale(self.image,(30,30))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]

    def update(self):
        self.rect.y+=1
        

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/spaceship.png')
        self.image=pygame.transform.scale(self.image,(setting.shipsizex,setting.shipsizey))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.time=pygame.time.get_ticks()
        self.health_start=health
        self.health_remaining=health
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
            laser.play()

        self.mask=pygame.mask.from_surface(self.image)
        pygame.draw.rect(screen,red,(self.rect.x,(self.rect.bottom+10),self.rect.width,15))
        if self.health_remaining>0:
            pygame.draw.rect(screen,green,(self.rect.x,(self.rect.bottom+10),int(self.rect.width*self.health_remaining/self.health_start),15))

        elif self.health_remaining<=0:
            explosion=Explosion(self.rect.centerx,self.rect.centery,3)
            explosion_group.add(explosion)
            explosion_b.play()
            self.kill()

class Aliens(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/monster.png')
        self.image=pygame.transform.scale(self.image,(setting.shipsizex,setting.shipsizey))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.move_count=0
        self.move_direction=1

    def update(self):
        self.rect.x+=self.move_direction
        self.move_count+=1

        if abs(self.move_count)>75:
            self.move_direction*=-1
            self.move_count*=self.move_direction

#Functs
def draw_bg():
    screen.blit(bg,(0,0))

def create_alien():

    for indexi,i in enumerate(levels.level1.level):
        for indexj,j in enumerate(i):
            if j==1:
                alien=Aliens(indexj*100+50,indexi*70+70)
                alien_grp.add(alien)


create_alien()

player=Player((setting.WIDTH//2),(setting.HEIGHT-100),100)
player_grp.add(player)

while setting.run:
    clock.tick(setting.fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Drawing
    draw_bg()
    time_now=pygame.time.get_ticks()
    if time_now-last_alien_shot>alien_shoot_cd and len(alien_bullet_group)<5 and len(alien_grp)>0:
        attacking_alien=random.choice(alien_grp.sprites())
        alien_bullet=AlienBullet(attacking_alien.rect.centerx,attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot=time_now

    player_grp.draw(screen)
    bullet_grp.draw(screen)
    alien_grp.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)
    thunderbolt_group.draw(screen)


    #Updaing grps
    player_grp.update()
    bullet_grp.update()
    alien_grp.update()
    alien_bullet_group.update()
    explosion_group.update()
    thunderbolt_group.update()
    pygame.display.update()

    thun=random_count=random.randrange(1,1000)
    if thun==69:
        thunderbolt=Thunderbolt(random.randrange(0,setting.WIDTH),0)
        thunderbolt_group.add(thunderbolt)