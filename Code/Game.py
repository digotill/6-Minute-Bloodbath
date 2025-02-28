import time

from Code.Variables.SettingVariables import *
from Code.Managers import *
from Code.Shaders import *
from Code.Variables.GameVariables import *
from Code.Variables.LoadAssets import *
from Code.Individuals.Player import *
from Code.Managers.InputManager import *
from Code.Variables.LoadSaveData import *

class Game:
          def __init__(self):

                    # Set up display and rendering surfaces
                    self.display = DISPLAY
                    self.displayS = pygame.Surface(RENRES).convert()
                    self.uiS = pygame.Surface(RENRES).convert()
                    self.shader = Shader(DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER, self.displayS)

                    # Initialize clock for managing frame rate
                    self.clock = pygame.time.Clock()
                    self.inputM = InputManager(self)
                    self.gameV = GameVariables(self)

                    # Initialize various game managers
                    self.eventM = EventManager(self)
                    self.backgroundM = BackgroundManager(self)
                    self.soundM = SoundManager(self)
                    self.interactablesM = InteractablesManager(self)
                    self.screeneffectM = ScreenEffectManager(self)
                    self.uiM = UIManager(self)

                    self.data = Data(self)
                    self.data.load_data()

          def refresh(self):
                    # Refresh the display and restart the game
                    pygame.mixer.music.stop()
                    pygame.display.flip()
                    self.__init__()
                    self.screeneffectM.set_transition_to_play()
                    self.run_game()

          def load_game(self):
                    start_load_time = time.time()
                    self.uiM.draw_loading()
                    self.shader.render_direct(pygame.Rect(0, 0, self.display.width, self.display.height))
                    pygame.display.flip()
                    pygame.mouse.set_visible(True)
                    self.soundM.fade_music(1000, self.assets["loading_music"])
                    managers = {
                              "enemyM": EnemyManager, "effectM": EffectManager, "muzzleflashM": MuzzleFlashManager, "casingM": CasingManager,
                              "bulletM": BulletManager, "rainM": RainManager, "drawingM": DrawingManager, "grassM": GrassManager, "tilemapM": TileMapManager,
                              "objectM": ObjectManager,"experienceM": ExperienceManager, "player": Player, "cameraM": CameraManager, "cardM": CardManager}
                    for manager_name, manager_class in managers.items():
                              setattr(self, manager_name, manager_class(self))
                    self.soundM.fade_music(1000, self.assets["game_music"])
                    pygame.mouse.set_visible(False)
                    print(time.time() - start_load_time)

          def check_if_load_game(self):
                    if not self.loaded_game and not self.in_menu:
                              self.load_game()
                              self.loaded_game = True

          def update_managers(self):
                    # Update game entities and managers
                    if not self.in_menu:
                              for manager in [self.enemyM, self.bulletM, self.experienceM, self.rainM, self.player, self.effectM, self.cameraM, self.muzzleflashM, self.cardM, self.casingM]:
                                        manager.update()
                    self.interactablesM.update()
                    self.soundM.update()

          def draw_managers(self):
                    # Draw game elements in order
                    if not self.in_menu:
                              for manager in [self.tilemapM, self.effectM, self.drawingM, self.rainM, self.uiM, self.cardM]:
                                        manager.draw()
                    for manager in [self.backgroundM, self.interactablesM, self.screeneffectM]:
                              manager.draw()

          def update_display(self):
                    # Update the display with all drawn elements
                    self.lag += self.dt
                    if self.lag >= 1.0 / self.fps:
                              self.uiM.update_display()
                              self.shader.render_direct(pygame.Rect(0, 0, self.display.width, self.display.height))
                              pygame.display.flip()
                              self.lag = self.lag % (1.0 / self.fps)

          def run_game(self):
                    self.soundM.play_music(self.assets["menu_music"])
                    # Main game loop
                    while self.running:
                              self.clock.tick_busy_loop(1000000)
                              self.check_if_load_game()
                              self.gameV.update()
                              self.eventM.handle_events()
                              self.update_managers()
                              self.draw_managers()
                              self.update_display()
                              if self.restart:
                                        self.data.save_data()
                                        self.refresh()
                    self.data.save_data()
