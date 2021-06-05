import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from greyhound import Greyhound
from bone import Bone
from cat import Cat

class CatInvasion:
    #Class to manage game assets and behavior

    def __init__(self):
        #Initialize game and create resources
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Cat Invasion")

        #Set the background color
        self.bg_color =(self.settings.bg_color)

        #Create an instance to store game statistics and create scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.dog = Greyhound(self)
        self.bones = pygame.sprite.Group()
        self.cats = pygame.sprite.Group()

        self._create_swarm()

        #Create the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        #Start main loop for the game
        while True:
            self._check_events()

            if self.stats.game_active:
                self.dog.update()
                self._update_bones()
                self._check_swarm_edges()
                self._update_cats()

            self._update_screen()

    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_btn(mouse_pos)

    def _create_swarm(self):
        #Create the swarm of cats
        #Make a cat and retrieve its width & height
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size

        #Find the number of cats in a row
        #Spacing between each cat is equal to one cat width
        available_space_x = self.settings.screen_width - (2 * cat_width)
        num_cats_x = available_space_x // (2 * cat_width)

        #Find the number of rows that will fit on the screen
        dog_height = self.dog.rect.height
        available_space_y = (self.settings.screen_height -
                             (2 * cat_height) - dog_height)
        num_rows = available_space_y // (2 * cat_height)

        #Create the swarm of cats
        for row_num in range(num_rows):
            for cat_num in range(num_cats_x):
                self._create_cat(cat_num, row_num)

    def _create_cat(self, cat_num, row_num):
        # Create a cat and place it in the row
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size
        cat.x = cat_width + 2 * cat_width * cat_num
        cat.rect.x = cat.x
        cat.rect.y = cat.rect.height + 1.25 * cat.rect.height * row_num
        self.cats.add(cat)

    def _check_swarm_edges(self):
        #Respond if cats have reached the right or left edge of the screen
        for cat in self.cats.sprites():
            if cat.check_edges():
                self._change_swarm_direction()
                break

    def _change_swarm_direction(self):
        #Drop entire swarm and change it's direction
        for cat in self.cats.sprites():
            cat.rect.y += self.settings.swarm_drop_speed
        self.settings.swarm_direction *= -1

    def _update_bones(self):
        self.bones.update()

        # Remove bones that have left the screen
        for bone in self.bones.copy():
            if bone.rect.bottom <= 0:
                self.bones.remove(bone)

        self._check_collisions()

    def _check_collisions(self):
        # Check for any bones that have hit cats
        # If collision, get rid of bone and cat
        collisions = pygame.sprite.groupcollide(self.bones, self.cats, True, True)

        if collisions:
            for cats in collisions.values():
                self.stats.score += self.settings.cat_points * len(cats)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.cats:
            #If no more cats, destroy existing bones and create a new swarm (level up!)
            self.bones.empty()
            self._create_swarm()
            self.settings.increase_speed()

            #Increase the level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_cats_bottom(self):
        #Check if any cats have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for cat in self.cats.sprites():
            if cat.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if a doggo was hit
                self._dog_hit()
                break

    def _dog_hit(self):
        #Respond to doggo being hit :(

        if self.stats.dogs_left > 0:
            #Decrement dogs_left
            self.stats.dogs_left -= 1
            self.sb.prep_dogs()

            #Get rid of remaining cats and bones
            self.cats.empty()
            self.bones.empty()

            #Create a new swarm and center the dog
            self._create_swarm()
            self.dog.center_dog()

            #Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_cats(self):
        #Update position of all cats in the swarm
        self.cats.update()

        #Look for cat-dog collisions
        if pygame.sprite.spritecollideany(self.dog, self.cats):
            self._dog_hit()

        #Look for cats hitting the bottom of the screen
        self._check_cats_bottom()

    def _update_screen(self):
        # Redraw screen
        self.screen.fill(self.bg_color)
        self.dog.blitme()
        for bone in self.bones.sprites():
            bone.blitme()
        self.cats.draw(self.screen)

        #Draw the score info
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make most recently drawn screen visible
        pygame.display.flip()

    def _fire_bone(self):
        #Create a new bone and add it to the bones group
        if len(self.bones) < self.settings.bones_allowed:
            new_bone = Bone(self)
            self.bones.add(new_bone)

    def _check_keydown_events(self, event):
        #Handles key press events
        if event.key == pygame.K_RIGHT:
            # Move dog to the right
            self.dog.moving_right = True
        if event.key == pygame.K_LEFT:
            # Move dog to the left
            self.dog.moving_left = True
        elif event.key == pygame.K_SPACE:
            #Fire a bone
            self._fire_bone()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        #Handles key release events
        if event.key == pygame.K_RIGHT:
            # Stop moving to the right
            self.dog.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Stop moving to the left
            self.dog.moving_left = False

    def _check_play_btn(self, mouse_pos):
        #Start a new game when player clicks play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset game settings
            self.settings.init_dynamic_settings()

            #Reset game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_dogs()

            #Hide cursor
            pygame.mouse.set_visible(False)

            #Get rid of remaining cats and bones
            self.cats.empty()
            self.bones.empty()

            #Create a new swarm and center the doggo
            self._create_swarm()
            self.dog.center_dog()

if __name__ == '__main__':
    #Make a game instance and run the game
    ci = CatInvasion()
    ci.run_game()
