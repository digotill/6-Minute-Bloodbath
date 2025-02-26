from Code.Variables.ImportDependencies import *

pygame.init()

M = Methods()

WINRES = 1280, 720
RENRES = 640, 360
GAMESIZE = 4000, 4000

DISPLAY = pygame.display.set_mode(WINRES, pygame.OPENGL | pygame.DOUBLEBUF)  # Set up the display

AM = LoadAssets()

pygame.mouse.set_visible(False)  # Set up mouse cursor and window properties
pygame.display.set_icon(AM.assets["cover"])
pygame.display.set_caption("Survivor Game")
pygame.display.toggle_fullscreen()  # Toggle fullscreen twice (to fix a display issue)
pygame.display.toggle_fullscreen()

GENERAL = {  # General game settings
          'enemies': (15, 0.5, True, 0.05, 0.1),  # max, spawn rate, spawning on, seperation, rebuild
          'brightness': (1.5, 1.5, 50),  # max, min, paused
          'sparks': (20, 0.3, 3.5, 0.1),  # friction, width, height, min_vel
          'hash_maps': (32, 48, 16, 96, 96, 32, 64, 16, 48, 16),  # Enemies, Bullets, Tilemap, Rain, Objects, Particles, Effects, XP, blood count
          'cooldowns': (0.5, 0.1, 0.6, 3),  # toggle cooldowns, value checker cooldown, choose card cooldown, upgrade text dissapear time
          'animation_speeds': (15, 20, 10, 20, 30, 15, 20),  # main menu background, transition, you died, muzzleflash, casing, blood
          "enviroment_density": (0.05, 16, 150),
          "misc": ("spas12", 100, (20, 0.5), 0.05, 0.05, 2, 5)}  # starting weapon, enemy spawn distance, screen shake on hit, text update frequancy, music fadeout, number of cards

PROGRESSION = {  # Progression settings
          0: {"canine_grey": 1}, 25: {"canine_grey": 0.8, "canine_white": 1}, 50: {"canine_grey": 0.1, "canine_white": 0.8, "canine_black": 1}, 75: {"canine_white": 0.1, "canine_black": 1}, 100: {"canine_black": 1},
          125: {"pebble": 1}, 150: {"pebble": 0.8, "golem": 1}, 175: {"pebble": 0.1, "golem": 0.8, "armoured_golem": 1}, 200: {"golem": 0.1, "armoured_golem": 1}, 225: {"armoured_golem": 1},
          250: {"mini_peka": 1}, 275: {"mini_peka": 0.8, "bat": 1}, 300: {"mini_peka": 0.1, "bat": 0.8, "skinny": 1}, 325: {"bat": 0.1, "skinny": 1}, 350: {"skinny": 1}, 380: {"nothing": 1}}

BOSSES = {  # Boss spawn settings
          100: "werewolf", 225: "titan", 350: "brain"}

VOLUMES = {  # Volume settings
          "music_volume": 1.1, "gun_shot_frequancy": 0.15, "gun_shot_volume": 0.2, "click_shot_frequancy": 0.1, "click_shot_volume": 10, "heartbeat_frequancy": 0.1, "heartbeat_volume": 200, "pausing_frequancy": 0.05, "pausing_volume": 0.15, "splatter_frequancy": 0.1, "splatter_volume": 1,
          "youdied_frequancy": 0, "youdied_volume": 1, "picked_xp_frequancy": 0.2, "picked_xp_volume": 0.1, "youwon_frequancy": 0, "youwon_volume": 1, "level_up_frequancy": 0, "level_up_volume": 1,
          "jump_frequancy": 0.1, "jump_volume": 1}

DIFFICULTY = {  # Difficulty settings    enemy speed, enemy health, enemy damage
          "easy": (0.9, 0.6, 0.5), "medium": (1, 1, 1), "hard": (1.1, 1.6, 1.7), "win_change": (1, 1.1, 1.1)}

EXPERIENCE = {  # Experience settings
          "starting_max_xp": 100, "xp_progression_rate": 1.2, "blue": 8, "orange": 15, "green": 24, "purple": 48, "light_blue": 64, "red": 86, "animation_speed": 10, "attributes": {"speed": 200, "attraction_distance": 50, "collection_distance": 10}, "gradual_increase": 600}

