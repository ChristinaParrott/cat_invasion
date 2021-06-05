import pygame
from pygame.sprite import Sprite

class Cat(Sprite):
    #A class to represent a single cat in the invading force

    def __init__(self, ci_game):
        #Initialize the cat and set its starting position
        super().__init__()
        self.screen = ci_game.screen
        self.settings = ci_game.settings

        #Load the cat and set its rect attribute
        self.image = pygame.image.load('images/cat.bmp')
        self.rect = self.image.get_rect()

        #Start each new cat at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the cat's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        #Move cat to the right or left
        self.x += self.settings.cat_speed * self.settings.swarm_direction
        self.rect.x = self.x

    def check_edges(self):
        #Returns true if cat is at the edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True