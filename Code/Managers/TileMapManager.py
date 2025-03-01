from Code.DataStructures.HashMap import HashMap
from Code.Utilities import v2, PerlinNoise, GENERAL, GAMESIZE, TILES, MAP, BIOMES
from Code.Assets import Assets # Assuming a centralized asset manager
import pygame
import random
import numpy as np
from typing import List, Tuple, Optional, Dict

# Constants for clarity and maintainability
TILE_GRID_KEYS = {"main": "main", "transition": "transition", "padding": "padding"}

class Tile:
 """Represents a single tile in the game world."""
 def __init__(self, game, tile_type: str, position: Tuple[int, int], size: int):
 self.game = game
 self.tile_type = tile_type
 self.position = v2(position)
 self.size = size
 self.rect = pygame.Rect(self.position.x, self.position.y, size, size)
 self.transition = False
 self.frame = 0

 # Use centralized asset manager
 assets = Assets.get_instance()
 if tile_type in TILES["animated_tiles"] and tile_type != "padding":
 self.images = assets.get_images(tile_type)
 elif tile_type != "padding":
 self.images = [random.choice(assets.get_images(tile_type))]
 else:
 self.images = []

 def draw(self, surface: pygame.Surface, offset: v2, frame: int) -> None:
 """Draw the tile on the given surface with an offset."""
 if self.images:
 draw_position = self.position - offset
 surface.blit(self.images[int(frame % len(self.images))], (draw_position.x, draw_position.y))


