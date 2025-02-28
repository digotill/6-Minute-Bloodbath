from Code.Variables.SettingVariables import *
from Code.Individuals.ScreenEffect import ScreenEffect


class ScreenEffectManager:
          def __init__(self, game):
                    self.game = game
                    self.initialize_screen_effects()
                    self.initialize_flags()

          def initialize_screen_effects(self):
                    self.transition_effect = ScreenEffect(self.game, self.game.assets["transition_screeneffect"], GENERAL['animation_speeds'][1])
                    self.youdied_effect = ScreenEffect(self.game, self.game.assets["youdied_screeneffect"], GENERAL['animation_speeds'][2])
                    self.blood_effect = ScreenEffect(self.game, self.game.assets["blood_screeneffect"], GENERAL['animation_speeds'][6])
                    self.youwon_effect = ScreenEffect(self.game, self.game.assets["youwin_screeneffect"], GENERAL['animation_speeds'][2])

          def initialize_flags(self):
                    self.inverted_transition = False
                    self.youdied_start_time = None
                    self.youdied_duration = 3
                    self.youwon_start_time = None
                    self.youwon_duration = 3
                    self.draw_restart_transition = False
                    self.drawing_restart_transition = False
                    self.play_start_transition = False
                    self.has_blood_effect = False
                    self.blood_effect_start_time = None

          def set_transition_to_play(self):
                    self.play_start_transition = True
                    self.transition_effect.frame = self.transition_effect.length

          def add_blood_effect(self):
                    if not self.has_blood_effect:
                              self.has_blood_effect = True
                              self.blood_effect_start_time = self.game.game_time

          def draw(self):
                    self.game.uiM.draw_xp_bar()
                    self.handle_you_died_effect()
                    self.handle_you_won_effect()
                    self.draw_start_transition()
                    self.handle_menu_to_game_transition()
                    self.handle_game_start_transition()
                    self.handle_in_game_transition()
                    self.handle_restart_transition()


          def draw_start_transition(self):
                    if self.play_start_transition:
                              self.transition_effect.draw(-1)
                              if self.transition_effect.frame < 0:
                                        self.play_start_transition = False
                                        self.transition_effect.frame = 0

          def handle_menu_to_game_transition(self):
                    if self.game.playing_transition and self.game.in_menu:
                              if self.transition_effect.draw():
                                        self.game.in_menu = False

          def handle_game_start_transition(self):
                    if not self.game.in_menu and self.game.game_time < 1:
                              self.transition_effect.draw()

          def handle_in_game_transition(self):
                    if not self.game.in_menu and self.game.game_time >= 1 and self.game.playing_transition:
                              if not self.inverted_transition:
                                        self.transition_effect.frame = self.transition_effect.length
                                        self.inverted_transition = True
                              self.transition_effect.draw(-1)
                              if self.transition_effect.frame < 0:
                                        self.game.playing_transition = False

          def handle_you_won_effect(self):
                    if self.game.won:
                              if self.youwon_start_time is None:
                                        self.youwon_start_time = self.game.game_time
                                        pygame.mixer.music.stop()
                                        if self.game.difficulty == "easy":
                                                  self.game.wins += 1
                                        elif self.game.difficulty == "medium":
                                                  self.game.wins += 2
                                        elif self.game.difficulty == "hard":
                                                  self.game.wins += 3
                                        self.game.soundM.play_sound("youwon_sound", VOLUMES["youwon_frequancy"], VOLUMES["youwon_volume"] * self.game.master_volume)
                              elapsed_time = self.game.game_time - self.youwon_start_time
                              self.youwon_effect.alpha = min(max(elapsed_time / self.youwon_duration, 0), 1) * 255
                              self.youwon_effect.draw()

          def handle_you_died_effect(self):
                    if self.game.died:
                              if self.youdied_start_time is None:
                                        self.youdied_start_time = self.game.game_time
                                        pygame.mixer.music.stop()
                                        self.game.soundM.play_sound("youdied_sound", VOLUMES["youdied_frequancy"], VOLUMES["youdied_volume"] * self.game.master_volume)
                              elapsed_time = self.game.game_time - self.youdied_start_time
                              self.youdied_effect.alpha = min(max(elapsed_time / self.youdied_duration, 0), 1) * 255
                              self.youdied_effect.draw()

          def handle_restart_transition(self):
                    if self.draw_restart_transition:
                              self.transition_effect.frame = 0
                              self.drawing_restart_transition = True
                              self.draw_restart_transition = False
                    if self.drawing_restart_transition:
                              self.transition_effect.draw()
                              if self.transition_effect.frame > self.transition_effect.length + 3:
                                        self.game.restart = True

          def draw_blood_effect(self):
                    if self.has_blood_effect and not self.game.died and not self.game.won:
                              elapsed_time = self.game.game_time - self.blood_effect_start_time
                              if elapsed_time < BLOOD["blood_effect_duration"]:
                                        self.blood_effect.draw()
                                        if self.blood_effect.frame > self.blood_effect.length:
                                                  self.blood_effect.frame = self.blood_effect.length
                              elif elapsed_time > BLOOD["blood_effect_duration"]:
                                        self.blood_effect.draw(-1)
                                        if self.blood_effect.frame < 0:
                                                  self.has_blood_effect = False

          def draw_blood_when_dead(self):
                    if self.game.died and not self.game.won:
                              self.blood_effect.frame = self.blood_effect.length
                              self.blood_effect.draw()
