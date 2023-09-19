import pandas as pd
import matplotlib.pyplot as plt
from persistence import Persistence
from rebellion.rebellion import Rebellion

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True


class Analyser:
    def __init__(self, rebellion: Rebellion, full_file: str, plot_path: str, plot_fname: str) -> None:
        print(f"analysing: {full_file}")
        self.plot_path: str = plot_path
        self.plot_fname: str = plot_fname
        headers = ['tick', 'quiet', 'jailed', 'active']
        df = pd.read_csv(full_file, usecols=headers)
        self.df = df.set_index('tick')
        # plt.figure()
        self.fig, self.ax = plt.subplots()
        self.df.plot(ax=self.ax)

        textstr = '\n'.join((
            f'World={rebellion.world_height}h x {rebellion.world_width}w',
            f'ticks={rebellion._max_ticks}',
            f'threshold={rebellion.threshold}',
            f'K={rebellion.k}',
            f'cop density={rebellion.initial_cop_density}',
            f'agent density={rebellion.initial_agent_density}',
            f'vision={rebellion.vision}',
            f'movement={rebellion.movement}',
            f'government legitimacy={rebellion.government_legitimacy}',
            f'max jail term={rebellion.max_jail}',
            f'communication (extension)={rebellion.communication}',
        ))
        props = dict(boxstyle='square', facecolor='#ffcfdc', alpha=0.8)
        self.ax.text(-0, -0.2, textstr, transform=self.ax.transAxes, fontsize=8,
                     verticalalignment='top', bbox=props)

    def __call__(self, plot: bool = False, save_plot: bool = False) -> None:
        if save_plot:
            save_as = f"{self.plot_path}/{self.plot_fname}.png"
            plt.savefig(save_as, bbox_inches='tight')
        if plot:
            plt.show()
