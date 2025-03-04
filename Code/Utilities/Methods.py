import functools, math, os, random, pygame


class Methods:
    def __init__(self):
        # Configuration for buttons and sliders
        self.button_config = {
            "button": {"res": (64, 24), "axis": "y", "axisl": "max", "text_pos": "center", "speed": 1500,
                       "base_colour": (255, 255, 255), "distance_factor": 0.3,
                       "hovering_colour": (131, 64, 44), "hover_slide": True, "hover_offset": 15, "hover_speed": 30,
                       "on": False, "active": False, "current_hover_offset": 0,
                       },
            "slider": {"res": (64, 24), "axis": "y", "axisl": "max", "text_pos": "right", "speed": 1500,
                       "base_colour": (255, 255, 255), "distance_factor": 0.3,
                       "circle_base_colour": (131, 64, 44), "circle_hovering_colour": (38, 27, 46),
                       "hover_slide": False, "hover_offset": 15, "hover_speed": 30,
                       "line_thickness": 2, "line_colour": (131, 64, 44), "on": False, "active": False,
                       "current_hover_offset": 0,
                       },
            "card": {"res": (44, 67), "axis": "y", "axisl": "min", "speed": 1500, "distance_factor": 0.3,
                     "hover_slide": True, "hover_offset": 15, "hover_speed": 30,
                     "active": False, "current_hover_offset": 0}}
        self.enemy_config = {"stopping_range": 25 ** 2, "steering_strength": 0.4, "friction": 0.2,
                             "animation_speed": 15, "hit_cooldown": 0, "separation_radius": 8,
                             "separation_strength": 4, "attack_cooldown": 0.4, "knockback": 1, "hit_effect": (20, 200),
                             "spawn_blood": True}

        self.rename_files_recursive(r"C:\Users\digot\PycharmProjects\Survivor-Coursework-Project\Assets")

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

    @staticmethod
    def get_transparent_image(image, alpha):
        # Create a transparent version of the given image
        transparent_image = image.copy()
        transparent_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        return transparent_image

    @staticmethod
    def get_shadow_image(self, image):
        # Create a shadow image for the given image
        shadow_image = self.game.assets["shadow"].copy()
        return pygame.transform.scale(shadow_image, (image.width, shadow_image.height))

    @staticmethod
    def get_shadow_image2(self, width):
        # Create a shadow image for the given image
        shadow_image = self.game.assets["shadow"].copy()
        return pygame.transform.scale(shadow_image, (width, shadow_image.height))

    @staticmethod
    def get_image_outline(img, outline_color=(255, 255, 255)):
        # Create an outline for the given image
        mask = pygame.mask.from_surface(img)
        mask_outline = mask.outline()
        mask_surf = pygame.Surface(img.get_size(), pygame.SRCALPHA)

        for x, y in mask_outline:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                mask_surf.set_at((x + dx, y + dy), outline_color)

        outlined_img = img.copy()
        outlined_img.blit(mask_surf, (0, 0))
        outlined_img.blit(img)
        return outlined_img

    @staticmethod
    def get_image_mask(image):
        # Create a mask for the given image
        mask = pygame.mask.from_surface(image)
        image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        image.set_colorkey((0, 0, 0))
        return mask.to_surface(image)

    @staticmethod
    def lerp(start, end, amount):
        # Linear interpolation between start and end values
        return start + (end - start) * amount

    @staticmethod
    def normalize(val, amt, target):
        # Normalize a value towards a target
        if val > target + amt:
            val -= amt
        elif val < target - amt:
            val += amt
        else:
            val = target
        return val

    @staticmethod
    def change(number, diff):
        # Add a random change to a number within a range
        return number + random.uniform(-diff, diff)

    @staticmethod
    def lookup_colour(colour):
        # Look up and print colors containing the given colour name
        color_list = [(c, v) for c, v in pygame.color.THECOLORS.items() if colour in c]
        for colour in color_list: print(colour)

    @staticmethod
    def rename_files_recursive(directory):
        # Rename image files in a directory and its subdirectories
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

        # First pass: remove "_1", "_2", etc. from the end of filenames
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(image_extensions):
                    base, ext = os.path.splitext(filename)
                    if base.split('_')[-1].isdigit():
                        new_base = '_'.join(base.split('_')[:-1])
                        new_filename = f"{new_base}{ext}"
                        old_path = os.path.join(root, filename)
                        new_path = os.path.join(root, new_filename)
                        try:
                            os.rename(old_path, new_path)
                            print(f"Removed number suffix: {old_path} -> {new_path}")
                        except OSError as e:
                            print(f"Error removing number suffix from {old_path}: {e}")

        # Second pass: rename files (lowercase and replace spaces with underscores)
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(image_extensions):
                    old_path = os.path.join(root, filename)
                    new_filename = filename.lower().replace(' ', '_')

                    if filename != new_filename:
                        new_path = os.path.join(root, new_filename)

                        try:
                            if os.path.exists(new_path):
                                # If the file already exists, find a unique name
                                base, ext = os.path.splitext(new_filename)
                                counter = 1
                                while os.path.exists(new_path):
                                    new_filename = f"{base}_{counter}{ext}"
                                    new_path = os.path.join(root, new_filename)
                                    counter += 1

                            os.rename(old_path, new_path)
                            print(f"Renamed: {old_path} -> {new_path}")
                        except OSError as e:
                            print(f"Error renaming {old_path}: {e}")

    @staticmethod
    def get_unique_filename(path):
        # Generate a unique filename by appending a number if necessary
        root, ext = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = f"{root}_{counter}{ext}"
            counter += 1
        return path

    def create_button(self, text_input, pos, image, dictionary2=None):
        # Create a button configuration dictionary
        value = {
            "text_input": text_input,
            "pos": pos,
            "image": image,
        }
        value.update(self.button_config["button"])
        if dictionary2 is not None:
            value.update(dictionary2)
        return value

    def create_slider(self, pos, text_input, min_value, max_value, initial_value, image, dictionary2=None):
        # Create a slider configuration dictionary
        value = {
            "text_input": text_input,
            "pos": pos,
            "min_value": min_value,
            "max_value": max_value,
            "value": initial_value,
            "image": image,
        }
        value.update(self.button_config["slider"])
        if dictionary2 is not None:
            value.update(dictionary2)
        return value

    def create_card(self, dictionary2=None):
        # Create a slider configuration dictionary
        value = {
            "damage": 0,
            "health": 0,
            "pierce": 0,
            "attack_speed": 0,
            "spread": 0,
            "shots": 0,
            "knockbacks": 0,
        }
        value.update(self.button_config["card"])
        if dictionary2 is not None:
            value.update(dictionary2)
        return value

    def create_enemy(self, name, res, health, vel, damage, attack_range, armour, xp_chances, has_shadow, shadow_width,
                     dictionary2=None):
        # Create a slider configuration dictionary
        value = {
            "name": name,
            "res": res,
            "health": health,
            "vel": vel,
            "damage": damage,
            "attack_range": attack_range,
            "armour": armour,
            "xp_chances": xp_chances,
            "has_shadow": has_shadow,
            "shadow_width": shadow_width,
        }
        value.update(self.enemy_config)
        if dictionary2 is not None:
            value.update(dictionary2)
        return value

    @staticmethod
    def set_attributes(object1, attributes):
        # Set multiple attributes of an object at once
        for key, value in attributes.items():
            setattr(object1, key, value)

    @staticmethod
    def set_rect(object1):
        # Set the rect attribute of an object based on its position and resolution
        object1.rect = pygame.Rect(object1.pos.x - object1.res[0] / 2, object1.pos.y - object1.res[1] / 2,
                                   object1.res[0], object1.res[1])
