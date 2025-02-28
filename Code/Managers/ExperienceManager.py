from Code.DataStructures.HashMap import HashMap
from Code.Individuals.Experience import Experience
from typing import Any, Set


class ExperienceManager:
          """
          Manages Experience objects within the game using a spatial HashMap.
          It supports recycling of Experience objects via an object pool,
          minimizing instantiation overhead.
          """

          def __init__(self, game: Any) -> None:
                    """
                    Initializes the ExperienceManager.

                    Args:
                        game: The main game instance.
                    """
                    self.game = game
                    # Initialize the grid with settings from the global GENERAL dict.
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][7])
                    # Pool to store recycled Experience instances.
                    self.pool: Set[Experience] = set()

          def add_experience(self, name: str, location: Any) -> None:
                    """
                    Adds an experience object at the specified location with the given name.
                    If a recycled Experience is available, reinitialize it; otherwise, create a new one.

                    Args:
                        name: The identifier for the experience.
                        location: The spatial location where the experience should appear.
                    """
                    if self.pool:
                              xp = self.pool.pop()
                              xp.reset(location, name)
                    else:
                              xp = Experience(self.game, location, name)
                    self.grid.insert(xp)

          def update(self) -> None:
                    """
                    Updates all Experience objects in the grid.
                    For each experience, calls its update method; if it has been collected,
                    removes it from the grid and adds it to the recycling pool.
                    Finally, rebuilds the grid to ensure spatial consistency.
                    """
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

                    def add_experience(self, name, location):
                              if bool(self.pool):
                                        xp = self.pool.pop()
                                        xp.reset(location, name)
                              else:
                                        xp = Experience(self.game, location, name)
                              self.grid.insert(xp)

                    def update(self):
                              if not self.game.changing_settings and not self.game.cards_on:
                                        for xp in self.grid.items.copy():
                                                  xp.update()
                                                  if xp.is_collected and xp in self.grid.items:
                                                            try:
                                                                      self.grid.remove(xp)
                                                            except ValueError:
                                                                      pass
                                                            self.pool.add(xp)
                                        self.grid.rebuild()
