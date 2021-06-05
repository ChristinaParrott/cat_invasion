import pygame
from pygame.sprite import Sprite

class Bone(Sprite):
    #Class to manage the bone "bullets"
    def __init__(self, ci_game):
        #initialize the bone and set the starting position
        super().__init__()
        self.screen = ci_game.screen
        self.screen_rect = ci_game.screen.get_rect()
        self.settings = ci_game.settings

        #Load the bone and get its rect
        self.image = pygame.image.load('images/bone.bmp')
        self.rect = self.image.get_rect()

        #Start each new bone at the dog's current position
        self.rect.midtop = ci_game.dog.rect.midtop

        #Store a dec value for the bone's vertical position
        self.y = float(self.rect.y)



    def update(self):
        #Move the bone up the screen
        #Update it's decimal position
        self.y -= self.settings.bone_speed
        #Update the bone position
        self.rect.y = self.y



    def blitme(self):
        #Draw bone at it's current location
        self.screen.blit(self.image, self.rect)