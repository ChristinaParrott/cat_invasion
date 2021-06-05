import pygame.font
from pygame.sprite import Group
from greyhound import Greyhound

class Scoreboard():
    #A class to report scoring information

    def __init__(self, ci_game):
        #Initialize score keeping attributes
        self.ci_game = ci_game
        self.screen = ci_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ci_game.settings
        self.stats = ci_game.stats

        #Font settings for scoring information
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        #Prepare initial dogs, score, and level images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_dogs()

    def prep_score(self):
        #Turn the score into a rendered image
        rounded_score = round(self.stats.score, -1)
        score_str = "Current Score: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #Display the store at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        #Turn the score into a rendered image
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #Display the store at the top right of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        #Turn the level into a rendered image
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_dogs(self):
        #Show how many doggos are left
        self.dogs = Group()
        for dog_num in range(self.stats.dogs_left):
            dog = Greyhound(self.ci_game)
            dog.rect.x = 10 + dog_num * dog.rect.width
            dog.rect.y = 10
            self.dogs.add(dog)

    def show_score(self):
        #Draw dogs, scores, and level to the screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.dogs.draw(self.screen)

    def check_high_score(self):
        #Check to see if there is a new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()