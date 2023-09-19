import pandas as pd
from rebellion.rebellion import Rebellion
from typing import TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from simulation.simulation import Simulation


PATH = "output"  # TODO: add to CLI with default
PLOT_PATH = PATH + "/plots"
WITH_INDEX = True
SEPERATOR = ","


class Persistence:
    def __init__(self, simulaiton: "Simulation", rebellion: Rebellion):
        self.rebellion: Rebellion = rebellion
        self.simulation: "Simulation" = simulaiton
        self.full_file = ""
        self.filename = ""
        # TODO: change to dynamic, full-file path using pathlib or os?
        self.plot_path = PLOT_PATH
        self.__create_filename()
        self.__create_file()

    def __create_filename(self) -> None:
        height = self.rebellion.world_height
        width = self.rebellion.world_width
        datetimeformat = "%y-%m-%d_%Hh-%Mm-%Ss"
        now = datetime.now()
        self.filename = now.strftime(f"{datetimeformat}-{height}x{width}")
        self.full_file = f"{PATH}/{self.filename}.csv"

    def __create_file(self) -> None:
        df = pd.DataFrame([[
            self.rebellion.quiet_count,
            self.rebellion.jailed_count,
            self.rebellion.active_count,
            self.rebellion.vision,
            self.rebellion.threshold,
            self.rebellion.k,
            self.rebellion.initial_cop_density,
            self.rebellion.initial_agent_density,
            self.rebellion.movement,
            self.rebellion.government_legitimacy,
            self.rebellion.max_jail,
        ]])
        df.columns = [
            'quiet',
            'jailed',
            'active',
            'vision',
            'threshold',
            'K',
            'cop_density',
            'agent_density',
            'movement',
            'government_legitimacy',
            'max_jail_term'
        ]
        df.to_csv(self.full_file, sep=SEPERATOR,
                  index_label="tick", index=WITH_INDEX)

    def append(self) -> None:
        # TODO: assert file exists before doing anyting
        df = pd.DataFrame([[
            self.rebellion.quiet_count,
            self.rebellion.jailed_count,
            self.rebellion.active_count
        ]], index=[self.rebellion.current_tick()])
        df.to_csv(self.full_file, mode="a", sep=SEPERATOR,
                  header=False, index=WITH_INDEX)
