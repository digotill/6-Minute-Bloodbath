from Code.Variables.SettingVariables import *
from Code.Individuals.Gun import *

class GameVariables:
          def __init__(self, game):
                    self.game = game  # Store reference to the game object

                    self.game.changing_settings = False  # Flag for settings change state
                    self.game.immidiate_quit = False  # Flag for immediate game quit
                    self.game.in_menu = True  # Flag for menu state
                    self.game.restart = False  # Flag for game restart
                    self.game.running = True  # Flag for game running state
                    self.game.died = False  # Flag for player death
                    self.game.playing_transition = False  # Flag for transition state
                    self.game.playing_end_trantition = False  # Flag for end screen transition state
                    self.game.loaded_game = False    # Flag for whether a game has been loaded
                    self.game.music = True
                    self.game.auto_shoot = False
                    self.game.won = False
                    self.game.cards_on = False

                    self.game.assets = AM.assets  # Store game assets
                    self.game.methods = M  # Store game methods
                    self.game.render_resolution = RENRES  # Set render resolution

                    self.game.game_time = 0  # Initialize game time
                    self.game.difficulty = "medium"  # Set default difficulty
                    self.game.fps = 240  # Set frames per second
                    self.game.lag = 0
                    self.game.uiS.set_colorkey((0, 0, 0))  # Set UI surface transparency
                    self.game.player = None  # Initialize player object
                    self.game.reduced_screen_shake = 1
                    self.game.colour_mode = 50
                    self.game.master_volume = 1
                    self.game.text_size = 1
                    self.update_font_sizes()
                    self.update()  # Call update method

          def update_font_sizes(self):
                    self.game.assets["font8"] = pygame.font.Font("Assets/UI/fonts/font8.ttf", int(8 * self.game.text_size))

          def update(self):
                    # Update game state variables each frame
                    self.game.displayinfo = pygame.display.Info()
                    self.game.inputM.update()  # Update input manager
                    if self.game.clock.get_fps() != 0: self.game.dt = min(1 / self.game.clock.get_fps(), 1/60)  # Calculate delta time
                    else: self.game.dt = 0
                    if not self.game.changing_settings and not self.game.in_menu and not self.game.cards_on: self.game.game_time += self.game.dt  # Update game time
                    self.game.ticks = pygame.time.get_ticks() / 1000  # Get current time in seconds
                    if self.game.ticks % 10 == 0: gc.collect()  # Perform garbage collection every 10 seconds
                    if self.game.player is not None and self.game.player.health <= 0 and not self.game.won and not self.game.cards_on: self.game.died = True  # Check for player death
                    if self.game.changing_settings or self.game.in_menu or self.game.died or self.game.won: self.update_font_sizes()  # Update font sizes
                    self.game.fullscreen = pygame.display.is_fullscreen()  # Flag for fullscreen mode
                    if getattr(self.game, "enemyM", None) is not None and len(self.game.enemyM.grid.items) == 0 and not self.game.player.dead and self.game.game_time > 380:self.game.won = True