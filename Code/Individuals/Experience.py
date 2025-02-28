from Code.Variables.GameVariables import *


class Experience:
          def __init__(self, game, location, name):
                    self.game = game

                    self.images = self.game.assets[name + "_xp"]
                    self.frame = 0
                    self.pos = v2(location)
                    self.name = name
                    self.xp_amount = EXPERIENCE[name]

                    self.game.methods.set_attributes(self, EXPERIENCE["attributes"])

                    self.is_moving = False
                    self.is_collected = False

                    # Initialize rect
                    self.rect = self.images[0].get_rect(center=self.pos)

          def update(self):
                    if self.is_collected:
                              return

                    player_pos = v2(self.game.player.rect.center)
                    distance_to_player = (player_pos - self.pos).length()

                    if distance_to_player <= self.attraction_distance:
                              self.is_moving = True

                    if self.is_moving:
                              direction = (player_pos - self.pos).normalize()
                              self.pos += direction * self.speed * self.game.dt

                              if distance_to_player <= self.collection_distance:
                                        self.is_collected = True
                                        self.collect()

                    # Update rect after moving
                    self.update_rect()
                    self.frame += EXPERIENCE["animation_speed"] * self.game.dt

          def collect(self):
                    # Add XP to the player
                    self.game.player.xp_to_add += self.xp_amount
                    self.game.soundM.play_sound("picked_xp", VOLUMES["picked_xp_frequancy"], VOLUMES["picked_xp_volume"] * self.game.master_volume)
                    # You might want to add some visual or sound effect here

          def update_rect(self):
                    # Update the rect to match the current position
                    self.rect.center = self.pos

          def draw(self):
                    if not self.is_collected:
                              # Convert world coordinates to screen coordinates
                              screen_pos = self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y
                              image = self.images[int(self.frame) % len(self.images)]
                              self.game.displayS.blit(image, screen_pos)

          def reset(self, location, name):
                    self.image = self.game.assets[name + "_xp"]
                    self.pos = v2(location)
                    self.name = name
                    self.xp_amount = EXPERIENCE[name]
                    self.is_moving = False
                    self.is_collected = False

                    # Initialize rect
                    self.rect = self.images[0].get_rect(center=self.pos)
