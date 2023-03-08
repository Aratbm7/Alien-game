class Setting:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Ship speed
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        # fleet_direction of 1 represent right, -1 represent left.
        self.ship_limit = 3
        self.fleet_drop_speed = 10.0
        # How quickly the game speeds up.
        self.speedup_scale = 1.5
        self.initialize_dynamic_setting()
        self.alien_points = 50
        # How quickly the alien point values increase.
        self.score_scale = 1.5

    def initialize_dynamic_setting(self):
        """Initialize settings that change throughout the game. """
        self.ship_speed = 0.7
        self.bullet_speed = 2.0
        self.alien_speed = 0.5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)

    def increase_speed_easy(self):
        self.ship_speed = 0.7
        self.bullet_speed = 2.0
        self.alien_speed = 0.5

    def increase_speed_normal(self):
        self.ship_speed = 1.0
        self.bullet_speed = 2.5
        self.alien_speed = 0.8

    def increase_speed_hard(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.5
        self.alien_speed = 1.3
