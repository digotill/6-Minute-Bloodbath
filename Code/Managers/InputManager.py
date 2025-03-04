from Code.Variables.SettingVariables import *


class InputManager:
    def __init__(self, game):
        self.game = game
        self.keys = {
            'move_up': Input(self.game, pygame.K_w),
            'move_left': Input(self.game, pygame.K_a),
            'move_down': Input(self.game, pygame.K_s),
            'move_right': Input(self.game, pygame.K_d),
            'jump': Input(self.game, pygame.K_SPACE),
            'sprint': Input(self.game, pygame.K_LSHIFT),
            'dodge': Input(self.game, pygame.K_SPACE, 1),
            'toggle_fullscreen': Input(self.game, pygame.K_F11, 0.5),
            'toggle_fps': Input(self.game, pygame.K_F12, 0.2),
            'quit': Input(self.game, pygame.K_F10),
            'ungrab': Input(self.game, pygame.K_ESCAPE),
        }
        self.mouse = {
            "left_click": False,
            "right_click": False,
            "position": v2(0, 0),
            "real_position": v2(0, 0)
        }

    def get_mouse(self, key):
        return self.mouse.get(key, None)

    def get(self, key):
        if key in self.keys:
            return self.keys[key].state
        elif key in self.mouse:
            return self.mouse[key]
        return None

    def update(self):
        keys = pygame.key.get_pressed()
        for input_obj in self.keys.values():
            input_obj.update(keys)

        self.mouse["left_click"], _, self.mouse["right_click"] = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.mouse["real_position"] = v2(max(0, min(mouse_pos[0], self.game.display.width)),
                                         max(0, min(mouse_pos[1], self.game.display.height)))
        self.mouse["position"] = v2(
            int(self.mouse["real_position"].x * self.game.render_resolution[0] / self.game.display.width),
            int(self.mouse["real_position"].y * self.game.render_resolution[1] / self.game.display.height))
        if self.mouse["real_position"] != mouse_pos: pygame.mouse.set_pos(
            self.mouse["real_position"])  # Update mouse position if changed

        if self.game.auto_shoot and not self.game.changing_settings and not self.game.in_menu and not self.game.died:
            self.mouse["left_click"] = True


class Input:
    def __init__(self, game, pygame_input, cooldown=None):
        self.game = game
        self.input = pygame_input
        self.state = False
        self.timer = Timer(cooldown, pygame.time.get_ticks() / 1000) if cooldown else None

    def update(self, keys):
        if self.timer is not None:
            if self.timer.check(pygame.time.get_ticks() / 1000):
                self.state = keys[self.input]
                if self.state:
                    self.timer.reactivate(pygame.time.get_ticks() / 1000)
            else:
                self.state = False
        else:
            self.state = keys[self.input]
