from utils.cli import CLI, CLIArgs
from .simulation import Simulation, SimulationFactory

factory: SimulationFactory


def run_simulations(
        k: float,
        threshold: float,
        cop_density: float,
        agent_density: float,
        vision: float,
        movement: float,
        government_legitimacy: float,
        max_jail: int,
        communication: bool,
        n: int,
        height: int,
        width: int,
        ticks: int,
        gui: bool,
        persist: bool,
        plot: bool = False,
        save_plot: bool = False) -> None:
    factory = SimulationFactory(
        height, width, ticks, gui, persist, plot, save_plot)
    sim: Simulation
    for _ in range(n):
        sim = factory.create(
            k,
            threshold,
            cop_density,
            agent_density,
            vision,
            movement,
            government_legitimacy,
            max_jail,
            communication)
        sim()
