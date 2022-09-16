
import pygame
from pygame.locals import *
from setting import *
import sys
from spaceship import Spaceship



#Loading images

bg=pygame.image.load('../src/img/bg.jpg')
bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))
#Groups

spaceship_group=pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock=pygame.time.Clock()
        pygame.display.set_caption('Space invaders')

        self.player=Spaceship(WIDTH//2,HEIGHT-100)
        spaceship_group.add(self.player)

    def run(self):
        while run:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_bg()
            #Drawing groups

            spaceship_group.draw(self.screen)
            bullet_group.draw(self.screen)



            #Updating groups

            spaceship_group.update()
            bullet_group.update()



            pygame.display.update()
            self.clock.tick(fps)


    def draw_bg(self):
        self.screen.blit(bg,(0,0))


if __name__=='__main__':
    game=Game()
    game.run()        