from Code.Variables.SettingVariables import *


class HashMap:
    def __init__(self, game, size):
        self.grid = {}  # Dictionary to store grid cells
        self.items = set()  # Set to store all items
        self.game = game  # Reference to the game object
        self.size = size  # Size of each grid cell

    def rebuild(self):
        self.grid = {}  # Clear the grid
        for item in self.items: self.insert(item)  # Reinsert all items

    def _rect_cells(self, rect):
        x1, y1 = rect.topleft
        x1 //= self.size  # Calculate top-left cell
        y1 //= self.size
        x2, y2 = rect.bottomright
        x2 = x2 // self.size + 1  # Calculate bottom-right cell
        y2 = y2 // self.size + 1
        return product(range(x1, x2), range(y1, y2))  # Return all cells in range

    def insert(self, entity):
        self.items.add(entity)  # Add entity to items set
        for cell in self._rect_cells(entity.rect):
            items = self.grid.get(cell)
            if items is None:
                self.grid[cell] = [entity]  # Create new cell if needed
            else:
                items.append(entity)  # Add entity to existing cell

    def query(self, rect):
        items = set()  # Set to store query results
        for cell in self._rect_cells(rect): items.update(self.grid.get(cell, ()))  # Get items in cells
        return items

    def remove(self, entity):
        self.items.remove(entity)  # Remove entity from items set
        for cell in self._rect_cells(entity.rect):
            items = self.grid.get(cell)
            if items is not None: items.remove(entity)  # Remove entity from cells

    def window_query(self):
        items = set()  # Set to store visible items
        for cell in self._rect_cells(self.game.cameraM.rect): items.update(self.grid.get(cell, ()))  # Get visible items
        return items
