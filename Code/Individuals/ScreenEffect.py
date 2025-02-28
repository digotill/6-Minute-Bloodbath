from Code.Variables.SettingVariables import *


class ScreenEffect:
          def __init__(self, game, frames, animation_speed):
                    self.game = game  # Reference to the main game object
                    self.frame = 0  # Current frame of the animation
                    self.length = len(frames) - 1  # Total number of frames minus one
                    self.images = frames  # List of image frames for the effect
                    self.animation_speed = animation_speed  # Speed of the animation
                    self.alpha = 255  # Transparency of the effect (0 = fully transparent)

          def draw(self, order=1, surface=None):
                    if surface is None:
                              surface = self.game.uiS  # Use game's UI surface if none provided

                    if 0 <= self.frame <= self.length:
                              # If within animation frames, draw current frame
                              self.blit(self.images[int(self.frame)], surface)
                              # Update frame counter
                              self.frame += order * self.animation_speed * self.game.dt
                              return False  # Animation not finished
                    elif self.frame > self.length:
                              # If past last frame, draw last frame
                              self.blit(self.images[self.length], surface)
                              # Continue updating frame counter (for potential looping)
                              self.frame += order * self.animation_speed * self.game.dt
                              return True  # Animation finished
                    else:
                              # If past last frame, draw last frame
                              self.blit(self.images[0], surface)
                              # Continue updating frame counter (for potential looping)
                              self.frame += order * self.animation_speed * self.game.dt
                              return False


          def blit(self, image, surface):
                    # Create a transparent version of the image
                    temp_surface = pygame.transform.scale(self.game.methods.get_transparent_image(image, self.alpha), self.game.render_resolution)
                    # Draw the transparent image on the provided surface
                    surface.blit(temp_surface)
