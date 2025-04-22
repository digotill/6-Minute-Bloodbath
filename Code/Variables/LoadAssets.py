import pygame
import os
from PIL import Image
import io


class LoadAssets:
    def __init__(self):
        # Initialize the assets dictionary to store loaded assets
        self.assets = {}
        # Load all assets upon initialization
        self.load_all_assets()

    def load_all_assets(self):
        # Define the directory where assets are stored
        assets_dir = "Assets"
        # Walk through the directory to find all files
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Split the file name and extension
                file_name, file_ext = os.path.splitext(file)

                # Load different types of assets based on file name or extension
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
        # Load a GIF file and convert each frame to a pygame image
        frames = []
        with Image.open(path) as gif:
            for frame_index in range(gif.n_frames):
                gif.seek(frame_index)
                frame_rgba = gif.convert("RGBA")
                pygame_image = pygame.image.fromstring(
                    frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
                )
                frames.append(pygame_image)
        # Store the frames in the assets dictionary
        self.assets[name] = frames

    def load_image(self, file_path, name):
        # Load an image file and convert it to a format suitable for pygame
        img = pygame.image.load(file_path).convert_alpha()
        # Store the image in the assets dictionary
        self.assets[name] = img

    def load_sound(self, file_path, name):
        # Load a sound file using pygame's mixer
        sound = pygame.mixer.Sound(file_path)
        # Store the sound in the assets dictionary
        self.assets[name] = sound

    def load_tileset(self, filepath, name):
        # Load a tileset image and split it into individual tiles
        tileset_image = pygame.image.load(filepath).convert_alpha()
        tile = pygame.Surface((16, 16), pygame.SRCALPHA)
        array = ["1212", "1101", "1010", "1011", "1", "1001", "", "0110", "2121", "0111", "0101", "1110", "0000",
                 "1221", "2", "2112"]
        dictionary = {}  # Dictionary to store tiles with specific keys

        def add_tile(count, position):
            # Extract a tile from the tileset and store it in the dictionary
            tile.fill((0, 0, 0, 0))
            tile.blit(tileset_image, (0, 0), (16 * position[0], 16 * position[1], 16, 16))
            dictionary[array[count]] = [tile.copy()]

        # Iterate over the tileset to extract all tiles
        for i in range(4):
            for j in range(4):
                add_tile(i * 4 + j, (j, i))
        # Store the tileset dictionary in the assets dictionary
        self.assets[name] = dictionary

    def load_music(self, file_path, name):
        # Store the path to a music file in the assets dictionary
        self.assets[name] = file_path