from Code.Variables.SettingVariables import *


class Background:
          def __init__(self, game, frames, animation_speed):
                    self.game = game  # Reference to the main game object
                    self.frame = 0  # Current frame index (can be fractional)
                    self.length = len(frames) - 1  # Total number of frames minus one
                    self.images = frames  # List of image surfaces for the animation
                    self.animation_speed = animation_speed  # Speed of the animation
                    if self.images[0].size != self.game.displayS.size:
                              self.images = [pygame.transform.scale(image, self.game.displayS.size) for image in self.images]

          def draw(self):
                    # Calculate current frame index, wrapping around if needed
                    current_frame = int(self.frame) % self.length

                    # Draw the current frame on the game's display surface
                    self.game.displayS.blit(self.images[current_frame], (0, 0))

                    # Update frame counter for next draw call, using delta time for consistent speed
                    self.frame += self.animation_speed * self.game.dt
