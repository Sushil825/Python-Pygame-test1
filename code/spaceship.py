import pygame
from setting import spaceship_speed



class Spaceship(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('../src/img/spaceship.png')
        self.image=pygame.transform.scale(self.image,(40,40))
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.speed=spaceship_speed
    def update(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x-=self.speed
        if key[pygame.K_RIGHT]:
            self.rect.x+=self.speed     

        
