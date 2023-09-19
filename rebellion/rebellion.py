import functools
from math import floor
from rebellion.rebellion_turtle import Turtle as RTurtle
from rebellion.agent import Agent
from rebellion.cop import Cop
from pylogo.patch import Patch, PatchFactory
import random
from pylogo import world
from typing import List, Tuple
from colorama import Fore, Back, Style
import pandas as pd
import numpy as np


# DEFAULTS
K = 2.3
THRESHOLD = 0.1
INITIAL_COP_DENSITY = 0.05
INITIAL_AGENT_DENSITY = 0.7
VISION = 7.0
MOVEMENT = True
GOVERNMENT_LEGITIMACY = 0.4
MAX_JAIL_TERM = 30


class Rebellion(world.World):
    '''
    Description of Rebellion class...
    '''

    def __init__(self,
                 k: float,
                 threshold: float,
                 cop_density: float,
                 agent_density: float,
                 vision: float,
                 movement: bool,
                 government_legitimacy: float,
                 max_jail: int,
                 communication: bool = False,
                 ** kwargs):
        super().__init__(**kwargs)
        self.k: float = k
        self.threshold: float = threshold
        self.initial_cop_density: float = cop_density
        self.initial_agent_density: float = agent_density
        self.vision: float = vision
        self.movement: bool = movement
        self.government_legitimacy: float = government_legitimacy
        self.max_jail: int = max_jail
        self.communication = communication
        self.turtles: List[RTurtle] = []
        # check density of cops and agents is does not exceed 100%
        if self.initial_agent_density + self.initial_cop_density > 1:
            raise ValueError("Density of Agents and Cops over 100%")
        self.__init_grid()

    def __init_grid(self):
        assert self.GRID == None, world.WorldError("grid already initialised")
        # initialize the grid - remember that it loops around both horizontally
        # and vertically
        make_patch = PatchFactory(self.vision)
        self.GRID = [make_patch(row, col)
                     for row in range(self.world_height)
                     for col in range(self.world_width)]
        self.GRID = np.array(self.GRID).reshape(
            (self.world_height, self.world_width))

        # populate neighbors
        for row in self.GRID:
            for cell in row:
                cell.set_neighbourhood(self.GRID,
                                       self.world_width,
                                       self.world_height)

        # populate the grid
        empty_spaces = self.__get_empty_spaces()
        cop_count = floor(self.initial_cop_density * self.num_patches)
        agent_count = floor(self.initial_agent_density * self.num_patches)
        for _ in range(cop_count):
            r, c = empty_spaces.pop()
            newCop = Cop(patch=self.GRID[r][c])
            self.GRID[r][c].contents.append(newCop)
            self.turtles.append(newCop)
        for _ in range(cop_count, cop_count + agent_count):
            r, c = empty_spaces.pop()
            newAgent = Agent(self.government_legitimacy,
                             self.GRID[r][c],
                             self.k,
                             self.threshold,
                             communication=self.communication)
            self.GRID[r][c].contents.append(newAgent)
            self.turtles.append(newAgent)

        self.agent_count = agent_count
        self.quiet_count: int = agent_count
        self.active_count: int = 0
        self.jailed_count: int = 0

    def __get_empty_spaces(self) -> Tuple[int, int]:
        empty_spaces = [(r, c)
                        for r in range(self.world_height)
                        for c in range(self.world_width)]
        assert(len(empty_spaces) == self.num_patches)
        random.shuffle(empty_spaces)
        return empty_spaces

    def get_quiet(self) -> List[RTurtle]:
        return [i for i in self.turtles if i.is_agent and i.active == False]

    def get_active(self) -> List[RTurtle]:
        return [i for i in self.turtles if i.is_agent and i.active == True]

    def get_jailed(self) -> List[RTurtle]:
        return [i for i in self.turtles if i.is_agent and i.jail_time > 0]

    def update_agent_counts(self):
        self.active_count = sum(
            1 for t in self.turtles if t.is_agent and t.active)
        self.jailed_count = sum(
            1 for t in self.turtles if t.is_agent and t.jail_time > 0)
        self.quiet_count = sum(
            1 for t in self.turtles if t.is_agent and not t.active) - self.jailed_count
        total_check = self.active_count + self.jailed_count + self.quiet_count
        assert self.agent_count == total_check, "mistake counting agents"

    def on_tick(self):
        """
            1) turtle update: Move, Check rebellion, then cops arrest
            2) tick down jailed agent timer

            3) Update Agent display
        """

        # Step 1: Rule M - move all agents
        if self.movement:
            self.move_agents()

        if self.communication:
            self.agent_communication()

        # Step 2: Rule A - determine behaviour of agents
        self.determine_agents()

        # Step 3: Rule C - enforcement by cops
        self.enforce_cops()

        # Count the agents in each state (quiet, jailed, active)
        self.update_agent_counts()

    def determine_agents(self):
        agents: Agent = [i for i in self.turtles if isinstance(i, Agent)]
        # Check Agent Rebellion
        for agent in agents:
            agent.determine_behaviour(self.k, self.threshold)
            assert agent in agent.patch.contents

    def enforce_cops(self):
        cops = [i for i in self.turtles if isinstance(i, Cop)]
        # Cops arrest active agents
        for cop in cops:
            cop.enforce(self.max_jail)
            assert cop in cop.patch.contents

    def agent_communication(self):
        agents: Agent = [i for i in self.turtles if isinstance(i, Agent)]
        for agent in agents:
            agent.communicate()
        for agent in agents:
            agent.become_open_to_communication()
            assert agent.has_communicated == False

    def move_agents(self):
        for row in self.GRID:
            for cell in row:
                for turt in cell.contents:
                    # Get non-jailed agents and cops
                    if isinstance(turt, Agent) and turt.jail_time < 1:
                        # get the turtle and all empty spaces around it
                        # empty spaces include jailed agents
                        empty = [i for i in cell.neighborhood
                                 if not i.contents or
                                 all((isinstance(x, Agent) and x.jail_time > 0)
                                     for x in i.contents)]

                        # if no empty spaces, don't move
                        if empty:
                            # Move to a random empty space
                            destination = random.choice(empty)

                            # Movement step
                            destination.contents.append(turt)
                            cell.contents.remove(turt)
                            turt.patch = destination
                            # assert len(destination.contents) <= 2

    def __call__(self) -> None:
        return super().__call__()


if __name__ == "__main__":
    raise Exception("Simulation Error: cannot run Rebellion directly")
