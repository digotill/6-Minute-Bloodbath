from Code.DataStructures.HashMap import HashMap
from Code.Individuals.Experience import Experience
from Code.Variables.SettingVariables import *
from typing import Any, Set


class ExperienceManager:
    def __init__(self, game: Any) -> None:

        self.game = game
        # Initialize the grid with settings from the global GENERAL dict.
        self.grid = HashMap(self.game, GENERAL["hash_maps"][7])
        # Pool to store recycled Experience instances.
        self.pool: Set[Experience] = set()

    def add_experience(self, name: str, location: Any) -> None:

        if self.pool:
            xp = self.pool.pop()
            xp.reset(location, name)
        else:
            xp = Experience(self.game, location, name)
        self.grid.insert(xp)

    def update(self) -> None:

        if not self.game.changing_settings:
            # Iterate over a copy of the grid items to allow safe removal.
            for xp in self.grid.items.copy():
                xp.update()
                if xp.is_collected and xp in self.grid.items:
                    try:
                        self.grid.remove(xp)
                    except ValueError as err:
                        # Log the error and continue processing.
                        print(f"Warning: Failed to remove collected experience: {err}")
                    self.pool.add(xp)
            self.grid.rebuild()
