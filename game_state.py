import json


class GameState:
    """Track statistics for Alien invasion."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_state()
        self.game_active = False
        # high score should never reset.
        self.open_json_file()

    def open_json_file(self):
        self.high_score = 1
        with open('score_high.json') as f:
            high_score = json.load(f)
        self.high_score = int(high_score)

    def reset_state(self):
        """Initialize statistics that can change during game."""
        self.ships_left = self.settings.ship_limit
        self.score = 1
        self.level = 1

