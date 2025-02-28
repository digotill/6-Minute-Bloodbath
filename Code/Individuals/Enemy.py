from Code.Variables.SettingVariables import *


class Enemy:
          def __init__(self, game, dictionary):
                    self.game = game

                    # Set attributes from the provided dictionary
                    self.game.methods.set_attributes(self, dictionary)

                    # Initialize enemy position and attributes
                    self.set_coordinates()
                    self.game.methods.set_rect(self)

                    self.health *= DIFFICULTY[self.game.difficulty][1] * (DIFFICULTY["win_change"][1] ** self.game.wins)
                    self.vel *= DIFFICULTY[self.game.difficulty][0] * (DIFFICULTY["win_change"][0] ** self.game.wins)
                    self.damage *= DIFFICULTY[self.game.difficulty][2] * (DIFFICULTY["win_change"][2] ** self.game.wins)

                    self.acceleration = v2(0, 0)
                    self.vel_vector = v2(0, 0)
                    self.max_vel = self.vel
                    self.max_health = self.health
                    self.current_animation = 'running'
                    self.is_attacking = False
                    self.hit_count = None
                    self.dead = False
                    self.creation_time = self.game.game_time
                    self.last_hit = - self.hit_cooldown
                    self.facing = "right"
                    self.frame = 0

                    self.attack_timer = Timer(self.attack_cooldown, self.game.game_time)

          def apply_force(self, force):
                    # Apply a force to the enemy's velocity
                    self.vel_vector += force
                    if self.vel_vector.length() > self.vel:
                              self.vel_vector = self.vel_vector.normalize() * self.vel

          def set_coordinates(self):
                    # Set initial coordinates for the enemy spawn
                    s = GENERAL["misc"][1]
                    camera_rect = self.game.cameraM.rect
                    spawn_area = pygame.Rect(camera_rect.left - s, camera_rect.top - s, camera_rect.width + 2 * s, camera_rect.height + 2 * s)

                    while True:
                              x = random.randint(spawn_area.left, spawn_area.right - self.res[0])
                              y = random.randint(spawn_area.top, spawn_area.bottom - self.res[1])

                              # Create a rect for the potential enemy position
                              enemy_rect = pygame.Rect(x, y, self.res[0], self.res[1])

                              # Check if the enemy is outside the camera view and within the game boundaries
                              if not camera_rect.colliderect(enemy_rect) and 0 <= x < GAMESIZE[0] - self.res[0] and 0 <= y < GAMESIZE[1] - self.res[1]:
                                        self.pos = v2(x, y)
                                        break

          def update(self):
                    # Main update method, randomly choosing between full and partial updates
                    self.attack_timer.update(self.game.dt)  # Update the attack timer
                    if random.random() < 0.1:
                              self.full_update()
                    else:
                              self.partial_update()

          def full_update(self):
                    # Perform a full update of the enemy's state and actions
                    self.update_state()
                    if self.should_move():
                              self.move()
                    self.update_is_attacking()
                    self.update_frame()
                    self.update_facing()
                    self.update_position()
                    self.attack_player()

          def partial_update(self):
                    # Perform a partial update (less computationally intensive)
                    if self.should_move():
                              self.update_position()
                    self.update_frame()

          def update_frame(self):
                    # Update the animation frame
                    self.frame += self.animation_speed * self.game.dt

          def should_move(self):
                    # Determine if the enemy should move based on distance to player
                    return (self.game.player.rect.center - self.pos).length_squared() > self.stopping_range

          def attack_player(self):
                    # Attempt to damage the player if in attack range and cooldown is over
                    if self.is_attacking and self.rect.colliderect(self.game.player.rect):
                              if self.attack_timer.check(self.game.game_time):
                                        self.game.player.deal_damage(self.damage)
                                        self.attack_timer.reactivate(self.game.game_time)  # Reset the timer after a successful attack

          def move(self):
                    # Move the enemy towards the player
                    direction = self.game.player.rect.center - self.pos
                    if direction.length_squared() > 0:
                              direction = direction.normalize()

                    desired_velocity = direction * self.max_vel
                    steering = (desired_velocity - self.vel_vector) * self.steering_strength
                    self.apply_force(steering)

                    self.vel_vector += self.acceleration * self.game.dt
                    if self.vel_vector.length_squared() > self.max_vel ** 2:
                              self.vel_vector = self.vel_vector.normalize() * self.max_vel

                    self.vel_vector *= (1 - self.friction)
                    self.acceleration.update(0, 0)

          def update_position(self):
                    # Update the enemy's position based on its velocity
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = (int(self.pos.x), int(self.pos.y))

          def update_facing(self):
                    # Update the direction the enemy is facing
                    self.facing = "right" if self.game.player.rect.centerx > self.pos.x else "left"

          def distance_to_player(self):
                    # Calculate the distance to the player
                    return (self.game.player.rect.center - self.pos).length()

          def update_is_attacking(self):
                    # Determine if the enemy should be in attacking state
                    distance_squared = (self.game.player.rect.center - self.pos).length_squared()
                    if distance_squared <= self.attack_range ** 2:
                              self.is_attacking = True
                    elif self.is_attacking and self.frame > len(self.game.assets[f"{self.name}_{self.current_animation}_{self.facing}"]):
                              self.is_attacking = False
                    self.update_animation()

          def get_position(self):
                    # Get the enemy's position relative to the camera
                    return self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y

          def draw(self, surface=None):
                    # Draw the enemy on the given surface
                    if surface is None:
                              surface = self.game.displayS
                    pos = self.get_position()
                    current_sprite = self.get_current_sprite()
                    if self.has_shadow:
                        shadow_image = self.game.methods.get_shadow_image2(self, self.shadow_width)
                        self.game.displayS.blit(shadow_image, (pos[0] + self.res[0] / 2 - shadow_image.width / 2, pos[1] + self.res[1] - shadow_image.height / 2))
                    if self.hit_count is not None:
                              current_sprite = self.game.methods.get_image_mask(current_sprite)
                              self.hit_count += self.hit_effect[1] * self.game.dt
                              if self.hit_count >= self.hit_effect[0]:
                                        self.hit_count = None
                    surface.blit(current_sprite, pos)

          def get_current_sprite(self):
                    # Get the current sprite based on the enemy's state and animation
                    current_animation = self.game.assets[self.name + "_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    sprite = current_animation[frame_index]
                    return sprite

          def reset(self, new_dictionary):
                    # Reset the enemy with new attributes
                    self.__init__(self.game, new_dictionary)

          def change_animation(self, animation_name):
                    # Change the current animation
                    if self.current_animation != animation_name:
                              self.current_animation = animation_name
                              self.frame = 0

          def update_animation(self):
                    # Update the animation based on the enemy's state
                    new_animation = 'attacking' if self.is_attacking else 'running'
                    if self.current_animation != new_animation:
                              self.current_animation = new_animation
                              self.frame = 0

          # New methods for enhanced behavior

          def update_state(self):
                    # Update the enemy's state based on various conditions
                    distance_to_player = self.distance_to_player()

                    if distance_to_player <= self.attack_range:
                              self.state = 'attack'
                    else:
                              self.state = 'chase'

          def take_damage(self, damage):
                    # Handle the enemy taking damage
                    self.health -= damage
                    self.hit_count = 0
                    if self.health <= 0:
                              self.die()

          def die(self):
                    # Handle the enemy's death
                    self.dead = True
                    # Add any death animation or particle effects here
                    self.game.remove_enemy(self)

          def apply_knockback(self, force):
                    self.apply_force(force * self.knockback)