class TileMapManager:
 """Manages the tile map, including generation, rendering, and transitions."""
 def __init__(self, game, tile_size: int = GENERAL["hash_maps"][2]):
 self.game = game
 self.tile_size = tile_size
 self.width = GAMESIZE[0] // self.tile_size + 1
 self.height = GAMESIZE[1] // self.tile_size + 1
 self.animation_speed = TILES["animation_speed"]
 self.frames: Dict[str, int] = {tile_type: 0 for tile_type in TILES["animated_tiles"]}

 # Use a seeded random generator for reproducibility
 self.rng = random.Random(random.randint(0, 100000))
 self.perlin_noise = PerlinNoise(MAP["tiles_map"][1], self.rng.randint(0, 100000))
 self.biome_map, self.density_map = self._generate_maps()

 # Unified grid management
 self.tile_grids = {
 TILE_GRID_KEYS["main"]: HashMap(game, self.tile_size),
 TILE_GRID_KEYS["transition"]: HashMap(game, self.tile_size),
 TILE_GRID_KEYS["padding"]: HashMap(game, self.tile_size)
 }

 self.terrain_generator()
 self.padding_generator()
 self._build_cached_surface()

 def _generate_maps(self) -> Tuple[np.ndarray, np.ndarray]:
 """Generate biome and density maps using Perlin noise."""
 biome_noise = PerlinNoise(octaves=MAP["biomes_map"][1], seed=self.rng.randint(0, 100000))
 density_noise = PerlinNoise(octaves=MAP["biomes_density_map"][1], seed=self.rng.randint(0, 100000))
 biome_map = self._generate_noise_map(biome_noise, MAP["biomes_map"][0])
 density_map = self._generate_noise_map(density_noise, MAP["biomes_density_map"][0])
 return biome_map, density_map

 def _generate_noise_map(self, noise: PerlinNoise, scale: float) -> np.ndarray:
 """Generate a normalized noise map for terrain or biome generation."""
 size = GENERAL["enviroment_density"][1]
 width, height = GAMESIZE[0] // size + 1, GAMESIZE[1] // size + 1
 noise_map = np.array([[noise([i * scale, j * scale]) for j in range(width)] for i in range(height)])
 return (noise_map + 1) / 2 # Normalize to [0, 1]

 def _build_cached_surface(self) -> None:
 """Build a cached surface for static tiles to optimize rendering."""
 all_tiles = self._get_all_tiles()
 if not all_tiles:
 self.cached_surface = None
 return

 min_x = min(tile.position.x for tile in all_tiles)
 min_y = min(tile.position.y for tile in all_tiles)
 max_x = max(tile.position.x + self.tile_size for tile in all_tiles)
 max_y = max(tile.position.y + self.tile_size for tile in all_tiles)

 width, height = int(max_x - min_x), int(max_y - min_y)
 self.cached_surface = pygame.Surface((width, height), pygame.SRCALPHA)
 self.cache_offset = v2(min_x, min_y)

 for grid_key in TILE_GRID_KEYS.values():
 for tile in self.tile_grids[grid_key].items:
 if tile.images:
 draw_pos = (tile.position.x - self.cache_offset.x, tile.position.y - self.cache_offset.y)
 self.cached_surface.blit(tile.images[0], draw_pos)

 def _get_all_tiles(self) -> List[Tile]:
 """Retrieve all tiles across all grids."""
 return [tile for grid in self.tile_grids.values() for tile in grid.items]

 def draw(self) -> None:
 """Render the tile map to the game display."""
 if not self.game.changing_settings:
 for tile_type in self.frames:
 self.frames[tile_type] += self.game.dt * self.animation_speed

 if self.cached_surface:
 camera_rect = self.game.cameraM.rect
 draw_pos = (self.cache_offset.x - camera_rect.left, self.cache_offset.y - camera_rect.top)
 self.game.displayS.blit(self.cached_surface, draw_pos)

 def add_tile(self, tile_type: str, grid_position: Tuple[int, int], grid_key: str = TILE_GRID_KEYS["main"]) -> None:
 """Add a tile to the specified grid."""
 pixel_pos = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
 tile = Tile(self.game, tile_type, pixel_pos, self.tile_size)
 self.tile_grids[grid_key].insert(tile)

 def get_tile_type(self, x: int, y: int) -> str:
 """Determine tile type based on Perlin noise value."""
 noise_value = self.perlin_noise([x * MAP["tiles_map"][0], y * MAP["tiles_map"][0]])
 for tile, threshold in TILES["Tile_Ranges"].items():
 if noise_value < threshold:
 return tile
 return list(TILES["Tile_Ranges"].keys())[-1]

 def tile_collision(self, rect: pygame.Rect, *tile_types: str) -> bool:
 """Check for collision with specified tile types across all grids."""
 for grid_key in TILE_GRID_KEYS.values():
 for tile in self.tile_grids[grid_key].query(rect):
 if tile.tile_type in tile_types:
 return True
 return False

 def get(self, grid_position: Tuple[int, int], grid_key: str = TILE_GRID_KEYS["main"]) -> Optional[Tile]:
 """Retrieve a tile from the specified grid at the given position."""
 pixel_pos = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
 tile = self.tile_grids[grid_key].grid.get(grid_position, None)
 if isinstance(tile, list):
 for t in tile:
 if t.rect.topleft == pixel_pos:
 return t
 return tile

 def apply_transition_tiles(self, transition_array: List[str]) -> None:
 """Apply transition tiles iteratively to avoid recursion overhead."""
 max_iterations = 5
 for iteration in range(max_iterations):
 changes = 0
 tiles_to_process = list(self.tile_grids[TILE_GRID_KEYS["main"]].items)
 for tile in tiles_to_process:
 if tile.tile_type != transition_array[1]:
 continue

 grid_x = int(tile.position.x // self.tile_size)
 grid_y = int(tile.position.y // self.tile_size)
 neighbors = self._get_neighbors(grid_x, grid_y, TILE_GRID_KEYS["main"])
 neighbor_str = ''.join('1' if n and n.tile_type == transition_array[1] else '0' for n in neighbors)

 # Simplified transition logic (expand as needed)
 if neighbor_str in ["1100", "0011"] and iteration == 0:
 self._change_tile(tile, grid_x, grid_y, transition_array[0])
 changes += 1

 if changes == 0:
 break

 def _get_neighbors(self, x: int, y: int, grid_key: str) -> List[Optional[Tile]]:
 """Get the four adjacent tiles (top, bottom, right, left)."""
 directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
 return [self.get((x + dx, y + dy), grid_key) for dx, dy in directions]

 def _change_tile(self, tile: Tile, grid_x: int, grid_y: int, new_type: str) -> None:
 """Change a tile's type and update grids."""
 existing = self.get((grid_x, grid_y), TILE_GRID_KEYS["transition"])
 if existing and existing in self.tile_grids[TILE_GRID_KEYS["transition"]].items:
 self.tile_grids[TILE_GRID_KEYS["transition"]].remove(existing)
 tile.images = Assets.get_instance().get_images(new_type)
 tile.tile_type = new_type

 def terrain_generator(self) -> None:
 """Generate the initial terrain and apply transitions."""
 for x in range(self.width):
 for y in range(self.height):
 tile_type = self.get_tile_type(x, y)
 self.add_tile(tile_type, (x, y), TILE_GRID_KEYS["main"])
 for array in TILES["transitions"]:
 self.apply_transition_tiles(array)

 def padding_generator(self) -> None:
 """Generate padding tiles based on biome and density maps."""
 height, width = self.biome_map.shape
 assets = Assets.get_instance()
 for y in range(height):
 for x in range(width):
 tile = self.get((x, y), TILE_GRID_KEYS["main"])
 if tile and tile.tile_type == 'grass_tile' and not tile.transition:
 biome = self.get_biome_at(x, y)
 _, _, padding_density = BIOMES[biome]
 density_value = self.density_map[y][x]
 combined_density = padding_density * density_value
 if self.rng.random() < combined_density:
 padding_images = assets.get_images(biome + '_padding')
 self.add_tile('padding', (x, y), TILE_GRID_KEYS["padding"])
 # Update cached surface incrementally if needed

 def get_biome_at(self, x: int, y: int) -> str:
 """Determine the biome at a given position."""
 if y >= self.biome_map.shape[0] or x >= self.biome_map.shape[1]:
 return list(BIOMES.keys())[-1]
 biome_value = self.biome_map[y][x]
 for biome, (chance, _, _) in BIOMES.items():
 if biome_value < chance:
 return biome
 return list(BIOMES.keys())[-1]
