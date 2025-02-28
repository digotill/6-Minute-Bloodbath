from Code.Variables.SettingVariables import *


class Bullet:
          def __init__(self, game, gun, pos, angle, name, spread_factor, shake_map):
                    # Initialize bullet properties
                    self.game = game
                    self.gun = gun
                    self.name = name

                    # Calculate bullet spread using noise
                    noise_value = shake_map([game.game_time * MAP["gun_shake_map"][0], 0])
                    spread_angle = noise_value * gun.spread * spread_factor
                    self.angle = angle + spread_angle

                    # Set up bullet image
                    self.image = pygame.transform.rotate(gun.bullet_image, self.angle + 90)
                    self.original_image = gun.bullet_image

                    # Set up bullet position and velocity
                    self.pos = v2(pos)
                    self.vel_vector = v2(0, -gun.vel).rotate(-self.angle)
                    self.original_vel_vector = self.vel_vector
                    self.rect = self.image.get_rect(center=self.pos)
                    self.res = self.rect.size

                    self.hit_list = []  # List to track hit targets

                    # Set up bullet properties
                    self.lifetime = self.game.methods.change(self.gun.lifetime, self.gun.lifetime_randomness)
                    self.dead = False
                    self.creation_time = game.game_time
                    self.friction = self.gun.friction
                    self.damage = self.gun.damage
                    self.pierce = self.gun.pierce

          def update(self):
                    # Apply friction to bullet velocity
                    if self.friction > 0:
                              self.vel_vector *= (1 - self.friction * self.game.dt)

                    # Update bullet position
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def draw(self, surface=None):
                    # Draw the bullet on the given surface (or game display if None)
                    if surface is None:
                              surface = self.game.displayS
                    pos = self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y
                    surface.blit(self.image, pos)

          def collide(self, target):
                    # Check for collision with a target
                    rect = self.rect.inflate(self.res[0] / 2, self.res[1] / 2)
                    if rect.colliderect(target.rect) and target not in self.hit_list and not target.dead:
                              target.health -= self.damage * self.vel_vector.length_squared() / self.original_vel_vector.length_squared()
                              self.pierce -= target.armour
                              self.hit_list.append(target)

                              # Add blood effect
                              angle = self.angle if self.angle > 0 else 360 + self.angle
                              if random.random() < BLOOD["blood_amount"] and target.spawn_blood:
                                        self.game.effectM.add_effect(self.pos, angle, BLOOD["blood"])

                              if target.health > 0:
                                        # Apply knockback if the enemy is still alive
                                        knockback_force = self.vel_vector.normalize() * self.game.player.gun.knockback
                                        target.apply_knockback(knockback_force)

                              target.hit_count = 0
                              if self.pierce <= 0:
                                        self.dead = True
                              return True
                    return False

          def reset(self, pos, angle, spread):
                    # Reset the bullet with new parameters
                    self.__init__(self.game, self.gun, pos, angle, self.name, spread, self.game.player.gun.noise_map)
