from Code.Individuals.Rain import *
from Code.DataStructures.HashMap import *


class RainManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, GENERAL["hash_maps"][3])  # Spatial hash grid for efficient rain droplet management

                    # Timer to control rain spawning rate
                    self.spawn_timer = Timer(RAIN['spawn_rate'], self.game.game_time, self.spawn_rain)

                    # Surface to draw rain droplets, using alpha channel for transparency
                    self.rain_surface = pygame.Surface(self.game.displayS.get_size(), pygame.SRCALPHA)

                    self.grid.rebuild()  # Initialize the spatial hash grid

          def update(self):
                    if not self.game.changing_settings and not self.game.cards_on:
                              for rain_droplet in self.grid.items:
                                        rain_droplet.update()  # Update position and state of each rain droplet
                                        if rain_droplet.hit_ground:
                                                  rain_droplet.update_frame()  # Animate splash effect for grounded droplets

                              # Spawn new rain droplets based on the timer
                              if self.spawn_timer.update(self.game.game_time):
                                        self.spawn_rain()
                                        self.spawn_timer.reactivate(self.game.game_time)

                              self.check_dead()  # Remove finished rain droplets
                              self.grid.rebuild()  # Rebuild spatial hash grid after updates

          def draw(self):
                    # Clear the rain surface with transparent color
                    self.rain_surface.fill((0, 0, 0, 0))

                    # Draw only the rain droplets visible in the current window
                    for rain_droplet in self.grid.window_query():
                              if not rain_droplet.hit_ground:
                                        # Calculate position relative to camera offset
                                        pos = (rain_droplet.rect.x - self.game.cameraM.rect.x,
                                               rain_droplet.rect.y - self.game.cameraM.rect.y)
                                        self.rain_surface.blit(rain_droplet.animation[0], pos)

                    # Blit the rain surface onto the main display surface
                    self.game.displayS.blit(self.rain_surface, (0, 0))

          def spawn_rain(self):
                    # Spawn multiple rain droplets at once
                    for _ in range(RAIN['amount_spawning']):
                              rain = Rain(self.game, RAIN)
                              self.grid.insert(rain)

          def check_dead(self):
                    # Remove rain droplets that have finished their animation
                    for rain_droplet in self.grid.items.copy():
                              if rain_droplet.frame >= len(rain_droplet.animation):
                                        self.grid.items.remove(rain_droplet)
