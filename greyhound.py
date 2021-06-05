import pygame
from pygame.sprite import Sprite

class Greyhound(Sprite):
    #Class to manage the greyhound hero
    def __init__(self, ci_game):
        super().__init__()
        #initialize the dog and set the starting position
        self.screen = ci_game.screen
        self.screen_rect = ci_game.screen.get_rect()
        self.settings = ci_game.settings

        #Load the dog and get its rect
        self.image = pygame.image.load('images/greyhound.bmp')
        self.rect = self.image.get_rect()

        #Start each new greyhound at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a dec value for the ship's horz position
        self.x = float(self.rect.x)

        #Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #Update dog's position based on the movement flags
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.x += self.settings.dog_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.dog_speed

        #Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        #Draw greyhound at it's current location
        self.screen.blit(self.image, self.rect)

    def center_dog(self):
        #Center the dog at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x - float(self.rect.x)