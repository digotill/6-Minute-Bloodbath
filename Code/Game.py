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
        self.display = DISPLAY  # Main display surface
        self.displayS = pygame.Surface(RENRES).convert()  # Surface for rendering game visuals
        self.uiS = pygame.Surface(RENRES).convert()  # Surface for rendering UI elements
        self.shader = Shader(DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER,
                             self.displayS)  # Shader for rendering effects

        # Initialize clock for managing frame rate
        self.clock = pygame.time.Clock()  # Clock to control game loop timing
        self.inputM = InputManager(self)  # Manager for handling user input
        self.gameV = GameVariables(self)  # Game variables manager

        # Initialize various game managers
        self.eventM = EventManager(self)  # Manager for handling game events
        self.backgroundM = BackgroundManager(self)  # Manager for background elements
        self.soundM = SoundManager(self)  # Manager for sound effects and music
        self.interactablesM = InteractablesManager(self)  # Manager for interactable objects
        self.screeneffectM = ScreenEffectManager(self)  # Manager for screen effects
        self.uiM = UIManager(self)  # Manager for UI elements

        self.data = Data(self)  # Data manager for loading and saving game data
        self.data.load_data()  # Load game data

    def refresh(self):
        pygame.mixer.music.stop()  # Stop any currently playing music
        pygame.display.flip()  # Update the display with any pending changes
        self.__init__()  # Reinitialize the game to reset its state
        self.screeneffectM.set_transition_to_play()  # Set the screen effect manager to transition to the play state
        self.run_game()  # Start the main game loop

    def load_game(self):
        start_load_time = time.time()  # Record the start time for loading
        self.uiM.draw_loading()  # Display loading screen
        pygame.mouse.set_visible(True)  # Make the mouse cursor visible
        self.soundM.fade_music(1000, self.assets["loading_music"])  # Fade in loading music

        # Dictionary of manager names and their corresponding classes
        managers = {
            "enemyM": EnemyManager, "effectM": EffectManager, "muzzleflashM": MuzzleFlashManager,
            "casingM": CasingManager,
            "bulletM": BulletManager, "rainM": RainManager, "drawingM": DrawingManager,
            "grassM": GrassManager,
            "tilemapM": TileMapManager, "objectM": ObjectManager, "experienceM": ExperienceManager,
            "player": Player,
            "cameraM": CameraManager, "cardM": CardManager}

        # Initialize each manager and assign it as an attribute of the Game instance
        for manager_name, manager_class in managers.items():
            setattr(self, manager_name, manager_class(self))

        self.soundM.fade_music(1000, self.assets["game_music"])  # Fade in game music
        pygame.mouse.set_visible(False)  # Hide the mouse cursor
        print("load time: ", time.time() - start_load_time)  # Print the total load time

    def check_if_load_game(self):
        # Check if the game needs to be loaded
        if not self.loaded_game and not self.in_menu:
            self.load_game()  # Load the game if it hasn't been loaded and the player is not in the menu
            self.loaded_game = True  # Set the flag to indicate the game has been loaded

    def update_managers(self):
        # Update game entities and managers
        if not self.in_menu:  # Only update managers if not in the menu
            # Iterate over each manager and call their update method
            for manager in [self.enemyM, self.bulletM, self.experienceM, self.rainM, self.player,
                            self.effectM, self.cameraM, self.muzzleflashM, self.cardM, self.casingM]:
                manager.update()  # Update each manager
        self.interactablesM.update()  # Update interactable objects
        self.soundM.update()  # Update sound manager

    def draw_managers(self):
        # Draw game elements in order
        if not self.in_menu:  # Only draw managers if not in the menu
            # Iterate over each manager and call their draw method
            for manager in [self.tilemapM, self.effectM, self.drawingM, self.rainM, self.uiM,
                            self.cardM]:
                manager.draw()  # Draw each manager
        # Draw background, interactables, and screen effects
        for manager in [self.backgroundM, self.interactablesM, self.screeneffectM]:
            manager.draw()  # Draw each manager

    def update_display(self):
        # Update the display with all drawn elements
        self.lag += self.dt  # Increment lag by the time delta
        if self.lag >= 1.0 / self.fps:  # Check if it's time to update the display based on the frame rate
            self.uiM.update_display()  # Update the UI display
            # Render the shader directly onto the display surface
            self.shader.render_direct(pygame.Rect(0, 0, self.display.width, self.display.height))
            pygame.display.flip()  # Flip the display to show the updated frame
            self.lag = self.lag % (1.0 / self.fps)  # Reset lag, keeping any leftover time

    def run_game(self):
        self.soundM.play_music(self.assets["menu_music"])  # Start playing menu music
        # Main game loop
        while self.running:  # Continue running while the game is active
            self.clock.tick_busy_loop(1000000)  # Control the frame rate
            self.check_if_load_game()  # Check and load the game if necessary
            self.gameV.update()  # Update game variables
            self.eventM.handle_events()  # Handle user input and other events
            self.update_managers()  # Update all game managers
            self.draw_managers()  # Draw all game elements
            self.update_display()  # Update the display with the drawn elements
            if self.restart:  # Check if a game restart is requested
                self.data.save_data()  # Save current game data
                self.refresh()  # Refresh the game state
        self.data.save_data()  # Save game data when exiting the loop
