from Code.Utilities.SaveLoadSystem import *
import pygame


class Data:
          def __init__(self, game):
                    self.game = game

                    self.save_folder = "DataSave"
                    self._validate_save_folder()
                    self.save_load_system = SaveLoadSystem(".save", self.save_folder)
                    self.slider_configs = {
                              'fps': {'default': pygame.display.get_current_refresh_rate()}, 'brightness': {'default': 100}, 'shake': {'default': 20},
                              'colour': {'default': 50}, 'volume': {'default': 50}, 'text_size': {'default': 200}}

          def _validate_save_folder(self):
                    if not os.path.exists(self.save_folder):
                              os.makedirs(self.save_folder)
                              print(f"Created save folder: {self.save_folder}")

          def load_data(self):
                    for slider_name, config in self.slider_configs.items():
                              value = self.save_load_system.load_game_data([slider_name], [config['default']])
                              self.game.interactablesM.sliders[slider_name].value = value

                    self.game.wins = self.save_load_system.load_game_data(["wins"], [0])
                    self.game.master_volume = self.game.interactablesM.sliders["volume"].value
                    self.game.music = self.save_load_system.load_game_data(["music"], [True])

          def save_data(self):
                    for slider_name in self.slider_configs.keys():
                              value = self.game.interactablesM.sliders[slider_name].value
                              self.save_load_system.save_game_data([value], [slider_name])

                    self.save_load_system.save_game_data([self.game.wins], ["wins"])
                    self.save_load_system.save_game_data([self.game.music], ["music"])

          def load_default_data(self):
                    for slider_name, config in self.slider_configs.items():
                              default_value = config['default']
                              self.game.interactablesM.sliders[slider_name].value = default_value
                              self.save_load_system.save_game_data([default_value], [slider_name])
