from Code.Variables.SettingVariables import *

class SoundManager:
          def __init__(self, game):
                    self.game = game
                    pygame.mixer.init()
                    self.current_music = None
                    self.update()

          def play_music(self, music_path, loop=-1, volume=1):
                    if self.current_music != music_path:
                              pygame.mixer.music.load(music_path)
                              pygame.mixer.music.play(loop)
                              pygame.mixer.music.set_volume(self.music_volume * volume)
                              self.current_music = music_path

          def fade_music(self, fade_out_ms, next_music=None, next_music_volume=1):
                    pygame.mixer.music.fadeout(fade_out_ms)
                    if next_music:
                              self.play_music(next_music, volume=next_music_volume)

          def play_sound(self, sound, frequency_variation=0, volume=1):
                    sound = self.game.assets[sound]

                    if frequency_variation > 0:
                              # Apply random frequency variation
                              variation = np.random.uniform(1 - frequency_variation, 1 + frequency_variation)
                              # Convert sound to numpy array
                              sound_array = pygame.sndarray.array(sound)
                              # Resample the sound array
                              resampled = self.resample(sound_array, variation)
                              # Create a new Sound object from the resampled array
                              sound = pygame.sndarray.make_sound(resampled)

                    sound.set_volume(volume)
                    sound.play()

          @staticmethod
          def resample(sound_array, factor):
                    """Resample a sound array by a given factor."""
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
                    if self.game.music:
                              self.music_volume = VOLUMES["music_volume"] * self.game.master_volume
                    else:
                              self.music_volume = 0
                    pygame.mixer.music.set_volume(self.music_volume)
