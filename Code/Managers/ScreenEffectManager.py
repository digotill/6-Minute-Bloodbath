from Code.Variables.SettingVariables import *
from Code.Individuals.ScreenEffect import ScreenEffect
import pygame
from typing import Optional, Dict, Callable

class ScreenEffectManager:
    def __init__(self, game):
        """Initialize the ScreenEffectManager with a reference to the game instance."""
        self.game = game
        self._initialize_effects()
        self._initialize_state()

    def _initialize_effects(self):
        """Initialize all screen effects with their assets and animation speeds."""
        assets = self.game.assets
        self.effects: Dict[str, ScreenEffect] = {
            "transition": ScreenEffect(self.game, assets["transition_screeneffect"], GENERAL['animation_speeds'][1]),
            "you_died": ScreenEffect(self.game, assets["youdied_screeneffect"], GENERAL['animation_speeds'][2]),
            "you_won": ScreenEffect(self.game, assets["youwin_screeneffect"], GENERAL['animation_speeds'][2]),
            "blood": ScreenEffect(self.game, assets["blood_screeneffect"], GENERAL['animation_speeds'][6]),
        }

    def _initialize_state(self):
        """Initialize state variables for managing active effects."""
        self.active_effects: Dict[str, dict] = {}  # Tracks active effects and their states
        self.transition_direction = 1  # 1 for forward, -1 for reverse

    def start_effect(self, effect_name: str, duration: Optional[float] = None, callback: Optional[Callable] = None):
        """Start an effect with an optional duration and completion callback."""
        if effect_name not in self.effects:
            return
        self.active_effects[effect_name] = {
            "start_time": self.game.game_time,
            "duration": duration,
            "callback": callback,
            "frame": 0 if effect_name != "transition" else self.effects["transition"].length
        }
        if effect_name == "transition":
            self.transition_direction = -1 if self.game.in_menu else 1
        self._handle_audio_for_effect(effect_name)

    def _handle_audio_for_effect(self, effect_name: str):
        """Play audio associated with specific effects."""
        if effect_name == "you_died":
            pygame.mixer.music.stop()
            self.game.soundM.play_sound("youdied_sound", VOLUMES["youdied_frequancy"], VOLUMES["youdied_volume"] * self.game.master_volume)
        elif effect_name == "you_won":
            pygame.mixer.music.stop()
            self.game.soundM.play_sound("youwon_sound", VOLUMES["youwon_frequancy"], VOLUMES["youwon_volume"] * self.game.master_volume)

    def update(self):
        """Update the state of all active effects."""
        current_time = self.game.game_time
        for name, state in list(self.active_effects.items()):
            effect = self.effects[name]
            elapsed = current_time - state["start_time"]

            # Remove effect if duration is exceeded
            if state["duration"] and elapsed > state["duration"]:
                if state["callback"]:
                    state["callback"]()
                del self.active_effects[name]
                continue

            # Handle specific effect updates
            if name == "transition":
                effect.frame += self.transition_direction
                if self.transition_direction > 0 and effect.frame >= effect.length:
                    effect.frame = effect.length
                    self._end_effect(name, state["callback"])
                elif self.transition_direction < 0 and effect.frame <= 0:
                    effect.frame = 0
                    self._end_effect(name, state["callback"])

            elif name in ["you_died", "you_won"]:
                effect.alpha = min(max(elapsed / state["duration"], 0), 1) * 255

            elif name == "blood":
                if elapsed < BLOOD["blood_effect_duration"]:
                    effect.frame += 1
                    if effect.frame > effect.length:
                        effect.frame = effect.length
                else:
                    effect.frame -= 1
                    if effect.frame < 0:
                        del self.active_effects[name]

    def _end_effect(self, effect_name: str, callback: Optional[Callable]):
        """End an effect and execute its callback if provided."""
        if callback:
            callback()
        if effect_name in self.active_effects:
            del self.active_effects[effect_name]

    def draw(self):
        """Draw all active effects and update their states."""
        self.game.uiM.draw_xp_bar()  # Draw XP bar under effects
        self.update()

        for name, state in self.active_effects.items():
            effect = self.effects[name]
            if name == "transition":
                effect.draw(speed=1 if self.transition_direction > 0 else -1)
            else:
                effect.draw()

        # Draw blood effect when dead, outside of active effects for layering
        if self.game.died and not self.game.won and "blood" not in self.active_effects:
            self.effects["blood"].frame = self.effects["blood"].length
            self.effects["blood"].draw()

    ### Public Trigger Methods ###
    def trigger_transition(self, reverse: bool = False, callback: Optional[Callable] = None):
        """Trigger a transition effect with optional reverse direction."""
        self.transition_direction = -1 if reverse else 1
        self.start_effect("transition", callback=callback)

    def trigger_you_died(self, duration: float = 3):
        """Trigger the 'You Died' effect."""
        if "you_died" not in self.active_effects:
            self.start_effect("you_died", duration=duration)

    def trigger_you_won(self, duration: float = 3):
        """Trigger the 'You Won' effect with difficulty-based win increments."""
        if "you_won" not in self.active_effects:
            self.start_effect("you_won", duration=duration, callback=self._on_you_won_complete)

    def trigger_blood_effect(self):
        """Trigger the blood effect."""
        if "blood" not in self.active_effects:
            self.start_effect("blood", duration=BLOOD["blood_effect_duration"])

    def _on_you_won_complete(self):
        """Handle logic when 'You Won' effect completes."""
        if self.game.difficulty == "easy":
            self.game.wins += 1
        elif self.game.difficulty == "medium":
            self.game.wins += 2
        elif self.game.difficulty == "hard":
            self.game.wins += 3

    ### Game State Integration ###
    def handle_game_state(self):
        """Handle effects based on current game state."""
        if self.game.died and not self.game.won:
            self.trigger_you_died()
        elif self.game.won:
            self.trigger_you_won()
        if self.game.playing_transition:
            self.trigger_transition(reverse=self.game.in_menu, callback=self._on_transition_complete)

    def _on_transition_complete(self):
        """Handle transition completion logic."""
        if self.game.in_menu:
            self.game.in_menu = False
        self.game.playing_transition = False
