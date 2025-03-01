from Code.Variables.SettingVariables import *
import pygame
import numpy as np
import logging
from typing import Optional, List

class SoundManager:
    def __init__(self, game):
        """Initialize the SoundManager with game instance and audio settings."""
        self.game = game
        self.logger = logging.getLogger(__name__)  # Setup logging for debugging
        pygame.mixer.init()  # Initialize Pygame mixer
        self.current_music: Optional[str] = None  # Track current music
        self.music_queue: List[str] = []  # Queue for background music
        self.music_volume: float = VOLUMES["music_volume"] * self.game.master_volume  # Initial music volume
        self.sound_pool: dict = {}  # Cache for sound objects
        self.update()  # Set initial volume state

    def load_sound(self, sound_path: str) -> Optional[pygame.mixer.Sound]:
        """Safely load a sound file with error handling."""
        try:
            if sound_path not in self.sound_pool:
                self.sound_pool[sound_path] = pygame.mixer.Sound(sound_path)
            return self.sound_pool[sound_path]
        except FileNotFoundError:
            self.logger.error(f"Sound file not found: {sound_path}")
            return None

    def play_music(self, music_path: str, loop: int = -1, volume: float = 1.0):
        """Play background music with looping and volume control."""
        if self.current_music != music_path:
            music = self.load_sound(music_path)
            if music:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(loop)
                pygame.mixer.music.set_volume(self.music_volume * volume)
                self.current_music = music_path
                self.logger.info(f"Playing music: {music_path}")

    def fade_music(self, fade_out_ms: int, next_music: Optional[str] = None, next_music_volume: float = 1.0):
        """Fade out current music and optionally play the next track."""
        pygame.mixer.music.fadeout(fade_out_ms)
        if next_music:
            self.play_music(next_music, volume=next_music_volume)

    def play_sound(self, sound_key: str, frequency_variation: float = 0.0, volume: float = 1.0):
        """Play a sound effect with optional pitch variation and volume."""
        sound = self.game.assets.get(sound_key)  # Safely fetch sound from game assets
        if not sound:
            self.logger.warning(f"Sound not found in assets: {sound_key}")
            return

        # Apply frequency variation if specified
        if frequency_variation > 0:
            sound_array = pygame.sndarray.array(sound)
            variation = np.random.uniform(1 - frequency_variation, 1 + frequency_variation)
            resampled = self.resample(sound_array, variation)
            sound = pygame.sndarray.make_sound(resampled)

        sound.set_volume(volume)
        sound.play()
        self.logger.debug(f"Playing sound: {sound_key}")

    @staticmethod
    def resample(sound_array: np.ndarray, factor: float) -> np.ndarray:
        """Resample a sound array by a given factor for pitch variation."""
        sound_array = sound_array.astype(float)
        num_channels = sound_array.shape[1]
        new_length = int(sound_array.shape[0] / factor)
        resampled = np.zeros((new_length, num_channels), dtype=np.int16)

        for channel in range(num_channels):
            channel_data = sound_array[:, channel]
            old_indices = np.arange(len(channel_data))
            new_indices = np.linspace(0, len(channel_data) - 1, new_length)
            resampled[:, channel] = np.interp(new_indices, old_indices, channel_data).astype(np.int16)

        return resampled

    def update(self):
        """Update music volume based on game settings."""
        if self.game.music:
            self.music_volume = VOLUMES["music_volume"] * self.game.master_volume
        else:
            self.music_volume = 0
        if self.current_music:
            pygame.mixer.music.set_volume(self.music_volume)

    def queue_music(self, music_path: str, volume: float = 1.0):
        """Add a music track to the queue."""
        self.music_queue.append((music_path, volume))
        self.logger.info(f"Queued music: {music_path}")

    def play_next_in_queue(self):
        """Play the next track in the music queue."""
        if self.music_queue:
            next_music, volume = self.music_queue.pop(0)
            self.play_music(next_music, volume=volume)
            self.logger.info(f"Playing next in queue: {next_music}")

    def set_volume(self, music_volume: float, master_volume: float):
        """Adjust music and master volume dynamically."""
        VOLUMES["music_volume"] = music_volume
        self.game.master_volume = master_volume
        self.update()
        self.logger.debug(f"Volume updated - Music: {music_volume}, Master: {master_volume}")
