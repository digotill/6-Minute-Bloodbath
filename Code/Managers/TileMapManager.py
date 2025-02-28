from Code.DataStructures.HashMap import *


class Tile:
          def __init__(self, game, tile_type, position):
                    self.game = game  # Reference to the main game object
                    self.tile_type = tile_type  # Type of the tile (e.g., 'grass', 'water', etc.)
                    self.position = v2(position)  # Position of the tile in the game world
                    self.size = GENERAL["hash_maps"][2]  # Size of the tile in pixels
                    self.rect = pygame.Rect(self.position.x, self.position.y, self.size - 1, self.size - 1)  # Rectangular area of the tile
                    if tile_type in TILES["animated_tiles"] and tile_type != "padding":
                              self.images = self.game.assets[tile_type]  # List of images for this tile type
                    elif tile_type != "padding":
                              self.images = [random.choice(self.game.assets[tile_type])]  # List of images for this tile type
                    self.transition = False  # Flag to indicate if this is a transition tile
                    self.frame = 0  # Current frame for animated tiles

          def draw(self, surface, offset, frame):
                    draw_position = self.position - offset  # Calculate draw position
                    surface.blit(self.images[int(frame % len(self.images))], draw_position)  # Draw tile


class TileMapManager:
          def __init__(self, game):
                    self.game = game

                    self.tile_size = GENERAL["hash_maps"][2]  # Set tile size
                    self.grid = HashMap(game, self.tile_size)  # Main tile grid
                    self.grid2 = HashMap(game, self.tile_size)  # Secondary tile grid (for transitions)
                    self.grid3 = HashMap(game, self.tile_size)  # Tertiary tile grid (for padding)
                    self.width = GAMESIZE[0] // self.tile_size + 1  # Calculate map width in tiles
                    self.height = GAMESIZE[1] // self.tile_size + 1  # Calculate map height in tiles

                    self.animation_speed = TILES["animation_speed"]  # Set animation speed for tiles
                    self.frames = {tile_type: 0 for tile_type in TILES["animated_tiles"]}  # Initialize animation frames
                    self.perlin_noise = PerlinNoise(MAP["tiles_map"][1], random.randint(0, 100000))  # Create Perlin noise generator

                    self.biome_map, self.density_map = self._generate_maps()  # Generate biome and density maps

                    self.terrain_generator()  # Generate initial terrain

                    self.cached_surface = None  # Initialize cached surface
                    self.create_cached_surface()  # Create cached surface for efficient rendering
                    self.padding_generator()  # Generate padding tiles

                    self.grid.rebuild()  # Rebuild main grid
                    self.grid2.rebuild()  # Rebuild secondary grid

          def _generate_maps(self):
                    biome_noise = PerlinNoise(octaves=MAP["biomes_map"][1], seed=random.randint(0, 100000))  # Create biome noise
                    density_noise = PerlinNoise(octaves=MAP["biomes_density_map"][1], seed=random.randint(0, 100000))  # Create density noise
                    return (
                              self._generate_noise_map(biome_noise, MAP["biomes_map"][0]),  # Generate biome map
                              self._generate_noise_map(density_noise, MAP["biomes_density_map"][0])  # Generate density map
                    )

          @staticmethod
          def _generate_noise_map(noise, scale):
                    size = GENERAL["enviroment_density"][1]  # Get environment density size
                    width, height = GAMESIZE[0] // size + 1, GAMESIZE[1] // size + 1  # Calculate map dimensions
                    noise_map = [[noise([i * scale, j * scale]) for j in range(width)] for i in range(height)]  # Generate noise map
                    return (np.array(noise_map) + 1) / 2  # Normalize noise values to [0, 1]

          def create_cached_surface(self):
                    # Calculate the size of the entire map
                    all_tiles = list(self.grid.items) + list(self.grid2.items)  # Combine tiles from both grids

                    min_x = min(tile.position.x for tile in all_tiles)  # Find minimum x coordinate
                    min_y = min(tile.position.y for tile in all_tiles)  # Find minimum y coordinate
                    max_x = max(tile.position.x + self.tile_size for tile in all_tiles)  # Find maximum x coordinate
                    max_y = max(tile.position.y + self.tile_size for tile in all_tiles)  # Find maximum y coordinate

                    width = int(max_x - min_x)  # Calculate width of cached surface
                    height = int(max_y - min_y)  # Calculate height of cached surface

                    # Create a surface big enough to hold the entire map
                    self.cached_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create cached surface
                    self.cache_offset = pygame.math.Vector2(min_x, min_y)  # Set cache offset

                    # Draw all tiles to the cached surface
                    for grid in [self.grid, self.grid2]:  # Iterate through both grids
                              for tile in grid.items:  # Draw each tile
                                        draw_position = (int(tile.position.x - self.cache_offset.x),
                                                         int(tile.position.y - self.cache_offset.y))
                                        if tile.images:
                                                  self.cached_surface.blit(tile.images[0], draw_position)

                    # For animated tiles, we'll need to keep track of them separately
                    self.animated_tiles = [tile for tile in all_tiles
                                           if tile.tile_type in TILES["animated_tiles"]]  # Store animated tiles

          def draw(self):
                    if not self.game.changing_settings:  # Update animation frames if not changing settings
                              for tile_type in self.frames:
                                        self.frames[tile_type] += self.game.dt * self.animation_speed
                    camera_rect = self.game.cameraM.rect  # Get camera offset

                    # Draw the cached surface
                    draw_position = (int(self.cache_offset.x - camera_rect.left),
                                     int(self.cache_offset.y - camera_rect.top))
                    self.game.displayS.blit(self.cached_surface, draw_position)  # Draw cached surface

          def add_tile(self, tile_type, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)  # Convert grid to pixel position
                    tile = Tile(self.game, tile_type, pixel_position)  # Create new tile
                    self.grid.insert(tile)  # Insert tile into grid

          def get_tile_type(self, x, y):
                    noise_value = self.perlin_noise([x * MAP["tiles_map"][0], y * MAP["tiles_map"][0]])  # Get noise value
                    for tile in TILES["Tile_Ranges"].keys():  # Determine tile type based on noise value
                              if noise_value < TILES["Tile_Ranges"][tile]:
                                        return tile

          def tile_collision(self, rect, *tile_types):
                    for tile in self.grid.query(rect):  # Check for collision with specified tile types
                              for tile_type in tile_types:
                                        if tile.tile_type == tile_type:
                                                  return True
                    return False

          def get(self, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)  # Convert grid to pixel position
                    tile = self.grid.grid.get(grid_position, None)  # Get tile from grid
                    if isinstance(tile, list) and tile:  # Handle case where multiple tiles occupy same position
                              for i in tile:
                                        if i.rect.topleft == pixel_position:
                                                  return i
                    return None

          def apply_transition_tiles(self, transition_array, count=0):
                    changes = 0
                    for tile in self.grid.items:
                              if tile.tile_type == transition_array[1]:
                                        grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)
                                        neighbours = [self.get((grid_x + dx, grid_y + dy)) for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]]  # Get neighboring tiles (top, bottom, right, left)

                                        def neighbor_value(n):
                                                  # Determine the value for each neighbor tile
                                                  if not n or n.tile_type != transition_array[1]:
                                                            return '0'  # Different tile type or no tile
                                                  return '2' if count > 2 and n.transition else '1'  # Transitioned or not

                                        def change_tile(change):
                                                  # Change the current tile to the transition tile type
                                                  grid2tile = self.get((grid_x, grid_y))
                                                  if grid2tile and grid2tile in self.grid2.items:
                                                            self.grid2.remove(grid2tile)
                                                  tile.images = self.game.assets[transition_array[0]]
                                                  tile.tile_type = transition_array[0]
                                                  return change + 1

                                        neighbours_string = ''.join(map(neighbor_value, neighbours))  # Create string representation of neighbors
                                        string = self.get_surrounding_tiles_string(tile)  # Get string representation of all surrounding tiles
                                        corner_string = self.check_corners(tile)  # Check corner configurations
                                        new_string = self.find_if_corner(neighbours_string, string)  # Determine if it's a corner case

                                        # Apply transition rules based on neighbor configurations and iteration count
                                        if neighbours_string in ["1100", "0011", "0000", "1000", "0100", "0010", "0001"] and count == 0:
                                                  changes = change_tile(changes)
                                        elif self.count_surrounding_tiles(tile) == 4 and count == 0 and string in ["11100100", "00111001", "01001110", "10010011", "10100100", "00101001", "01001010", "10010010"]:
                                                  changes = change_tile(changes)
                                        elif self.count_surrounding_tiles(tile) == 4 and count == 1 and ("101" in string or string in ["1100010"]):
                                                  changes = change_tile(changes)
                                        elif neighbours_string in ["1100", "0011", "0000", "1000", "0100", "0010", "0001"] and count == 1:
                                                  changes = change_tile(changes)
                                        elif neighbours_string in ["1101", "1011", "0111", "1110"] and count == 1:
                                                  self.add_grid2_tile(tile, grid_x, grid_y, transition_array, new_string)
                                        elif neighbours_string in ["0101", "0110", "1001", "1010"] and count == 2:
                                                  self.add_grid2_tile(tile, grid_x, grid_y, transition_array, neighbours_string)
                                        elif neighbours_string in ["2121", "2112", "1221", "1212", "1222", "2122", "2212", "2221", "2222"] and count == 3 and corner_string is not True:
                                                  self.add_grid2_tile(tile, grid_x, grid_y, transition_array, corner_string)
                                        elif self.count_surrounding_tiles(tile) == 3 and count == 4 and string in ["01011011", "01101101", "10110101", "11010110"]:
                                                  changes = change_tile(changes)
                                        elif count == 4 and tile.tile_type == transition_array[0]:
                                                  grid2tile = self.get((grid_x, grid_y))
                                                  if grid2tile and grid2tile in self.grid2.items:
                                                            self.grid2.remove(grid2tile)

                    # Recursively apply transitions if changes were made and count is less than 5
                    if changes == 0:
                              count += 1
                    if count < 5:
                              self.apply_transition_tiles(transition_array, count)

          @staticmethod
          def find_if_corner(string1, string2):
                    if string2 in ["00111011", "01111011", "10111001", "10111101"]:
                              return "0110"
                    elif string2 in ["01101110", "01101111", "11001110", "11011110"]:
                              return "0101"
                    elif string2 in ["10110011", "10110111", "10011011", "11011011"]:
                              return "1001"
                    elif string2 in ["11100110", "11110110", "11101100", "11101101"]:
                              return "1010"
                    else:
                              return string1

          def get_surrounding_tiles_string(self, tile):
                    grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)

                    # Define all 8 directions (including diagonals) in clockwise order
                    directions = [
                              (0, -1),  # Top
                              (1, -1),  # Top-Right
                              (1, 0),  # Right
                              (1, 1),  # Bottom-Right
                              (0, 1),  # Bottom
                              (-1, 1),  # Bottom-Left
                              (-1, 0),  # Left
                              (-1, -1)  # Top-Left
                    ]

                    surrounding_tiles = ""

                    for dx, dy in directions:
                              neighbor = self.get((grid_x + dx, grid_y + dy))
                              if neighbor and neighbor.tile_type == tile.tile_type:
                                        surrounding_tiles += "1"
                              else:
                                        surrounding_tiles += "0"

                    return surrounding_tiles

          def check_corners(self, tile):
                    grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)
                    neighbours = [self.get((grid_x + dx, grid_y + dy)) for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]]
                    return_data = []
                    for neighbour in neighbours:
                              if neighbour is None or neighbour.tile_type != tile.tile_type:
                                        return_data.append(["2112", "2121", "1212", "1221"][neighbours.index(neighbour)])
                    if len(return_data) == 0:
                              return True
                    elif len(return_data) == 1:
                              return return_data[0]
                    elif "2112" in return_data:
                              return "1"
                    else:
                              return "2"

          def count_adjacent_tiles(self, tile):
                    grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)

                    # Define the four adjacent directions
                    directions = [
                              (0, -1),  # Top
                              (-1, 0),  # Left
                              (1, 0),  # Right
                              (0, 1)  # Bottom
                    ]

                    count = 0
                    for dx, dy in directions:
                              neighbor = self.get((grid_x + dx, grid_y + dy))
                              if neighbor and neighbor.tile_type == tile.tile_type:
                                        count += 1

                    return count

          def count_surrounding_tiles(self, tile):
                    grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)

                    # Define all 8 directions (including diagonals)
                    directions = [
                              (-1, -1), (0, -1), (1, -1),
                              (-1, 0), (1, 0),
                              (-1, 1), (0, 1), (1, 1)
                    ]

                    tile_count = 0

                    for dx, dy in directions:
                              neighbor = self.get((grid_x + dx, grid_y + dy))
                              if neighbor is None or neighbor.tile_type != tile.tile_type:
                                        tile_count += 1

                    return tile_count

          def count_corners(self, tile):
                    grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)

                    # Define the four corner directions
                    directions = [
                              (-1, -1),  # Top-Left
                              (1, -1),  # Top-Right
                              (-1, 1),  # Bottom-Left
                              (1, 1)  # Bottom-Right
                    ]

                    count = 0
                    for dx, dy in directions:
                              neighbor = self.get((grid_x + dx, grid_y + dy))
                              if neighbor and neighbor.tile_type == tile.tile_type:
                                        count += 1

                    return count

          def add_grid2_tile(self, tile, grid_x, grid_y, transition_array, index):
                    # Calculate the pixel position from the grid coordinates
                    pixel_position = (grid_x * self.tile_size, grid_y * self.tile_size)

                    # Check if there's already a tile in grid2 at this position
                    grid2tile = self.get((grid_x, grid_y))
                    if grid2tile and grid2tile in self.grid2.items:
                              # If a tile exists, remove it from grid2
                              self.grid2.remove(grid2tile)

                    # Create a new transition tile
                    new_tile = Tile(self.game, transition_array[0], pixel_position)

                    # Set the image for the new tile based on the transition type and index
                    # The index determines which specific transition image to use
                    new_tile.images = self.game.assets[transition_array[0][:6] + "tileset"][index]

                    # Mark the original tile as transitioned
                    tile.transition = True

                    # Insert the new transition tile into grid2
                    self.grid2.insert(new_tile)

          def terrain_generator(self):
                    for x in range(self.width):  # Generate initial terrain
                              for y in range(self.height):
                                        tile_type = self.get_tile_type(x, y)
                                        self.add_tile(tile_type, (x, y))

                    for array in TILES["transitions"]: self.apply_transition_tiles(array)  # Apply transition tiles

          def get_biome_at(self, x, y):
                    # Ensure x and y are within the bounds of the biome_map
                    y = min(y, self.biome_map.shape[0] - 1)  # Clamp y coordinate
                    x = min(x, self.biome_map.shape[1] - 1)  # Clamp x coordinate

                    biome_value = self.biome_map[y][x]  # Get biome value from map
                    for biome, (chance, _, density) in BIOMES.items():  # Determine biome based on value
                              if biome_value < chance:
                                        return biome
                    return list(Biomes_Config.keys())[-1]  # Return the last biome if no match found

          def draw_padding(self, x, y, images):
                    padding_image = random.choice(images)  # Choose random padding image

                    # Create a new tile for the padding
                    padding_tile = Tile(self.game, 'padding', (x, y))  # Create padding tile
                    padding_tile.images = [padding_image]

                    # Insert the padding tile into grid3
                    self.grid3.insert(padding_tile)  # Insert padding tile into tertiary grid

                    # Update the cached surface with the new padding
                    draw_position = (int(x - self.cache_offset.x), int(y - self.cache_offset.y))
                    self.cached_surface.blit(padding_image, draw_position)  # Draw padding on cached surface

          def padding_generator(self):
                    height, width = self.biome_map.shape
                    for y in range(height):
                              for x in range(width):
                                        tile = self.get((x, y))
                                        if tile and tile.tile_type == 'grass_tile' and not tile.transition:
                                                  biome = self.get_biome_at(x, y)  # Get the biome at the current position
                                                  _, _, padding_density = BIOMES[biome]  # Get biome properties

                                                  density_value = self.density_map[y][x]  # Get density value from density map
                                                  normalized_density = (density_value + 1) / 2  # Normalize density to [0, 1]
                                                  combined_density = padding_density * normalized_density  # Combine with biome-specific density

                                                  if random.random() < combined_density:  # Randomly decide to add padding based on combined density
                                                            padding_images = self.game.assets[biome + '_padding']  # Get padding images for the biome
                                                            self.draw_padding(x * self.tile_size, y * self.tile_size, padding_images)  # Draw padding
