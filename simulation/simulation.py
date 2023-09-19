from colorama import Fore, Back, Style
from rebellion.rebellion import Rebellion
from view import RebellionView
from persistence import Persistence
from analysis import Analyser


class Simulation:
    _id = 0

    def __init__(self,
                 k: float,
                 threshold: float,
                 cop_density: float,
                 agent_density: float,
                 vision: float,
                 movement: bool,
                 government_legitimacy: float,
                 max_jail: int,
                 communication: bool,
                 height: int,
                 width: int,
                 max_ticks: int,
                 gui: bool,
                 persist: bool,
                 plot: bool = False,
                 save_plot: bool = False):
        self.id = Simulation.get_id()
        self.gui = gui
        self.persist = persist
        self.plot = plot
        self.save_plot = save_plot
        self.rebellion = Rebellion(k=k,
                                   threshold=threshold,
                                   cop_density=cop_density,
                                   agent_density=agent_density,
                                   vision=vision,
                                   movement=movement,
                                   government_legitimacy=government_legitimacy,
                                   max_jail=max_jail,
                                   height=height,
                                   width=width,
                                   max_ticks=max_ticks,
                                   communication=communication)
        if self.persist:
            self.persistence = Persistence(self, self.rebellion)

    @classmethod
    def get_id(cls):
        cls._id += 1
        return cls._id

    def __call__(self):
        print(f"{Fore.WHITE}{Back.MAGENTA}Simulation #{self.id}{Style.RESET_ALL}")

        if self.gui:
            print(
                f"{Fore.WHITE}{Back.BLUE} INIT STATE {Style.RESET_ALL}")
            RebellionView.grid(self.rebellion)

        for _ in self.rebellion.go_iter():
            if self.persist:
                self.persistence.append()
            if self.gui:
                RebellionView.tick_message(self.rebellion)
                RebellionView.grid(self.rebellion)

        if self.persist and self.plot or self.save_plot:
            analyser = Analyser(self.rebellion,
                                self.persistence.full_file,
                                self.persistence.plot_path,
                                self.persistence.filename)
            analyser(self.plot, self.save_plot)


class SimulationFactory:
    def __init__(self,
                 height: int,
                 width: int,
                 max_ticks: int,
                 gui: bool,
                 persist: bool,
                 plot: bool = False,
                 save_plot: bool = False) -> None:
        self.height: int = height
        self.width: int = width
        self.max_ticks: int = max_ticks
        self.gui = gui
        self.persist = persist
        self.plot = plot
        self.save_plot = save_plot

    def create(self,
               k: float,
               threshold: float,
               cop_density: float,
               agent_density: float,
               vision: float,
               movement: bool,
               government_legitimacy: float,
               max_jail: int,
               communication: bool
               ) -> Simulation:
        return Simulation(
            k,
            threshold,
            cop_density,
            agent_density,
            vision,
            movement,
            government_legitimacy,
            max_jail,
            communication,
            self.height,
            self.width,
            self.max_ticks,
            self.gui,
            self.persist,
            self.plot,
            self.save_plot)
