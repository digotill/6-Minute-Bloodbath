from Code.Individuals.Background import *


class BackgroundManager:
          def __init__(self, game):
                    self.game = game  # Reference to the main game object

                    # Create the main menu background
                    # AM.assets['main_menu'] likely contains the frame images for the main menu background
                    # GENERAL['animation_speeds'][0] is the animation speed for the main menu background
                    self.main_background = Background(self.game, AM.assets['main_menu'], GENERAL['animation_speeds'][0])

          def draw(self):
                    # Draw the main menu background only when the game is in the menu state
                    if self.game.in_menu:
                              self.main_background.draw()

                              rect = self.game.assets["tutorial"].get_rect(center=UI["tutorial_pos"])
                              self.game.displayS.blit(self.game.assets["tutorial"], rect)

                              wins = max(min(int(self.game.wins), 10), 0)
                              rect = self.game.assets["wins" + str(wins)].get_rect(center=UI["wins_pos"])
                              self.game.displayS.blit(self.game.assets["wins" + str(wins)], rect)
