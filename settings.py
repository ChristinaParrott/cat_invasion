class Settings:
    #Class that stores all settings for Cat Invasion
    def __init__(self):
        #Initialize the game's settings

        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (78, 203, 217)

        #Dog settings
        self.dog_limit = 3

        #Bone settings
        self.bones_allowed = 3
        self.bone_speed = 3.0

        #Cat settings
        self.swarm_drop_speed = 10

        #How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quickly the point values increase
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        #Initialize settings that will change throughout the game
        self.dog_speed = 1.5
        self.cat_speed = 1.5
        #Swarm direction of 1 is right; -1 is left
        self.swarm_direction = 1

        # Scoring
        self.cat_points = 50

    def increase_speed(self):
        #Increase speed settings
        self.cat_speed *= self.speedup_scale
        self.dog_speed *= self.speedup_scale

        #Increase point values
        self.cat_points = int(self.cat_points * self.score_scale)