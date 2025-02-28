from Code.Individuals.Gun import *


class Player:
          def __init__(self, game):
                    self.game = game

                    # Set player attributes from PLAYER settings
                    self.game.methods.set_attributes(self, PLAYER)

                    # Find a suitable spawn position and set up the player's rectangle
                    self.pos = self.find_spawn_position()
                    self.game.methods.set_rect(self)

                    # Initialize player state variables
                    self.gun = self.game.gun
                    self.current_animation = 'idle'
                    self.facing = "right"
                    self.is_sprinting = False
                    self.dead = False
                    self.frame = 0
                    self.max_health = self.health
                    self.max_stamina = self.stamina
                    self.last_hit = - self.hit_cooldown
                    self.dx = self.dy = 0
                    self.water_check_timer = Timer(0.2, 0)
                    self.hit_count = None

                    self.jump_velocity = self.jumping_velocity  # Adjust this value to change jump height
                    self.gravity = self.gravity  # Adjust this value to change falling speed
                    self.air_offset = 0  # This will be used to draw the player above their actual position

                    self.is_on_air = False
                    self.jumping_timer = Timer(self.jump_cooldown, self.game.game_time)

                    self.xp = 0
                    self.level = 1
                    self.calculate_max_xp()
                    self.xp_to_add = 0

                    self.velocity = v2(0, 0)
                    self.acceleration = v2(0, 0)
                    self.base_vel = self.vel

          def apply_force(self, force):
                    self.acceleration += force

          def jump(self):
                    if not self.is_on_air and self.stamina - self.jump_stamina > 0 and self.jumping_timer.update(self.game.game_time):
                              self.jump_velocity = self.jumping_velocity
                              self.is_on_air = True
                              self.stamina -= self.jump_stamina
                              self.air_offset = -1
                              self.game.soundM.play_sound("jump", VOLUMES["jump_frequancy"], VOLUMES["jump_volume"] * self.game.master_volume)
                              self.velocity *= self.jump_vel

          def handle_input(self):
                    input_force = v2(0, 0)
                    if self.game.inputM.get("move_left"): input_force.x -= 1
                    if self.game.inputM.get("move_right"): input_force.x += 1
                    if self.game.inputM.get("move_up"): input_force.y -= 1
                    if self.game.inputM.get("move_down"): input_force.y += 1

                    if self.game.inputM.get("jump"):self.jump()

                    if input_force.length() > 0:
                              input_force = input_force.normalize() * self.acceleration_rate
                              input_force *= self.vel / self.base_vel
                              self.apply_force(input_force)

                    self.vel = self.base_vel

          def update_physics(self):

                    # Update velocity
                    if not self.is_on_air:
                              self.velocity *= self.friction
                              self.velocity += self.acceleration * self.game.dt
                              if self.velocity.length() > self.vel:
                                        self.velocity.scale_to_length(self.vel)

                    # Update position
                    new_pos = self.pos + self.velocity * self.game.dt

                    # Check and adjust for game boundaries
                    new_pos.x = max(self.res[0] / 2 + self.offset, min(new_pos.x, GAMESIZE[0] - self.res[0] / 2 - self.offset))
                    new_pos.y = max(self.res[0] / 2 + self.offset, min(new_pos.y, GAMESIZE[1] - self.res[1] / 2 - self.offset))

                    self.pos = new_pos

                    # Reset acceleration
                    self.acceleration *= 0

          def update_position(self):
                    self.rect.centerx = int(self.pos.x)
                    self.rect.centery = int(self.pos.y)

          def calculate_max_xp(self):
                    base_xp = EXPERIENCE["starting_max_xp"]
                    growth_factor = EXPERIENCE["xp_progression_rate"]
                    self.max_xp = int(base_xp * (growth_factor ** (self.level - 1)))

          def find_spawn_position(self):
                    # Find a suitable spawn position that's not on a water tile
                    center_x, center_y = GAMESIZE[0] // 2, GAMESIZE[1] // 2
                    max_distance = max(GAMESIZE[0], GAMESIZE[1])

                    for distance in range(0, max_distance, 16):
                              for angle in range(0, 360, 10):
                                        x = center_x + int(distance * math.cos(math.radians(angle)))
                                        y = center_y + int(distance * math.sin(math.radians(angle)))

                                        if 0 <= x < GAMESIZE[0] and 0 <= y < GAMESIZE[1]:
                                                  test_rect = pygame.Rect(x, y, self.res[0], self.res[1])
                                                  if not self.game.tilemapM.tile_collision(test_rect, "water_tile"):
                                                            return v2(x, y)

          def change_animation(self, animation_name):
                    # Change the current animation if it's different from the new one
                    if self.current_animation != animation_name:
                              self.current_animation = animation_name
                              self.frame = 0

          def update_animation(self):
                    # Update the animation based on player movement
                    new_animation = 'running' if (self.game.inputM.get("move_left") or self.game.inputM.get("move_right") or
                                                  self.game.inputM.get("move_down") or self.game.inputM.get("move_up")) and not self.game.changing_settings else 'idle'
                    self.change_animation(new_animation)

          def update(self):
                    if not self.game.changing_settings and not self.game.died and not self.game.won and not self.game.cards_on:
                              self.handle_input()
                              self.handle_stamina()
                              self.update_physics()
                              self.update_jumping()
                              self.update_position()
                              self.handle_slowdown()
                              self.manage_xp()

                    self.update_facing()
                    self.update_animation()
                    self.gun.update()
                    self.update_frame()
                    self.game.grassM.apply_force(self.rect.midbottom, self.rect.width, self.grass_force)

          def update_jumping(self):
                    if self.is_on_air and self.air_offset >= 0:
                              self.is_on_air = False
                              self.jumping_timer.reactivate(self.game.game_time)

                    if self.is_on_air:
                              self.air_offset += self.jump_velocity * self.game.dt
                              self.jump_velocity += self.gravity * self.game.dt
                    else:
                              self.air_offset = 0

          def manage_xp(self):
                    if self.xp >= self.max_xp:
                              self.level += 1
                              self.xp = self.xp - self.max_xp
                              self.calculate_max_xp()
                              self.game.cardM.toggle()
                              self.game.soundM.play_sound("level_up", VOLUMES["level_up_frequancy"], VOLUMES["level_up_volume"] * self.game.master_volume)
                    else:
                              self.calculate_max_xp()
                              xp = EXPERIENCE["gradual_increase"] * self.game.dt * self.xp_to_add / self.max_xp
                              if self.xp_to_add > xp:
                                        self.xp += xp
                                        self.xp_to_add -= xp

          def draw(self, surface=None):
                    # Draw the player on the given surface (or game display if none provided)
                    if surface is None:
                              surface = self.game.displayS

                    # Get the current animation frame
                    current_animation = self.game.assets["player_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    image = current_animation[frame_index]

                    # Draw player shadow
                    shadow_image = self.game.methods.get_shadow_image(self, image)
                    surface.blit(shadow_image, (self.get_position()[0], self.get_position()[1] + self.res[1] - shadow_image.height / 2))

                    # Apply hit effect if player was recently hit
                    if self.hit_count is not None:
                              image = self.game.methods.get_image_mask(image)
                              self.hit_count += self.hit_effect[1] * self.game.dt
                              if self.hit_count >= self.hit_effect[0]:
                                        self.hit_count = None

                    # Draw player
                    surface.blit(image, (self.get_position()[0], self.get_position()[1] + self.air_offset))

                    # Draw gun
                    self.gun.draw(surface)
                    self.game.muzzleflashM.draw()

          def handle_stamina(self):
                    self.is_sprinting = self.game.inputM.get("sprint") and self.velocity.length() > 0 and not self.game.changing_settings
                    if self.is_sprinting and self.stamina > 0:
                              self.vel *= self.sprint_vel
                              self.stamina -= self.stamina_consumption * self.game.dt
                              self.stamina = max(0, self.stamina)
                    else:
                              self.stamina += self.stamina_recharge_rate * self.game.dt
                              self.stamina = min(self.max_stamina, self.stamina)

                    if self.stamina <= 0:
                              self.is_sprinting = False

          def update_frame(self):
                    if not self.game.died and not self.game.won and not self.is_on_air:
                              factor = self.velocity.length() / self.base_vel
                              self.frame += self.animation_speed * factor * self.game.dt

          def get_position(self):
                    # Get player's position relative to the camera
                    return self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y

          def get_mid_position(self):
                    # Get player's center position relative to the camera
                    return self.rect.centerx - self.game.cameraM.rect.x, self.rect.centery - self.game.cameraM.rect.y

          def update_facing(self):
                    # Update player's facing direction based on mouse position
                    if not self.game.died and not self.game.won:
                              if self.game.inputM.get("position")[0] < self.get_mid_position()[0]:
                                        self.facing = "left"
                              else:
                                        self.facing = "right"

          def deal_damage(self, damage):
                    # Apply damage to player if not in hit cooldown
                    if self.game.game_time - self.last_hit > self.hit_cooldown and not self.is_on_air:
                              self.health -= damage
                              self.check_if_alive()

                              if not self.dead:
                                        self.game.cameraM.add_screen_shake(GENERAL["misc"][2][1], GENERAL["misc"][2][0])
                                        self.last_hit = self.game.game_time
                                        self.game.soundM.play_sound("heartbeat", VOLUMES["heartbeat_frequancy"], VOLUMES["heartbeat_volume"] * self.game.master_volume)
                                        integer = str(random.randint(0, 4))
                                        self.game.soundM.play_sound("splatter" + integer, VOLUMES["splatter_frequancy"], VOLUMES["splatter_volume"] * self.game.master_volume)
                                        self.hit_count = 0
                                        self.game.screeneffectM.add_blood_effect()
                                        for _ in range(BLOOD["blood_on_player_hit"]):
                                                  self.game.effectM.add_effect(self.pos, random.random() * 360, BLOOD["blood"])

          def check_if_alive(self):
                    # Check if player's health has depleted
                    if self.health <= 0:
                              self.dead = True
                              self.health = 0

          def handle_slowdown(self):
                    collision = self.game.tilemapM.tile_collision(pygame.Rect(self.pos.x, self.pos.y + self.res[1] / 2, 0, 0), "water_tile")
                    if collision:
                              self.vel *= self.slowed_vel
