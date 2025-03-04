from Code.Variables.SettingVariables import *


class Rain:
    def __init__(self, game, dictionary):
        self.game = game  # Reference to the main game object
        self.animation = self.game.assets["rain"]  # Load rain animation frames
        self.res = self.game.assets["rain"][0].size  # Get size of a rain frame

        self.game.methods.set_attributes(self, dictionary)  # Set attributes from dictionary

        # Calculate initial position based on camera offset
        self.pos = v2(self.game.methods.change(self.game.cameraM.rect.x * 1.1, self.game.cameraM.rect.width / 1.1),
                      self.game.cameraM.rect.y - self.game.cameraM.rect.height / 4)

        self.spawn_time = self.game.game_time  # Record spawn time
        self.initial_vel = self.vel  # Store initial velocity
        self.hit_ground = False  # Flag for when rain hits ground
        self.lifetime = self.game.methods.change(self.lifetime[0], self.lifetime[1])  # Set random lifetime
        self.vel = self.game.methods.change(self.vel[0], self.vel[1])  # Set random velocity
        self.vel_vector = self.calculate_vel_vector()  # Calculate velocity vector
        self.game.methods.set_rect(self)  # Set rectangle for rain drop
        self.frame = 0  # Current animation frame

    def update_frame(self):
        self.frame += self.animation_speed * self.game.dt  # Update animation frame

    def calculate_vel_vector(self):
        angle_rad = math.radians(self.angle)  # Convert angle to radians
        vel_x = self.vel * math.sin(angle_rad)  # Calculate x component of velocity
        vel_y = self.vel * math.cos(angle_rad)  # Calculate y component of velocity
        return v2(vel_x, vel_y)  # Return velocity vector

    def update(self):
        self.lifetime -= self.game.dt  # Decrease lifetime

        if self.lifetime <= 0:
            self.hit_ground = True  # Set hit_ground flag if lifetime is over

        if not self.hit_ground:
            self.pos += self.vel_vector * self.game.dt  # Update position
            self.rect.center = self.pos  # Update rectangle position

    def draw(self, surface=None):
        if surface is None:
            surface = self.game.displayS  # Use game's display surface if none provided

        # Calculate drawing position
        pos = self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y

        if not self.hit_ground:
            surface.blit(self.animation[0], pos)  # Draw falling raindrop
        else:
            # Draw splash animation
            surface.blit(
                self.animation[int(self.frame % len(self.animation))], pos)
