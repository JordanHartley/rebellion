from __future__ import annotations
from random import choice
from pylogo.logo_agent import LogoAgent
from pylogo.turtle import Turtle
from typing import List
from math import sqrt

from rebellion.agent import Agent
from rebellion.cop import Cop


class Patch(LogoAgent):
    '''
    A patch is a space that contains an agent or a cop.
    The only reason why they're a class is because they contain a set of
    other patches within their vision radius
    '''

    def __init__(self, row: int, col: int, vision: float):
        self.row: int = row
        self.col: int = col
        self.neighborhood = []
        self.contents = []
        self.vision: float = vision

    def add_neighbour(self, patch):
        self.neighborhood.append(patch)

    def set_neighbourhood(self, patches: List[Patch], world_width: int, world_height: int) -> None:
        # Use circular radius
        for row_i in range(int(-self.vision), int(self.vision)+1):
            for col_i in range(int(-self.vision), int(self.vision)+1):
                if ((row_i != 0 or col_i != 0) and
                        self.vision >= sqrt((row_i ** 2 + col_i ** 2))):
                    if ((self.row + row_i < 0) or
                            (self.row + row_i >= world_height)):
                        # Wrap around vertically
                        row_neighbour = (self.row+row_i) % world_height
                    else:
                        row_neighbour = self.row + row_i

                    if ((self.col + col_i < 0) or
                            (self.col + col_i >= world_width)):
                        # Wrap around horizontally
                        col_neighbour = (self.col + col_i) % world_width
                    else:
                        col_neighbour = self.col + col_i
                    self.add_neighbour(patches[row_neighbour][col_neighbour])

    def selectNeighbor(self):
        return choice(self.neighborhood)

    def __repr__(self) -> str:
        return f"Patch({self.contents}, row={self.row}, col={self.col})"

    def countActiveAgents(self):
        count = 0
        for cell in self.neighborhood:
            for turt in cell.contents:
                if isinstance(turt, Agent) and \
                        turt.active == True:
                    count += 1
        return count

    def countCops(self):
        count = 0
        for cell in self.neighborhood:
            for turt in cell.contents:
                if isinstance(turt, Cop):
                    count += 1
        return count


class PatchFactory:
    def __init__(self, vision: float) -> None:
        self.vision: float = vision

    def __call__(self, row: int, col: int,) -> Patch:
        return Patch(row, col, vision=self.vision)
