import sys
from time import sleep
import pygame
import json
from settings import Setting
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_state import GameState
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initial the game, and create game recourse."""
        pygame.init()
        self.settings = Setting()
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Set the background color
        self.stats = GameState(self)
        # Crate an instance to score game statistics,
        # and creat a scoreboard.
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.ships = pygame.sprite.Group()
        self.bullet_flag = False
        self._creat_fleet()
        # Make the play button.
        self.play_button = Button(self, "play")
        self.set_buttons = pygame.sprite.Group()
        self._creat_set_of_buttons()
        self.play_button_flag = True
        self._quit_button()
        self.json_file_flag = False
        # pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=2**12)
        self.shooting_sound = pygame.mixer.Sound('sounds/gun-gunshot-01.wav')
        self.explosion_sound = pygame.mixer.Sound('sounds/mixkit-arcade-game-explosion-2759.wav')
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_alien()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_high_score(self.stats.high_score)
                self.json_file_flag = True
                sys.exit()

            # Make the most recently drawn screen visible
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_set_of_buttons(mouse_pos)
                self._check_play_button(mouse_pos)
                self._check_quit_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
           # self.settings.initialize_dynamic_setting()
           self.play_button_flag = False
           self.stats.reset_state()
           self.sb.prep_score()
           self.sb.prep_level()
           self.sb.prep_ships()


    def _check_quit_button(self, mouse_pos):
        clicke_button = self._quit_button().rect.collidepoint(mouse_pos)
        if clicke_button and not self.stats.game_active:
            self.save_high_score(self.stats.high_score)
            self.json_file_flag = True
            sys.exit()


    def _check_set_of_buttons(self, mouse_pos):
        """Choose option for game."""
        self.button_clicked_easy = self.set_buttons.sprites()[0].rect.collidepoint(mouse_pos)
        self.button_clicked_normal = self.set_buttons.sprites()[1].rect.collidepoint(mouse_pos)
        self.button_clicked_hard = self.set_buttons.sprites()[2].rect.collidepoint(mouse_pos)
        if self.button_clicked_easy and not self.stats.game_active:
            self.settings.increase_speed_easy()
            self._start_game()
        elif self.button_clicked_normal and not self.stats.game_active:
            self.settings.increase_speed_normal()
            self._start_game()
        elif self.button_clicked_hard and not self.stats.game_active:
            self.settings.increase_speed_hard()
            self._start_game()

    def _check_keydown_events(self, event):
        """Respond the keypress"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.save_high_score(self.stats.high_score)
            self.json_file_flag = True
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
                self.shooting_sound.play()
            # self.bullet_flag = True
        elif event.key == pygame.K_p:
            if not self.stats.game_active and self.play_button_flag:
                # self.settings.initialize_dynamic_setting()
                # self._start_game()
                self.play_button_flag = False

    def _check_keyup_events(self, event):
        """Respond the Key release"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        # elif event.key == pygame.K_SPACE:
        #     if self.stats.game_active:
        #         self._fire_bullet()
        #     # self.bullet_flag = False

    def _quit_button(self):
        buton_quit = Button(self, None)
        buton_quit.rect.x = self.play_button.rect.right + 50
        buton_quit.rect.y = self.play_button.rect.top
        buton_quit.prep_msg('Quit')
        return buton_quit

    def _start_game(self):
        self.stats.reset_state()
        self.stats.game_active = True
        # Get ride of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        # Creat a new fleet and center the ship.
        self._creat_fleet()
        self.ship.center_ship()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _update_bullet(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        # Get ride of bullets tha have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """ Respond to bullet-alien collisions."""
        # Remove any bullets and aliens have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # Check if aliens list is empty creat a new fleet and remove exiting bullets.
        if not self.aliens.sprites():
            self.bullets.empty()
            self._creat_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            # Explosions sound effects
            self.explosion_sound.play()

            # self.stats.score += self.settings.alien_points
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


    def _update_alien(self):
        """Check if the fleet is at an edge,
            then update the position of all aliens in th fleet.
        """
        self._check_fleet_edge()
        self.aliens.update()
        # print(len(self.aliens.sprites()))
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        self._check_aliens_bottom()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        # if len(self.bullets) < self.settings.bullet_allowed:
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _creat_fleet(self):
        """Creat the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)
        # Determine number of rows
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Creat the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._creat_alien(alien_number, row_number)



    def _creat_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edge(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's directions."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def ship_hit(self):
        """Respond to the ship begin hit by an alien."""

        if self.stats.ships_left > 1:
            # Decrement ship left
            self.stats.ships_left -= 1
            self.sb.prep_ships()


            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Creat a new fleet and center the ship.
            self._creat_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.play_button_flag = True
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached teh bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self.ship_hit()
                break

    def save_high_score(self, high_score):
        with open('score_high.json', 'w') as f:
            json.dump(high_score, f)



    def _creat_set_of_buttons(self):
        """Creat three buttons Easy , Normal and Hard"""
        button_width = 150
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height // 3
        buttons_position_screen = screen_width // 5
        list_button = ['easy', 'normal', 'hard']
        i = 0
        for btn_write in list_button:
            button = Button(self, None)
            button.rect.x = buttons_position_screen + (2 * button_width * i)
            i += 1
            button.rect.y = screen_height
            button.prep_msg(btn_write.title())
            self.set_buttons.add(button)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redrawn this screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        # Draw the play button if the game is inactive.
        # if not self.state.game_active:
        #     self.play_button.draw_button()
        if not self.stats.game_active and self.play_button_flag:
            self.play_button.draw_button()
            self._quit_button().draw_button()
        elif not self.stats.game_active and not self.play_button_flag:
            for btn in self.set_buttons.sprites():
                btn.draw_button()


        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
