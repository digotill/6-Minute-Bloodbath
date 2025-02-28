from Code.Individuals.Objects import *
from Code.DataStructures.HashMap import *


class ObjectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, GENERAL["hash_maps"][4])  # Spatial hash grid for efficient object lookup and collision detection
                    self.biome_map, self.density_map = self.game.tilemapM.biome_map, self.game.tilemapM.density_map  # Get biome and density maps for object placement
                    self.generate_objects()  # Generate trees and rocks in the game world
                    self.generate_grass()  # Generate grass tiles throughout the map
                    self.draw_shadows()  # Pre-render shadows for all objects

          def draw_shadows(self):
                    for object1 in self.grid.items:
                              object1.draw_shadow(self.game.tilemapM.cached_surface)  # Draw shadow for each object on the pre-rendered surface

          def generate_objects(self):
                    self._generate_trees()  # Place trees based on biome and density
                    self._generate_rocks()  # Randomly place rocks in the world
                    self.grid.rebuild()  # Rebuild the spatial hash grid to optimize object lookup

          def _generate_trees(self):
                    size = GENERAL["enviroment_density"][1]
                    sorted_biomes = sorted(BIOMES.items(), key=lambda x: x[1])  # Sort biomes for efficient lookup
                    for y in range(0, GAMESIZE[1], size):
                              for x in range(0, GAMESIZE[0], size):
                                        biome_value = self.biome_map[y // size][x // size]  # Get biome value for current position
                                        density_value = self.density_map[y // size][x // size]  # Get density value for current position
                                        biome, biome_density_factor = self._get_biome_info(biome_value, sorted_biomes)  # Determine biome and its density factor

                                        if self._should_place_tree(density_value, biome_density_factor):  # Check if a tree should be placed here
                                                  self._place_tree(x, y, biome)  # Place a tree of the appropriate biome type

          def _generate_rocks(self):
                    for _ in range(GENERAL["enviroment_density"][2]):  # Generate a fixed number of rocks
                              number = random.randint(1, 5)  # Randomly choose the number of rock images
                              image = AM.assets["rock" + str(number)]  # Choose a random rock image
                              pos = self.generate_valid_position(image.size)  # Find a valid position for the rock
                              if pos:
                                        self.grid.insert(Object(self.game, image, image.size, pos))  # Add the rock to the game world

          def generate_grass(self):
                    size = GENERAL["enviroment_density"][1]
                    for tile in self.game.tilemapM.grid.items:
                              if tile.tile_type == "grass_tile":  # Only place grass on grass tiles
                                        biome_x, biome_y = int(tile.position.x) // size, int(tile.position.y) // size
                                        if self._is_valid_biome_position(biome_x, biome_y):
                                                  self._place_grass(tile, biome_x, biome_y)  # Place grass on valid positions

          def generate_valid_position(self, size, base_x=None, base_y=None):
                    base_x = base_x or random.randint(0, GAMESIZE[0])  # Start with given base_x or random x
                    base_y = base_y or random.randint(0, GAMESIZE[1])  # Start with given base_y or random y
                    v = 30  # Variation range for position adjustment
                    for _ in range(10):  # Try up to 10 times to find a valid position
                              x = base_x + random.randint(-v, v)  # Adjust x within variation range
                              y = base_y + random.randint(-v, v)  # Adjust y within variation range
                              if self._is_valid_position(x, y, size):
                                        return v2(x, y)  # Return valid position as a vector
                    return None  # Return None if no valid position found

          def _is_valid_position(self, x, y, size):
                    if 0 <= x < GAMESIZE[0] - size[0] and 0 <= y < GAMESIZE[1] - size[1]:  # Check if position is within game bounds
                              rect = pygame.Rect(x - size[0] * 0.25, y + size[1] * 0.5, size[0] / 2, size[1] / 10)  # Create a rect for collision check
                              return not self.game.tilemapM.tile_collision(rect, "water_tile")  # Check if not colliding with water tiles
                    return False

          @staticmethod
          def _get_biome_from_value(biome_value):
                    sorted_biomes = sorted(BIOMES.items(), key=lambda x: x[1][0])  # Sort biomes by their threshold values
                    for biome_name, data in sorted_biomes:
                              if biome_value < data[0]:  # Find the first biome whose threshold is greater than the biome value
                                        return biome_name
                    return sorted_biomes[-1][0]  # Return the last biome if no threshold is met

          @staticmethod
          def _get_biome_info(biome_value, sorted_biomes):
                    biome = "forest"  # Default biome
                    biome_density_factor = 1  # Default density factor
                    for biome_name, data in sorted_biomes:
                              if biome_value < data[0]:  # Find the appropriate biome based on the biome value
                                        biome = biome_name
                                        biome_density_factor = data[1]
                                        break
                    return biome, biome_density_factor

          @staticmethod
          def _should_place_tree(density_value, biome_density_factor):
                    return random.random() < density_value * GENERAL["enviroment_density"][0] * biome_density_factor  # Probability check for tree placement

          def _place_tree(self, x, y, biome):
                    tree_image = random.choice(self.game.assets[biome + "_tree"])  # Choose a random tree image for the biome
                    pos = self.generate_valid_position(tree_image.size, x, y)  # Find a valid position near the given coordinates
                    if pos:
                              self.grid.insert(Object(self.game, tree_image, tree_image.size, pos))  # Add the tree to the game world

          def _is_valid_biome_position(self, biome_x, biome_y):
                    return 0 <= biome_x < len(self.biome_map[0]) and 0 <= biome_y < len(self.biome_map)  # Check if position is within biome map bounds

          def _place_grass(self, tile, biome_x, biome_y):
                    biome_value = self.biome_map[biome_y][biome_x]  # Get biome value for the current position
                    biome = self._get_biome_from_value(biome_value)  # Determine the biome type
                    v = random.random()  # Random value for grass density check
                    if v < self.game.grassM.density:  # Check if grass should be placed based on density
                              grass_asset_key = f"{biome}_grass"  # Get the appropriate grass asset for the biome
                              grass_x = int(tile.position.x) // GRASS["tile_size"]  # Calculate grass tile x coordinate
                              grass_y = int(tile.position.y) // GRASS["tile_size"]  # Calculate grass tile y coordinate
                              self.game.grassM.place_tile(
                                        (grass_x, grass_y),
                                        int(v * 12),  # Determine grass variation
                                        GRASS["positions"][grass_asset_key]  # Get grass positions for the biome
                              )
