import random
from rebellion.rebellion_turtle import Turtle
from rebellion.agent import Agent


class Cop(Turtle):
    '''
    Description of Cop class...
    '''

    def __init__(self, patch):
        super().__init__(colour="red", highlight=True, patch=patch)
        self.make_cop()

    def enforce(self, max_jail):
        def is_arrestable(turtle: Turtle) -> bool:
            return turtle.is_agent and turtle.active and turtle.jail_time == -1

        arrestable_indexes = []
        for n, neighbour in enumerate(self.patch.neighborhood):
            for t, turt in enumerate(neighbour.contents):
                if is_arrestable(turt):
                    arrestable_indexes.append((n, t))

        # if we have any active agents, arrest them
        if len(arrestable_indexes) > 0:
            # print("ARRESTING!")
            patch, turtle = random.choice(arrestable_indexes)
            jailTime: float = random.randint(1, max_jail)
            self.patch.neighborhood[patch].contents[turtle].set_jail_time(
                jailTime)
            assert self.patch.neighborhood[patch].contents[turtle].active == False
            assert self.patch.neighborhood[patch].contents[turtle].jail_time > 0

            destination = self.patch.neighborhood[patch].contents[turtle].patch
            current = self.patch
            # print("OFF TO JAIL, SCUM!", destination.contents, jailTime,
            #       destination.row, destination.col)
            destination.contents.append(self)
            current.contents.remove(self)
            self.patch = destination
