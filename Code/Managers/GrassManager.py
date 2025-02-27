from Code.Variables.SettingVariables import *
from Code.Individuals.Grass import *


class GrassManager:
          def __init__(self, game):
                    self.game = game
                    self.ga = GrassAssets(self)
                    self.game.methods.set_attributes(self, GRASS)

                    self.grass_id = 0
                    self.grass_cache = {}
                    self.shadow_cache = {}
                    self.formats = {}
                    self.grass_tiles = {}

                    self.count = 0
                    self.rendered_shadows = False

          def get_format(self, format_id, data, tile_id):
                    if format_id not in self.formats:
                              self.formats[format_id] = {'count': 1, 'data': [(tile_id, data)]}
                    elif self.formats[format_id]['count'] >= self.max_unique:
                              return deepcopy(random.choice(self.formats[format_id]['data']))
                    else:
                              self.formats[format_id]['count'] += 1
                              self.formats[format_id]['data'].append((tile_id, data))
                    return tile_id, data

          def place_tile(self, location, density, grass_options):
                    location_tuple = tuple(location)
                    if location_tuple not in self.grass_tiles:
                              tile_position = (location[0] * self.tile_size, location[1] * self.tile_size)
                              self.grass_tiles[location_tuple] = GrassTile(self.game, self.tile_size, tile_position,
                                                                           density, grass_options, self.ga, self)

          def apply_force(self, location, radius, dropoff):
                    location = tuple(map(int, location))
                    grid_pos = tuple(int(loc // self.tile_size) for loc in location)
                    tile_range = math.ceil((radius + dropoff) / self.tile_size)

                    for y in range(-tile_range, tile_range + 1):
                              for x in range(-tile_range, tile_range + 1):
                                        pos = (grid_pos[0] + x, grid_pos[1] + y)
                                        if pos in self.grass_tiles:
                                                  self.grass_tiles[pos].apply_force(location, radius, dropoff)

          def draw(self):
                    self.count += 1
                    if not self.rendered_shadows and self.count > 1:
                              self.draw_shadows()
                              self.rendered_shadows = True

                    surf = self.game.displayS
                    offset = self.game.cameraM.rect.topleft

                    visible_tile_range = (
                              int(surf.get_width() // self.tile_size) + 1,
                              int(surf.get_height() // self.tile_size) + 2
                    )
                    base_pos = tuple(int(off // self.tile_size) for off in offset)

                    render_list = [
                              (base_pos[0] + x, base_pos[1] + y)
                              for y in range(visible_tile_range[1])
                              for x in range(visible_tile_range[0])
                              if (base_pos[0] + x, base_pos[1] + y) in self.grass_tiles
                    ]

                    return [self.grass_tiles[pos] for pos in render_list]

          def draw_shadows(self):
                    shadow_offset = (-self.shadow_shift[0], -self.shadow_shift[1])
                    for grass_tile in self.grass_tiles.values():
                              grass_tile.render_shadow(self.game.tilemapM.cached_surface, offset=shadow_offset)


class GrassAssets:
          def __init__(self, gm):
                    self.gm = gm
                    self.game = self.gm.game
                    self.blades = [
                              image
                              for key in GRASS["positions"].keys()
                              for image in self.game.assets[key]
                    ]

          def render_blade(self, surf, blade_id, location, rotation):
                    rot_img = pygame.transform.rotate(self.blades[blade_id], rotation)

                    shade = pygame.Surface(rot_img.get_size())
                    shade_amt = int(self.gm.shade_amount * (abs(rotation) / 90))
                    shade.set_alpha(shade_amt)
                    rot_img.blit(shade, (0, 0))

                    blit_pos = (location[0] - rot_img.get_width() // 2, location[1] - rot_img.get_height() // 2)
                    surf.blit(rot_img, blit_pos)
