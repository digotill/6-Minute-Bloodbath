from Code.Variables.SettingVariables import *


# the grass tile object that contains data for the blades
class GrassTile:
    def __init__(self, game, tile_size, location, amt, config, ga, gm):
        self.game = game
        self.ga = ga
        self.gm = gm
        self.pos = v2(location)
        self.size = tile_size
        self.blades = []
        self.master_rotation = 0
        self.precision = GRASS["wind_effect"][1]
        self.padding = GRASS["wind_effect"][0]
        self.inc = 90 / self.precision

        # generate blade data
        y_range = self.gm.vertical_place_range[1] - self.gm.vertical_place_range[0]
        for i in range(amt):
            new_blade = random.choice(config)

            y_pos = self.gm.vertical_place_range[0]
            if y_range:
                y_pos = random.random() * y_range + self.gm.vertical_place_range[0]

            self.blades.append([(random.random() * self.size, y_pos * self.size), new_blade,
                                random.random() * 30 - 15])

        # layer back to front
        self.blades.sort(key=lambda x: x[1])

        # get next ID
        self.base_id = self.gm.grass_id
        self.gm.grass_id += 1

        # check if the blade data needs to be overwritten with a previous layout to save RAM usage
        format_id = (amt, tuple(config))
        overwrite = self.gm.get_format(format_id, self.blades, self.base_id)
        if overwrite:
            self.blades = overwrite[1]
            self.base_id = overwrite[0]

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

        # custom_blade_data is used when the blade's current state should not be cached. all grass tiles will try to return to a cached state
        self.custom_blade_data = None

        self.update_render_data()

    # apply a force that affects each blade individually based on distance instead of the rotation of the entire tile
    def apply_force(self, force_point, force_radius, force_dropoff):
        if not self.custom_blade_data:
            self.custom_blade_data = [None] * len(self.blades)

        for i, blade in enumerate(self.blades):
            dis = math.sqrt((self.pos.x + blade[0][0] - force_point[0]) ** 2 + (
                    self.pos.y + blade[0][1] - force_point[1]) ** 2)
            if dis < force_radius:
                force = 2
            else:
                dis = max(0, dis - force_radius)
                force = 1 - min(dis / force_dropoff, 1)
            dir_ = 1 if force_point[0] > (self.pos.x + blade[0][0]) else -1
            # don't update unless force is greater
            if not self.custom_blade_data[i] or abs(
                    self.custom_blade_data[i][2] - self.blades[i][2]) <= abs(force) * 90:
                self.custom_blade_data[i] = [blade[0], blade[1], blade[2] + dir_ * force * 90]

    # update the identifier used to find a valid cached image
    def update_render_data(self):
        self.render_data = (self.base_id, self.master_rotation)
        self.true_rotation = self.inc * self.master_rotation

    # set new master tile rotation
    def set_rotation(self, rotation):
        self.master_rotation = rotation
        self.update_render_data()

    # render the tile's image based on its current state and return the data
    def render_tile(self, render_shadow=False):
        # make a new padded surface (to fit blades spilling out of the tile)
        surf = pygame.Surface((self.size + self.padding * 2, self.size + self.padding * 2))
        surf.set_colorkey((0, 0, 0))

        # use custom_blade_data if it's active (uncached). otherwise use the base data (cached).
        if self.custom_blade_data:
            blades = self.custom_blade_data
        else:
            blades = self.blades

        # render the shadows of each blade if applicable
        if render_shadow:
            shadow_surf = pygame.Surface(surf.get_size())
            shadow_surf.set_colorkey((0, 0, 0))
            for blade in self.blades:
                pygame.draw.circle(shadow_surf, (0, 0, 1),
                                   (blade[0][0] + self.padding, blade[0][1] + self.padding),
                                   self.gm.shadow_radius)
            shadow_surf.set_alpha(self.gm.shadow_strength)

        # render each blade using the asset manager
        for blade in blades:
            self.ga.render_blade(surf, blade[1],
                                 (blade[0][0] + self.padding, blade[0][1] + self.padding),
                                 max(-90, min(90, blade[2] + self.true_rotation)))

        # return surf and shadow_surf if applicable
        if render_shadow:
            return surf, shadow_surf
        else:
            return surf

    # draw the shadow image for the tile
    def render_shadow(self, surf, offset=(0, 0)):
        if self.gm.shadow_radius and (self.base_id in self.gm.shadow_cache):
            surf.blit(self.gm.shadow_cache[self.base_id], (
                self.pos.x - offset[0] - self.padding, self.pos.y - offset[1] - self.padding))

    # draw the grass itself
    def render(self, surf, dt, offset=(0, 0)):
        # render a new grass tile image if using custom uncached data otherwise use cached data if possible
        if self.custom_blade_data:
            surf.blit(self.render_tile(), (
                self.pos.x - offset[0] - self.padding, self.pos.y - offset[1] - self.padding))

        else:
            # check if a new cached image needs to be generated and use the cached data if not (also cache shadow if necessary)
            if (self.render_data not in self.gm.grass_cache) and (
                    self.gm.shadow_radius and (self.base_id not in self.gm.shadow_cache)):
                grass_img, shadow_img = self.render_tile(render_shadow=True)
                self.gm.grass_cache[self.render_data] = grass_img
                self.gm.shadow_cache[self.base_id] = shadow_img
            elif self.render_data not in self.gm.grass_cache:
                self.gm.grass_cache[self.render_data] = self.render_tile()

            # render image from the cache
            surf.blit(self.gm.grass_cache[self.render_data], (
                self.pos.x - offset[0] - self.padding, self.pos.y - offset[1] - self.padding))

        # attempt to move blades back to their base position
        if self.custom_blade_data:
            matching = True
            for i, blade in enumerate(self.custom_blade_data):
                blade[2] = self.normalize(blade[2], self.gm.stiffness * dt, self.blades[i][2])
                if blade[2] != self.blades[i][2]:
                    matching = False
            # mark the data as non-custom once in base position so the cache can be used
            if matching:
                self.custom_blade_data = None

    def draw(self, surface=None):
        if surface is None:
            surface = self.game.displayS
        self.render(surface, self.game.dt, offset=self.game.cameraM.rect.topleft)
        self.set_rotation(GRASS["Rot_Function"](self.pos.x, self.pos.y, self.game.game_time))

    @staticmethod
    def normalize(val, amt, target):
        if val > target + amt:
            val -= amt
        elif val < target - amt:
            val += amt
        else:
            val = target
        return val
