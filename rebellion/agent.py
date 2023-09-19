import random
import math
import statistics
from rebellion.rebellion_turtle import Turtle


class Agent(Turtle):
    '''
    Description of Agent class...
    '''

    def __init__(self, gov_legitimacy, patch, k, threshold, communication=False):
        super().__init__(colour="blue", patch=patch)
        self.k = k
        self.threshold = threshold
        self.active = False
        self.jail_time = 0
        self.in_jail = False
        self.communication = communication  # toggle communication functionality
        # keep track of whether this agent has had a conversation in the current tick
        self.has_communicated = False
        # control the effect that communication has on the two participants
        # self.chatter_func = self.randomise_chatter_func
        self.chatter_func = statistics.mean

        self.risk_aversion = random.uniform(0, 1)
        self.perceived_hardship = random.uniform(0, 1)

        self.cops_in_vision = 0 	# define a radius check method later
        self.active_agents_in_vision = 0 	# define a radius check method later

        self.grievance = self.perceived_hardship * (1 - gov_legitimacy)

    def randomise_chatter_func(self, grievances):
        def maximise(grievances):
            return 1

        def minimise(grievances):
            return 0

        funcs = [max, min, statistics.mean, maximise, minimise]
        # funcs = [max, min, statistics.mean]
        return random.choice(funcs)(grievances)

    def determine_behaviour(self, k, threshold):
        # count active agents and cops
        self.cops_in_vision = self.patch.countCops()
        self.active_agents_in_vision = self.patch.countActiveAgents()

        estimated_arrest_probability = self.calc_net_risk(k)
        activate = (self.grievance - estimated_arrest_probability) > threshold
        if not self.active and not self.in_jail:
            if activate:
                self.active = True
                self.jail_time = -1
                assert self.active
        elif self.in_jail:
            self.tick_jail_time()

    def communicate(self):
        # prevent an agent from communicating twice in a single tick
        if self.in_jail or self.has_communicated:
            return

        def can_communicate(turtle: Turtle) -> bool:
            return turtle.is_agent \
                and not turtle.in_jail \
                and not turtle.has_communicated

        conversation_indexes = []
        for n, neighbour in enumerate(self.patch.neighborhood):
            for t, turt in enumerate(neighbour.contents):
                if can_communicate(turt):
                    conversation_indexes.append((n, t))

        if len(conversation_indexes) > 0:
            assert self.has_communicated == False
            patch, turtle = random.choice(conversation_indexes)
            assert self.patch.neighborhood[patch].contents[turtle].has_communicated == False

            # make them both active
            # if self.active or self.patch.neighborhood[patch].contents[turtle].active:
            #     self.active = True
            #     self.patch.neighborhood[patch].contents[turtle].active = True

            self.patch \
                .neighborhood[patch] \
                .contents[turtle] \
                .communicate_with(self)
            assert self.patch.neighborhood[patch].contents[turtle].has_communicated == True
            assert self.has_communicated == True

    def communicate_with(self, other):
        assert other.__class__.__name__ == "Agent", f"Exepected Agent, received {other.__class__.__name__}"
        self.has_communicated = True
        other.has_communicated = True
        # TODO: dynamically change chatter function?
        new_grievance = self.chatter_func(
            [self.grievance, other.grievance])

        self.grievance = new_grievance
        other.grievance = new_grievance

    def become_open_to_communication(self):
        self.has_communicated = False

    def calc_net_risk(self, k):
        c_on_a = (self.cops_in_vision // (self.active_agents_in_vision + 1))
        return self.risk_aversion * (1 - math.exp(-k * c_on_a))

    def set_jail_time(self, ticks):
        self.jail_time = ticks
        self.active = False
        self.in_jail = True

    def tick_jail_time(self):
        assert not self.active
        assert self.jail_time != -1
        assert self.in_jail
        if self.jail_time > 0:
            self.jail_time -= 1
        elif self.jail_time == 0:
            self.in_jail = False
            self.active = False
