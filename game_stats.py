class GameStats:
    #Track statistics for cat invasion

    def __init__(self, ci_game):
        #initialize statistics
        self.settings = ci_game.settings
        self.reset_stats()

        #Start in an inactive state
        self.game_active = False

        #High score will never be reset
        self.high_score = 0

    def reset_stats(self):
        #initialize statistics that can change during the game
        self.dogs_left = self.settings.dog_limit
        self.score = 0
        self.level = 1