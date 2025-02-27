import pygame
import gc
from Code.Variables.SettingVariables import *
from Code.Individuals.Gun import *


class GameVariables:
          def __init__(self, game):
                    self.game = game
                    self.initialize_game_flags()
                    self.initialize_game_settings()
                    self.initialize_game_state()
                    self.update_font_sizes()
                    self.update()

          def initialize_game_flags(self):
                    flags = {
                              'changing_settings': False, 'immidiate_quit': False, 'in_menu': True, 'restart': False, 'running': True, 'died': False,
                              'playing_transition': False, 'playing_end_trantition': False, 'loaded_game': False, 'music': True, 'auto_shoot': False,
                              'won': False, 'cards_on': False}
                    for flag, value in flags.items():
                              setattr(self.game, flag, value)

          def initialize_game_settings(self):
                    self.game.assets = AM.assets
                    self.game.methods = M
                    self.game.render_resolution = RENRES
                    self.game.difficulty = "medium"
                    self.game.fps = 240
                    self.game.reduced_screen_shake = 1
                    self.game.colour_mode = 50
                    self.game.master_volume = 1
                    self.game.text_size = 1

          def initialize_game_state(self):
                    self.game.game_time = 0
                    self.game.lag = 0
                    self.game.uiS.set_colorkey((0, 0, 0))
                    self.game.player = None

          def update_font_sizes(self):
                    self.game.assets["font8"] = pygame.font.Font("Assets/UI/fonts/font8.ttf", int(8 * self.game.text_size))

          def update(self):
                    self.update_display_info()
                    self.update_input()
                    self.update_delta_time()
                    self.update_game_time()
                    self.update_ticks()
                    self.check_player_death()
                    self.check_font_update()
                    self.check_fullscreen()
                    self.check_win_condition()

          def update_display_info(self):
                    self.game.displayinfo = pygame.display.Info()

          def update_input(self):
                    self.game.inputM.update()

          def update_delta_time(self):
                    fps = self.game.clock.get_fps()
                    self.game.dt = min(1 / fps, 1 / 60) if fps != 0 else 0

          def update_game_time(self):
                    if not self.game.changing_settings and not self.game.in_menu and not self.game.cards_on:
                              self.game.game_time += self.game.dt

          def update_ticks(self):
                    self.game.ticks = pygame.time.get_ticks() / 1000

          def check_player_death(self):
                    if self.game.player is not None and self.game.player.health <= 0 and not self.game.won and not self.game.cards_on: self.game.died = True

          def check_font_update(self):
                    if self.game.changing_settings or self.game.in_menu or self.game.died or self.game.won: self.update_font_sizes()

          def check_fullscreen(self):
                    self.game.fullscreen = pygame.display.is_fullscreen()

          def check_win_condition(self):
                    if (getattr(self.game, "enemyM", None) is not None and len(self.game.enemyM.grid.items) == 0 and getattr(self.game, "player", None) is not None and
                            not self.game.player.dead and self.game.game_time > 380): self.game.won = True
