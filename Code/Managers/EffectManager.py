from Code.Variables.SettingVariables import *
from Code.Individuals.Effect import *
from Code.DataStructures.HashMap import *


class EffectManager:
          def __init__(self, game):
                    self.game = game
                    # Initialize a spatial hash map for efficient effect management
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][6])
                    self.count_grid_size = GENERAL["hash_maps"][8]
                    self.count_grid = {}

          def find_cells(self, rect):
                    x1, y1 = rect.topleft
                    x1 //= self.count_grid_size  # Calculate top-left cell
                    y1 //= self.count_grid_size
                    x2, y2 = rect.bottomright
                    x2 = x2 // self.count_grid_size + 1  # Calculate bottom-right cell
                    y2 = y2 // self.count_grid_size + 1
                    return product(range(x1, x2), range(y1, y2))  # Return all cells in range

          def add_count(self, rect):
                    for cell in self._rect_cells(rect):
                              items = self.grid.get(cell)
                              if items is None:
                                        self.count_grid[cell] = 1
                              else:
                                        self.count_grid[cell] += 1

          def update(self):
                    # Update all effects and remove those that have faded out
                    for effect in self.grid.items.copy():
                              effect.update()
                              # Remove effect if it has completely faded (alpha <= 0)
                              if effect.has_been_drawn:
                                        self.grid.remove(effect)
                    # Rebuild the spatial hash map after updates
                    self.grid.rebuild()

          def draw_at(self, rect):
                    for cell in self.find_cells(rect):
                              items = self.count_grid.get(cell)
                              if items is not None and self.count_grid[cell] < BLOOD["max_blood"]:
                                        new_rect = pygame.Rect(rect.centerx - 48 / 6, rect.centery - 48 / 6, 48 / 3, 48 / 3)
                                        collision = self.game.tilemapM.tile_collision(new_rect, "water_tile")
                                        if not collision:
                                                  integer = random.randint(1, 10)
                                                  blood_image = self.game.assets["blood" + str(integer)][0]
                                                  self.game.tilemapM.cached_surface.blit(blood_image, rect)
                              if items is None:
                                        self.count_grid[cell] = 1
                              else:
                                        self.count_grid[cell] += 1

          def draw(self):
                    # Draw all effects that are within the visible window
                    for effect in self.grid.window_query():
                              effect.draw()

          def add_effect(self, pos, direction, dictionary):
                    # Create a new effect and add it to the grid
                    effect = Effect(self.game, pos, direction, dictionary)
                    for cell in self.find_cells(effect.rect):
                              items = self.count_grid.get(cell)
                              if items is not None and self.count_grid[cell] < BLOOD["max_blood"]:
                                        self.grid.insert(effect)
                              if items is None:
                                        self.count_grid[cell] = 1
                              else:
                                        self.count_grid[cell] += 1

class MuzzleFlashManager:
          def __init__(self, game):
                    self.game = game
                    # Initialize a spatial hash map for efficient effect management
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][9])

          def add_muzzle_flash(self, pos, rotation, flip):
                    # Create a new muzzle flash effect and add it to the grid
                    effect = MuzzleFlash(self.game, pos, rotation, flip, self.game.player.gun.name)
                    self.grid.insert(effect)

          def update(self):
                    # Update all effects and remove those that have faded out
                    for effect in self.grid.items.copy():
                              effect.update()
                              # Remove effect if it has completely faded (alpha <= 0)
                              if effect.dead:
                                        self.grid.remove(effect)
                    # Rebuild the spatial hash map after updates
                    self.grid.rebuild()

          def draw(self):
                    # Draw all effects that are within the visible window
                    for effect in self.grid.window_query():
                              effect.draw()

class CasingManager:
          def __init__(self, game):
                    self.game = game
                    # Initialize a spatial hash map for efficient effect management
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][9])

          def add_casing(self, pos, facing):
                    # Create a new muzzle flash effect and add it to the grid
                    effect = Casing(self.game, pos, self.game.player.gun.name, facing)
                    self.grid.insert(effect)

          def update(self):
                    # Update all effects and remove those that have faded out
                    for effect in self.grid.items.copy():
                              effect.update()
                              # Remove effect if it has completely faded (alpha <= 0)
                              if effect.hit_ground:
                                        self.grid.remove(effect)
                    # Rebuild the spatial hash map after updates
                    self.grid.rebuild()

          def draw(self):
                    # Draw all effects that are within the visible window
                    for effect in self.grid.window_query():
                              effect.draw()