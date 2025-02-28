from Code.Individuals.Enemy import *
from Code.DataStructures.HashMap import *


class EnemyManager:
          def __init__(self, game):
                    self.game = game

                    self.grid = HashMap(game, GENERAL["hash_maps"][0])  # Spatial hash grid for efficient enemy management
                    self.enemy_pool = set()  # Pool of inactive enemies for reuse

                    self.spawn_timer = Timer(GENERAL["enemies"][1], self.game.game_time)  # Timer for enemy spawning
                    self.seperation_timer = Timer(GENERAL["enemies"][3], self.game.game_time)
                    self.rebuild_timer = Timer(GENERAL["enemies"][4], self.game.game_time)

          def update(self):
                    if not self.game.changing_settings and self.game.game_time > 5 and not self.game.cards_on:
                              for enemy in self.grid.items:
                                        enemy.update()  # Update each enemy's state
                                        if self.seperation_timer.update(self.game.game_time):
                                                  separation_force = self.calculate_separation(enemy)
                                                  enemy.apply_force(separation_force)  # Apply separation to avoid crowding
                                                  self.seperation_timer.reactivate(self.game.game_time)

                              self.remove_dead_enemies()  # Clean up dead enemies

                              self._add_enemies()  # Spawn new enemies if necessary

                              if self.rebuild_timer.update(self.game.game_time):
                                        self.grid.rebuild()  # Periodically rebuild spatial hash grid
                                        self.rebuild_timer.reactivate(self.game.game_time)

          def _add_enemies(self):
                    if self.spawn_timer.update(self.game.game_time):
                              current_time = self.game.game_time

                              # Find the appropriate progression stage
                              current_stage = max([time for time in PROGRESSION.keys() if time <= current_time])
                              enemy_probabilities = PROGRESSION[current_stage]

                              # Calculate total probability
                              total_prob = sum(enemy_probabilities.values())

                              # Generate a random number
                              rand_num = random.random() * total_prob

                              # Select an enemy type based on probabilities
                              cumulative_prob = 0
                              for enemy_type, prob in enemy_probabilities.items():
                                        cumulative_prob += prob
                                        if rand_num <= cumulative_prob:
                                                  if enemy_type != "nothing":
                                                            self.add_enemy(enemy_type)
                                                  break

                              # Reset the spawn timer
                              self.spawn_timer.reactivate(self.game.game_time)

                    for key in BOSSES.keys():
                              if self.game.game_time >= key and not getattr(self, BOSSES[key] + "_spawned", False) and GENERAL["enemies"][2]:
                                        enemy = Enemy(self.game, ENEMIES[BOSSES[key]])
                                        self.grid.insert(enemy)
                                        setattr(self, BOSSES[key] + "_spawned", True)
                                        break

          def add_enemy(self, enemy_type):
                    if len(self.grid.items) < GENERAL["enemies"][0] and GENERAL["enemies"][2]:  # Check enemy limit and spawn flag
                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()  # Reuse enemy from pool if available
                                        enemy.reset(ENEMIES[enemy_type])
                              else:
                                        enemy = Enemy(self.game, ENEMIES[enemy_type])  # Create new enemy if pool is empty

                              self.grid.insert(enemy)  # Add enemy to spatial hash grid

          def remove_dead_enemies(self):
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)  # Remove dead enemy from grid
                                        self.enemy_pool.add(enemy)  # Add dead enemy back to pool for reuse
                                        xp_type = self.get_experience(enemy)
                                        self.game.experienceM.add_experience(xp_type, enemy.rect.center)  # Add enemy's experience to player's total
                                        if enemy.spawn_blood:
                                                  self.game.effectM.draw_at(enemy.rect)

          @staticmethod
          def get_experience(enemy):
                    random_value = random.random()

                    for xp_type, chance in enemy.xp_chances.items():
                              if random_value <= chance:
                                        return xp_type

                    # If no experience type is selected (which should be rare),
                    # return the lowest tier experience type as a fallback
                    return "blue"

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(enemy.separation_radius * 2, enemy.separation_radius * 2))  # Query nearby enemies

                    enemy_pos = enemy.pos
                    separation_radius_sq = enemy.separation_radius ** 2

                    for other in nearby_enemies:
                              if other is not enemy:
                                        dx = enemy_pos.x - other.pos.x
                                        dy = enemy_pos.y - other.pos.y
                                        distance_sq = dx * dx + dy * dy

                                        if distance_sq < separation_radius_sq:
                                                  inv_dist = 1.0 / (distance_sq ** 0.5 + 1e-6)  # Inverse distance (avoid division by zero)
                                                  steering.x += dx * inv_dist
                                                  steering.y += dy * inv_dist
                                                  total += 1

                    if total > 0:
                              steering.x /= total
                              steering.y /= total

                              length = (steering.x ** 2 + steering.y ** 2) ** 0.5
                              if length > 0:
                                        inv_length = 1.0 / length
                                        steering.x *= inv_length * enemy.vel  # Normalize and scale by enemy velocity
                                        steering.y *= inv_length * enemy.vel

                              rel_vel_x = steering.x - enemy.vel_vector.x
                              rel_vel_y = steering.y - enemy.vel_vector.y
                              rel_vel_length_sq = rel_vel_x ** 2 + rel_vel_y ** 2

                              if rel_vel_length_sq > enemy.vel ** 2:
                                        inv_rel_vel_length = enemy.vel / (rel_vel_length_sq ** 0.5)
                                        steering.x = rel_vel_x * inv_rel_vel_length  # Limit steering force
                                        steering.y = rel_vel_y * inv_rel_vel_length

                    return steering * enemy.separation_strength  # Return final separation force
