from Code.Variables.SettingVariables import *


class CameraManager():
          def __init__(self, game):
                    self.game = game
                    self.res = self.game.render_resolution  # Resolution of the game window

                    # Set camera attributes from CAMERA settings
                    self.game.methods.set_attributes(self, CAMERA)

                    # Initialize camera position and offset
                    self.target_offset = v2(0, 0)
                    self.current_offset = v2(0, 0)

                    # Set initial camera position centered on the player
                    self.pos = v2(self.game.player.pos.x - self.res[0] / 2, self.game.player.pos.y - self.res[1] / 2)
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.res[0], self.res[1])

                    # Initialize screen shake parameters
                    self.shake_start_time = 0
                    self.shake_magnitude = 0
                    self.shake_duration = 0
                    self.shake_seed = random.random() * 1000
                    self.shake_direction = v2(1, 1)

                    # Create a Perlin noise map for camera shake
                    self.noise_map = PerlinNoise(MAP["camera_shake_map"][0], random.randint(0, 100000))

          def update(self):
                    if not self.game.died and not self.game.won:
                              # Update camera position based on player movement
                              self.pos = v2(self.game.player.pos.x - self.res[0] / 2, self.game.player.pos.y - self.res[1] / 2)

                              # Apply various camera effects
                              self.update_mouse_smoothing()
                              rounded_offset = self.calculate_offset()
                              shake_offset = self.calculate_shake()
                              self.update_offset_rect(rounded_offset, shake_offset)
                              self.ensure_player_in_bounds()

          def update_mouse_smoothing(self):
                    # Calculate target mouse position relative to screen center
                    mouse_target = v2(self.game.inputM.get("position")[0] - 0.5 * self.res[0],
                                      self.game.inputM.get("position")[1] - 0.5 * self.res[1])

                    # Apply smoothing to mouse movement
                    dt = min(self.game.dt, 1 / 20)
                    self.mouse_smoothing = v2(
                              self.game.methods.lerp(self.mouse_smoothing.x, mouse_target.x,
                                                     self.window_mouse_smoothing_amount * dt),
                              self.game.methods.lerp(self.mouse_smoothing.y, mouse_target.y,
                                                     self.window_mouse_smoothing_amount * dt)
                    )

                    # Apply deadzone to reduce small, unintended movements
                    self.mouse_smoothing.x = 0 if abs(self.mouse_smoothing.x) < self.deadzone else self.mouse_smoothing.x
                    self.mouse_smoothing.y = 0 if abs(self.mouse_smoothing.y) < self.deadzone else self.mouse_smoothing.y

          def calculate_offset(self):
                    # Calculate target offset based on mouse position
                    self.target_offset = v2(
                              self.window_max_offset * int(self.mouse_smoothing.x),
                              self.window_max_offset * int(self.mouse_smoothing.y)
                    )

                    dt = min(self.game.dt, 1 / 20)
                    # Smoothly interpolate current offset towards target offset
                    self.current_offset = v2(
                              self.game.methods.lerp(self.current_offset.x, self.target_offset.x, self.lerp_speed * dt),
                              self.game.methods.lerp(self.current_offset.y, self.target_offset.y, self.lerp_speed * dt)
                    )

                    return v2(round(self.current_offset.x), round(self.current_offset.y))

          def update_offset_rect(self, rounded_offset, shake_offset):
                    # Update the camera's offset rectangle, considering game boundaries
                    self.rect.x = max(0, min(self.pos.x + rounded_offset.x + shake_offset.x,
                                             GAMESIZE[0] - self.res[0]))
                    self.rect.y = max(0, min(self.pos.y + rounded_offset.y + shake_offset.y,
                                             GAMESIZE[1] - self.res[1]))

          def ensure_player_in_bounds(self):
                    # Ensure the player stays within the camera's view
                    player = self.game.player
                    player_left = player.pos.x - self.rect.x - player.res[0] / 2
                    player_right = player_left + player.res[0]
                    player_top = player.pos.y - self.rect.y - player.res[1] / 2
                    player_bottom = player_top + player.res[1]

                    # Adjust camera if player is too close to the edges
                    if player_left < player.offset:
                              self.rect.x += player_left - player.offset
                    elif player_right > self.res[0] - player.offset:
                              self.rect.x += player_right - (self.res[0] - player.offset)

                    if player_top < player.offset:
                              self.rect.y += player_top - player.offset
                    elif player_bottom > self.res[1] - player.offset:
                              self.rect.y += player_bottom - (self.res[1] - player.offset)

                    # Ensure camera stays within game boundaries
                    self.rect.x = max(0, min(self.rect.x, GAMESIZE[0] - self.res[0]))
                    self.rect.y = max(0, min(self.rect.y, GAMESIZE[1] - self.res[1]))

          def calculate_shake(self):
                    # Calculate screen shake effect
                    current_time = self.game.game_time
                    elapsed_time = current_time - self.shake_start_time

                    # Return zero offset if shake duration has passed
                    if elapsed_time > self.shake_duration:
                              self.shake_duration = 0
                              return v2(0, 0)

                    # Calculate shake intensity based on elapsed time
                    fade_out = 1 - (elapsed_time / self.shake_duration)
                    sin_value = math.sin(self.shake_speed * (self.shake_seed + elapsed_time))

                    # Use Perlin noise for more natural shake movement
                    noise_x = self.get_2d_noise(self.shake_seed + elapsed_time, 0)
                    noise_y = self.get_2d_noise(0, self.shake_seed + elapsed_time)
                    noise_offset = v2(noise_x, noise_y)

                    # Calculate final shake direction and magnitude
                    direction = (self.shake_direction + noise_offset * self.reduced_screen_shake).normalize()
                    shake_offset = direction * sin_value * self.shake_magnitude * fade_out
                    return v2(int(shake_offset.x), int(shake_offset.y))

          def get_2d_noise(self, x, y):
                    # Generate 2D Perlin noise for camera shake
                    scaled_x, scaled_y = x * MAP["camera_shake_map"][1], y * MAP["camera_shake_map"][1]
                    return self.noise_map([scaled_x, scaled_y])

          def add_screen_shake(self, duration, magnitude):
                    # Add a new screen shake effect
                    if self.shake_duration + self.shake_start_time < self.game.game_time:
                              self.shake_magnitude = 0
                    if magnitude > self.shake_magnitude:
                              self.shake_duration = duration
                              self.shake_magnitude = magnitude
                              self.shake_start_time = self.game.game_time
                              self.shake_seed = self.game.game_time
                              self.shake_direction = v2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