UI = {  # UI settings
          "ui_bars": (80, 30), "xp_bar": (240, 30), "fps_pos": (190, 10), "wins_pos": (320, 340), "tutorial_pos": (100, 180)}

CAMERA = {  # Camera settings
          'lerp_speed': 5, 'mouse_smoothing': v2(10, 10), 'window_mouse_smoothing_amount': 5, 'deadzone': 1, 'window_max_offset': 0.3, 'shake_speed': 200, 'reduced_screen_shake': 1}

GRASS = {  # Grass settings
          "tile_size": 16, "shade_amount": 100, "stiffness": 300, "max_unique": 5, "vertical_place_range": (0, 1), "wind_effect": (13, 25), "density": 0.6,
          "shadow_radius": 3, "shadow_strength": 60, "shadow_shift": (1, 2), "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 100) * 15),
          "positions": {"forest_grass": [0, 1, 2, 3, 4], "snow_grass": [5, 6, 7, 8, 9], "spring_grass": [10, 11, 12, 13, 14], "cherryblossom_grass": [15, 16, 17, 18, 19], "wasteland_grass": [20, 21, 22, 23, 24]}}

PLAYER = {  # Player settings
          'health': 20000, "res": (16, 16), 'vel': 80, "sprint_vel": 1.6, "slowed_vel": 0.5, 'damage': 30, 'acceleration': 200, "offset": 10, "hit_effect": (20, 200),
          'animation_speed': 10, "hit_cooldown": 0.4, 'stamina': 100, "stamina_consumption": 30, "stamina_recharge_rate": 10, "grass_force": 10, "slow_cooldown": 0.1,
          "friction": 0.9, "acceleration_rate": 2000, "jumping_velocity": -300, "gravity": 1000, "jump_stamina": 40, "jump_cooldown": 0.25, "jump_vel": 2}

BLOOD = {  # Blood settings
          "blood": {"name": "blood", "res": (48, 48), "speed": (1500, 30), "direction": 20, "animation_speed": 40, "vanish_time": (1, 1.5), "variety": 10}, "max_blood": 10, "blood_amount": 0.3, "blood_effect_duration": 4, "blood_on_player_hit": 20}

MAP = {  # Map generation settings
          "biomes_map": (0.004, 1), "biomes_density_map": (0.05, 4), "tiles_map": (0.2, 1), "gun_shake_map": (0.1, 2), "camera_shake_map": (0.1, 3)}

BIOMES = {  # Biome settings       chance of biome spawning, tree density, padding density
          "wasteland": (0.35, 0.7, 0.8), "spring": (0.45, 0.7, 0.8), "forest": (0.55, 0.7, 0.8), "snow": (0.6, 0.7, 0.8), "cherryblossom": (1, 0.7, 0.8), }

TILES = {  # Tile settings
          "Tile_Ranges": {"water_tile": -0.1, "grass_tile": 1}, "transitions": [["grass_tile", "water_tile"]], "animation_speed": 5, "animated_tiles": [], }

RAIN = {  # Rain effect settings
          "spawn_rate": 0.1, "amount_spawning": 5, "animation_speed": 30, "angle": 40, "vel": (800, 50), "lifetime": (0.5, 0.8)}

WEAPONS = {  # Weapon settings
          "ak47": {"vel": 1300, "spread": 4, "fire_rate": 0.15, "lifetime": 1, "lifetime_randomness": 0.2, "damage": 150, "distance": -7, "friction": 0.2, "spread_time": 2, "pierce": 2, "shots": 1, "name": "ak47", "knockback": 80, "screen_shake": 5},
          "spas12": {"vel": 1500, "spread": 15, "fire_rate": 0.9, "lifetime": 0.5, "lifetime_randomness": 0.2, "damage": 80, "distance": -7, "friction": 0.6, "spread_time": 2, "pierce": 5, "shots": 10, "name": "spas12", "knockback": 20, "screen_shake": 25},
          "m16a4": {"vel": 1600, "spread": 1, "fire_rate": 0.25, "lifetime": 1, "lifetime_randomness": 0.2, "damage": 360, "distance": -7, "friction": 0.1, "spread_time": 2, "pierce": 10, "shots": 1, "name": "m16a4", "knockback": 200, "screen_shake": 5},
          "m60e4": {"vel": 1400, "spread": 10, "fire_rate": 0.1, "lifetime": 1, "lifetime_randomness": 0.2, "damage": 250, "distance": -7, "friction": 0.4, "spread_time": 2, "pierce": 2, "shots": 1, "name": "m60e4", "knockback": 80, "screen_shake": 7}, }

