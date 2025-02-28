from Code.Individuals.Bullet import *
from Code.DataStructures.HashMap import *


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, GENERAL["hash_maps"][1])  # Spatial hash map for efficient collision detection
                    self.bullet_pool = set()  # Object pool for bullet reuse

          def update(self):
                    if not self.game.changing_settings and not self.game.cards_on:
                              current_time = self.game.game_time
                              for bullet in self.grid.items:
                                        bullet.update()
                                        # Check if bullet has exceeded its lifetime
                                        if current_time - bullet.creation_time > bullet.lifetime:
                                                  bullet.dead = True
                              self.check_for_collisions()
                              self.check_dead_bullets()
                              self.grid.rebuild()  # Rebuild the spatial hash map

          def add_bullet(self, pos, angle, name, spread):
                    if self.bullet_pool:
                              # Reuse a bullet from the pool if available
                              bullet = self.bullet_pool.pop()
                              bullet.reset(pos, angle, spread)
                    else:
                              # Create a new bullet if pool is empty
                              bullet = Bullet(self.game, self.game.player.gun, pos, angle, name, spread, self.game.player.gun.noise_map)
                    self.grid.insert(bullet)

                    # Add screen shake effect
                    array = self.game.player.gun.screen_shake, 0.1
                    self.game.cameraM.add_screen_shake(array[1], array[0] * self.game.reduced_screen_shake)

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        self.bullet_pool.add(bullet)  # Return dead bullets to the pool

          def check_for_collisions(self):
                    for bullet in self.grid.items:
                              # Check for collisions with enemies in the same grid cell
                              for enemy in self.game.enemyM.grid.query(bullet.rect):
                                        bullet.collide(enemy)
