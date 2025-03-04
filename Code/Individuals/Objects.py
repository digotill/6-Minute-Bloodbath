from Code.Variables.SettingVariables import *


class Object:
    def __init__(self, game, image, res, pos):
        self.game = game  # Reference to the main game object
        self.original_image = image  # Store the original image
        self.image = image  # Current image (maybe modified later)
        self.res = v2(res)  # Resolution/size of the object
        self.pos = pos  # Position of the object in the game world
        self.rect = self.image.get_rect(center=self.pos)  # Create a rectangle for the object

    def draw(self, surface=None):
        if surface is None:
            surface = self.game.displayS  # Use game's display surface if none provided

        # Calculate drawing position by subtracting camera offset
        draw_pos = (self.rect.x - self.game.cameraM.rect.x,
                    self.rect.y - self.game.cameraM.rect.y)

        surface.blit(self.image, draw_pos)  # Draw the object on the surface

    def draw_shadow(self, surface=None):
        if surface is None:
            surface = self.game.displayS  # Use game's display surface if none provided

        # Generate a shadow image for the object
        shadow_image = self.game.methods.get_shadow_image(self, self.image)

        # Draw the shadow image below the object
        surface.blit(shadow_image, (self.rect.x, self.rect.y + self.res[1] - shadow_image.height / 2 - 2))