BUTTONS = {  # Button settings for various game states
          "In_Game_Buttons": {
                    "quit": M.create_button("quit", v2(320, 225), AM.assets["button12"], {"axis": "y", "axisl": "max"}),
                    "return": M.create_button("return", v2(320, 180), AM.assets["button12"], {"axis": "y", "axisl": "min"}),
                    "resize": M.create_button("resize", v2(190, 90), AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "music": M.create_button("music", v2(190, 135), AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "stats": M.create_button("stats", v2(190, 180), AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "shoot": M.create_button("shoot", v2(190, 225), AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "reset": M.create_button("reset", v2(190, 270), AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "resume": M.create_button("resume", v2(190, 315), AM.assets["button12"], {"axis": "x", "axisl": "min"}), },
          "Weapon_Buttons": {
                    "ak47": M.create_button("ak47 (2 win)", v2(540, 140), AM.assets["ak47"], {"text_pos": "top", "active": True, "axisl": "max", "axis": "x", "res": AM.assets["ak47"].size, "requirement": 2}),
                    "spas12": M.create_button("spas12 (0 wins)", v2(540, 60), AM.assets["spas12"], {"text_pos": "top", "on": True, "active": True, "axisl": "max", "axis": "x", "res": AM.assets["spas12"].size, "requirement": 0}),
                    "m16a4": M.create_button("m16a4 (4 wins)", v2(540, 220), AM.assets["m16a4"], {"text_pos": "top", "active": True, "axisl": "max", "axis": "x", "res": AM.assets["m16a4"].size, "requirement": 4}),
                    "m60e4": M.create_button("m60e4 (6 wins)", v2(540, 300), AM.assets["m60e4"], {"text_pos": "top", "active": True, "axisl": "max", "axis": "x", "res": AM.assets["m60e4"].size, "requirement": 6}), },
          "Menu_Buttons": {
                    "play": M.create_button("play", v2(280, 180), AM.assets["button12"], {"active": True}),
                    "quit": M.create_button("quit", v2(360, 180), AM.assets["button12"], {"active": True}),
                    "easy": M.create_button("easy", v2(220, 30), AM.assets["button12"], {"active": True, "axisl": "min"}),
                    "medium": M.create_button("medium", v2(320, 30), AM.assets["button12"], {"on": True, "active": True, "axisl": "min"}),
                    "hard": M.create_button("hard", v2(420, 30), AM.assets["button12"], {"active": True, "axisl": "min"})},
          "Sliders": {
                    "brightness": M.create_slider(v2(450, 225), "brightness:  ", 20, 180, 100, AM.assets["button12"], {"axis": "x", "axisl": "max", "text_pos": "right"}),
                    "fps": M.create_slider(v2(450, 180), "max fps:  ", 20, 240, 60, AM.assets["button12"], {"axis": "x", "axisl": "max", "text_pos": "right"}),
                    "shake": M.create_slider(v2(450, 135), "reduced shake:  ", 0, 100, 100, AM.assets["button12"], {"axis": "x", "axisl": "max", "text_pos": "right"}),
                    "colour": M.create_slider(v2(450, 90), "colour mode:  ", 1, 100, 50, AM.assets["button12"], {"axis": "x", "axisl": "max", "text_pos": "right"}),
                    "volume": M.create_slider(v2(450, 315), "sound volume:  ", 0, 100, 50, AM.assets["button12"], {"axis": "x", "axisl": "max", "text_pos": "right"}),
                    "text_size": M.create_slider(v2(450, 270), "text size:  ", 120, 200, 120, AM.assets["button12"], {"axis": "x", "axisl": "max", "text_pos": "right"})},
          "End_Screen_Buttons": {
                    "restart": M.create_button("restart", v2(240, 270), AM.assets["button8"], {"axis": "y", "axisl": "max", "res": (92, 30)}),
                    "quit": M.create_button("quit", v2(400, 270), AM.assets["button8"], {"axis": "y", "axisl": "max", "res": (92, 30)})},
          "Won_Screen_Buttons": {
                    "restart": M.create_button("restart", v2(240, 270), AM.assets["button20"], {"axis": "y", "axisl": "max", "res": (92, 30)}),
                    "quit": M.create_button("quit", v2(400, 270), AM.assets["button20"], {"axis": "y", "axisl": "max", "res": (92, 30)})},
          "Bars": {
                    "XP_bar": M.create_button("", v2(320, 30), AM.assets["xp_bar_uncoloured"], {"text_pos": "top", "active": True, "hover_slide": False, "res": AM.assets["xp_bar_uncoloured"].size, "axisl": "min"}),
                    "Health_bar": M.create_button("", v2(80, 35), AM.assets["empty_bar_outline"], {"text_pos": "top", "active": True, "hover_slide": False, "res": AM.assets["empty_bar_outline"].size, "axisl": "min"}),
                    "Stamina_bar": M.create_button("", v2(560, 35), AM.assets["empty_bar_outline"], {"text_pos": "top", "active": True, "hover_slide": False, "res": AM.assets["empty_bar_outline"].size, "axisl": "min"})}}

ENEMIES = {  # Enemy settings           name,       res,      health, vel, damage, attack_range, armour, xp_chances, has_shadow
          "canine_grey": M.create_enemy("canine_grey", (48, 32), 200, 140, 20, 50, 1, {"blue": 0.95, "orange": 1}, True, 48),
          "canine_white": M.create_enemy("canine_white", (48, 32), 300, 150, 25, 50, 1, {"blue": 0.95, "orange": 1}, True, 48),
          "canine_black": M.create_enemy("canine_black", (48, 32), 400, 150, 30, 50, 2, {"blue": 0.95, "orange": 1}, True, 48),
          "werewolf": M.create_enemy("werewolf", (184, 64), 8000, 185, 60, 100, 5, {"green": 1}, True, 100, {"knockback": 1.2}),
          "pebble": M.create_enemy("pebble", (32, 32), 100, 150, 5, 50, 2, {"orange": 0.95, "green": 1}, False, 0, {"spawn_blood": False}),
          "golem": M.create_enemy("golem", (32, 32), 600, 160, 50, 50, 2, {"orange": 0.95, "green": 1}, True, 24, {"spawn_blood": False}),
          "armoured_golem": M.create_enemy("armoured_golem", (32, 32), 700, 160, 60, 50, 5, {"orange": 0.95, "green": 1}, True, 24, {"spawn_blood": False}),
          "titan": M.create_enemy("titan", (130, 100), 16000, 200, 80, 50, 10, {"purple": 1}, False, {"knockback": 1.2, "spawn_blood": False}),
          "mini_peka": M.create_enemy("mini_peka", (32, 32), 800, 160, 70, 50, 1, {"green": 0.95, "purple": 1}, True, 32),
          "bat": M.create_enemy("bat", (64, 64), 900, 160, 80, 50, 1, {"green": 0.95, "purple": 1}, True, 32),
          "skinny": M.create_enemy("skinny", (64, 64), 1000, 160, 90, 50, 1, {"green": 0.95, "purple": 1}, True, 36),
          "brain": M.create_enemy("brain", (80, 64), 30000, 200, 100, 50, 2, {"light_blue": 1}, True, 48, {"knockback": 1.2})}

CARDS = {  # Card settings
          6: ["damage", 6], 13: ["health", 6], 20: ["pierce", 1], 25: ["attack_speed", 0.004], 29: ["stamina", 8], 33: ["shots", 1.2], 41: ["knockback", 4],  # common
          45: ["damage", 10], 55: ["health", 10], 59: ["pierce", 1.5], 67: ["attack_speed", 0.008], 74: ["spread", 1], 83: ["stamina", 10], 90: ["knockback", 6],  # rare
          97: ["damage", 13], 106: ["health", 13], 111: ["pierce", 2], 120: ["attack_speed", 0.009], 127: ["spread", 2], 134: ["stamina", 13], 140: ["knockback", 7],  # epic
          144: ["damage", 20], 148: ["health", 20], 152: ["pierce", 3], 156: ["attack_speed", 0.01], 160: ["spread", 3], 163: ["stamina", 20], 165: ["knockback", 8]}  # legendary
