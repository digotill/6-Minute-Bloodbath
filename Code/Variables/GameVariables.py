from Code.Variables.SettingVariables import *
from Code.Individuals.Gun import *


class GameVariables:
    def __init__(self, game):
        self.game = game
        self.initialize_game_flags()  # Initialize game state flags
        self.initialize_game_settings()  # Set initial game settings
        self.initialize_game_state()  # Initialize game state variables
        self.update_font_sizes()  # Set initial font sizes
        self.update()  # Perform initial update to set up game variables

    def initialize_game_flags(self):
        # Define initial state flags for the game
        flags = {
            'changing_settings': False, 'immidiate_quit': False, 'in_menu': True, 'restart': False,
            'running': True, 'died': False,
            'playing_transition': False, 'playing_end_trantition': False, 'loaded_game': False,
            'music': True, 'auto_shoot': False,
            'won': False, 'cards_on': False}
        # Set each flag as an attribute of the game object
        for flag, value in flags.items():
            setattr(self.game, flag, value)

    def initialize_game_settings(self):
        # Set initial game settings
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
        # Initialize game state variables
        self.game.game_time = 0
        self.game.lag = 0
        self.game.uiS.set_colorkey((0, 0, 0))  # Set transparency color key for UI surface
        self.game.player = None  # Initialize player as None

    def update_font_sizes(self):
        # Update font sizes based on game settings
        self.game.assets["font8"] = pygame.font.Font("Assets/UI/fonts/font8.ttf",
                                                     int(8 * self.game.text_size))

    def update(self):
        # Update various game variables and states
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
        # Update display information
        self.game.displayinfo = pygame.display.Info()

    def update_input(self):
        # Update input manager
        self.game.inputM.update()

    def update_delta_time(self):
        # Calculate delta time based on current FPS
        fps = self.game.clock.get_fps()
        self.game.dt = min(1 / fps, 1 / 60) if fps != 0 else 0

    def update_game_time(self):
        # Update game time if not in certain states
        if not self.game.changing_settings and not self.game.in_menu and not self.game.cards_on:
            self.game.game_time += self.game.dt

    def update_ticks(self):
        # Update game ticks
        self.game.ticks = pygame.time.get_ticks() / 1000

    def check_player_death(self):
        # Check if the player has died
        if self.game.player is not None and self.game.player.health <= 0 and not self.game.won and not self.game.cards_on:
            self.game.died = True

    def check_font_update(self):
        # Update font sizes if in certain states
        if self.game.changing_settings or self.game.in_menu or self.game.died or self.game.won:
            self.update_font_sizes()

    def check_fullscreen(self):
        # Check if the game is in fullscreen mode
        self.game.fullscreen = pygame.display.is_fullscreen()

    def check_win_condition(self):
        # Check if the win condition is met
        if (getattr(self.game, "enemyM", None) is not None and len(
                self.game.enemyM.grid.items) == 0 and getattr(self.game, "player", None) is not None and
                not self.game.player.dead and self.game.game_time > 380):
            self.game.won = True
