from Code.Variables.SettingVariables import *


class DrawingManager:
          def __init__(self, game):
                    self.game = game
                    # List to store objects that need to be drawn
                    self.drawables = []

          def transparent_objects(self):
                    # Get the player's rectangle and bottom position
                    player_rect = self.game.player.rect
                    player_bottom = player_rect.bottom

                    # Iterate through objects that intersect with the player's rectangle
                    for thing in self.game.objectM.grid.query(player_rect):
                              if thing.rect.colliderect(player_rect):
                                        # Calculate the vertical distance between the object and player
                                        dy = thing.rect.bottom - player_bottom
                                        squared_distance = dy * dy
                                        greatest_side = thing.image.get_height()

                                        # Calculate alpha based on the distance (closer objects are more transparent)
                                        alpha = max(100, min(int(squared_distance / (greatest_side * greatest_side) * 255), 255))

                                        # If the player is below the object, make it fully opaque
                                        if player_bottom > thing.rect.bottom:
                                                  alpha = 255

                                        # Apply transparency to the object's image
                                        thing.image = self.game.methods.get_transparent_image(thing.original_image, alpha)
                              else:
                                        # If not colliding, use the original image
                                        thing.image = thing.original_image

          def draw(self):
                    # Apply transparency to objects that might obstruct the player's view
                    self.transparent_objects()

                    # Add drawable objects from various game managers to the drawables list
                    self.drawables.extend(self.game.objectM.grid.window_query())
                    self.drawables.extend(self.game.enemyM.grid.window_query())
                    self.drawables.extend(self.game.bulletM.grid.window_query())
                    self.drawables.extend(self.game.experienceM.grid.window_query())
                    self.drawables.extend(self.game.casingM.grid.window_query())
                    self.drawables.extend(self.game.grassM.draw())
                    # Add only rain particles that have hit the ground
                    self.drawables.extend([r for r in self.game.rainM.grid.window_query() if r.hit_ground])
                    # Add the player to the drawables list
                    self.drawables.append(self.game.player)

                    # Sort drawables based on their bottom y-coordinate for proper layering
                    self.drawables.sort(key=lambda obj: obj.rect.bottom)

                    # Draw all objects in the sorted order
                    for drawable in self.drawables:
                              drawable.draw()

                    # Clear the drawables list for the next frame
                    self.drawables.clear()
