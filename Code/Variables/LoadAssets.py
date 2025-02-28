import pygame
import os
from PIL import Image
import io


class LoadAssets:
          def __init__(self):
                    self.assets = {}
                    self.load_all_assets()

          def load_all_assets(self):
                    assets_dir = "Assets"
                    for root, dirs, files in os.walk(assets_dir):
                              for file in files:
                                        file_path = os.path.join(root, file)
                                        file_name, file_ext = os.path.splitext(file)

                                        if "tileset" in file_name.lower():
                                                  self.load_tileset(file_path, file_name)
                                        elif "music" in file_name.lower():
                                                  self.load_music(file_path, file_name)
                                        elif file_ext.lower() in ['.png', '.jpg', '.jpeg']:
                                                  self.load_image(file_path, file_name)
                                        elif file_ext.lower() == '.gif':
                                                  self.load_gif(file_path, file_name)
                                        elif file_ext.lower() in ['.wav', '.ogg', '.mp3']:
                                                  self.load_sound(file_path, file_name)

          def load_gif(self, path, name):
                    frames = []
                    with Image.open(path) as gif:
                              for frame_index in range(gif.n_frames):
                                        gif.seek(frame_index)
                                        frame_rgba = gif.convert("RGBA")
                                        pygame_image = pygame.image.fromstring(
                                                  frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
                                        )
                                        frames.append(pygame_image)
                    self.assets[name] = frames

          def load_image(self, file_path, name):
                    img = pygame.image.load(file_path).convert_alpha()
                    self.assets[name] = img

          def load_sound(self, file_path, name):
                    sound = pygame.mixer.Sound(file_path)
                    self.assets[name] = sound

          def load_tileset(self, filepath, name):
                    tileset_image = pygame.image.load(filepath).convert_alpha()
                    tile = pygame.Surface((16, 16), pygame.SRCALPHA)
                    array = ["1212", "1101", "1010", "1011", "1", "1001", "", "0110", "2121", "0111", "0101", "1110", "0000", "1221", "2", "2112"]
                    dictionary = {}  # "top", "bottom", "right", "left"

                    def add_tile(count, position):
                              tile.fill((0, 0, 0, 0))
                              tile.blit(tileset_image, (0, 0), (16 * position[0], 16 * position[1], 16, 16))
                              dictionary[array[count]] = [tile.copy()]

                    for i in range(4):
                              for j in range(4):
                                        add_tile(i * 4 + j, (j, i))
                    self.assets[name] = dictionary

          def load_music(self, file_path, name):
                    self.assets[name] = file_path
