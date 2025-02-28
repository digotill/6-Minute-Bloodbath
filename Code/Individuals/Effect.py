from Code.Variables.SettingVariables import *


class Effect:
          def __init__(self, game, pos, angle, dictionary):
                    self.game = game
                    self.game.methods.set_attributes(self, dictionary)  # Set attributes from the provided dictionary

                    self.pos = v2(pos)
                    self.set_rect()
                    # Randomly select an image set for variety
                    self.images = self.game.assets[self.name + str(random.randint(1, self.variety))]
                    self.frame = 0
                    self.length = len(self.images) - 1
                    self.alpha = 255
                    self.end_frame = random.randint(0, self.length)

                    # Add randomness to speed and set velocity vector
                    self.speed = self.speed[0] + random.uniform(-self.speed[0], self.speed[0])
                    self.vel_vector = v2(0, -self.speed).rotate(-angle)
                    self.should_draw = True

                    self.grounded = False
                    self.grounded_time = 0
                    self.time_when_grounded = None
                    self.has_been_drawn = False

          def update(self):
                    if not self.grounded and not self.game.changing_settings and not self.game.cards_on:
                              # Check for collision with water tiles
                              rect = pygame.Rect(self.pos.x - self.res[0] / 6, self.pos.y - self.res[1] / 6, self.res[0] / 3, self.res[1] / 3)
                              collision = self.game.tilemapM.tile_collision(rect, "water_tile")

                              if not collision and self.frame >= self.length:
                                        self.grounded = True
                              else:
                                        # Update position and animation frame
                                        self.pos += self.vel_vector * self.game.dt
                                        self.rect.center = self.pos
                                        self.frame += self.animation_speed * self.game.dt
                                        if collision and self.frame >= self.length and self in self.game.effectM.grid.items:
                                                  self.should_draw = False

          def draw(self, surface=None):
                    if self.should_draw and not self.grounded:
                              if surface is None:
                                        surface = self.game.displayS
                              # Select the appropriate frame
                              frame = int(self.frame) % len(self.images) if not self.grounded else self.end_frame
                              image = self.images[frame]

                              # Draw the image, accounting for camera offset
                              surface.blit(image, (self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y))
                    elif self.grounded and not self.has_been_drawn:
                              frame = int(self.frame) % len(self.images) if not self.grounded else self.end_frame
                              image = self.images[frame]
                              self.game.tilemapM.cached_surface.blit(image, self.rect)
                              self.has_been_drawn = True

          def set_rect(self):
                    # Set the rectangle for the effect
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0], self.res[1])


class MuzzleFlash:
          def __init__(self, game, pos, rotation, flip, name):
                    self.game = game

                    # Randomly select an image set for variety
                    self.images = self.game.assets[name + "_flash"]
                    self.images = [pygame.transform.flip(pygame.transform.rotate(image, rotation), True, False) if flip else pygame.transform.rotate(image, -rotation + 180) for image in self.images]
                    self.res = self.images[0].size

                    self.frame = 0
                    self.animation_speed = GENERAL['animation_speeds'][4]
                    self.pos = v2(pos)
                    self.set_rect()
                    self.dead = False

          def update(self):
                    if self.frame > len(self.images) - 1:
                              self.dead = True
                    elif not self.game.changing_settings:
                              self.frame += self.animation_speed * self.game.dt
                              self.pos = v2(self.game.player.gun.calculate_position(2))
                              self.set_rect()

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.displayS
                              # Select the appropriate frame
                    frame = int(self.frame) % len(self.images)
                    image = self.images[frame]

                    # Draw the image, accounting for camera offset
                    surface.blit(image, (self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y))

          def set_rect(self):
                    # Set the rectangle for the effect
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0], self.res[1])

class Casing:
          def __init__(self, game, pos, name, facing):
                    self.game = game

                    # Randomly select an image set for variety
                    self.images = self.game.assets[name + "_casing"]
                    self.images = [pygame.transform.flip(image, True, False) if facing else image for image in self.images]
                    self.res = self.images[0].size

                    self.frame = 0
                    self.animation_speed = GENERAL['animation_speeds'][5]
                    self.pos = v2(pos)
                    self.set_rect()
                    self.hit_ground = False

          def update(self):
                    if self.frame > len(self.images) - 1:
                              self.hit_ground = True
                              self.game.tilemapM.cached_surface.blit(self.images[-1], self.rect)
                    elif not self.game.changing_settings:
                              self.frame += self.animation_speed * self.game.dt

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.displayS
                              # Select the appropriate frame
                    frame = int(self.frame) % len(self.images)
                    image = self.images[frame]

                    # Draw the image, accounting for camera offset
                    surface.blit(image, (self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y))

          def set_rect(self):
                    # Set the rectangle for the effect
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0], self.res[1])
