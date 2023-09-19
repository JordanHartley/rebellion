import pandas as pd
from tabulate import tabulate
from colorama import Fore, Back, Style


from pylogo.patch import Patch
from rebellion.rebellion import Rebellion
from rebellion.agent import Agent


def colourise_turtle(turt):
    if (isinstance(turt, Agent)):
        return f"{Back.RED + '[' if turt.in_jail else ''}{repr(turt)}{']' + Style.RESET_ALL if turt.in_jail else ''}"
    else:
        return f"{Back.BLUE}{repr(turt)}{Style.RESET_ALL}"  # cop


class PatchView:
    @classmethod
    def agent_str(cls, contents, padding=5) -> str:
        # select non-jailed agents, if possible

        if (len(contents) == 0):  # empty patch
            return "     "
        if (len(contents) == 1):
            turt = contents[0]
            turt_str = colourise_turtle(turt)
            return turt_str
        # something standing on a jailed agent
        if (len(contents) >= 2):
            turt = contents[-1]
            turt_str = colourise_turtle(turt)
            return "_" + turt_str


class RebellionView:
    @classmethod
    def tick_message(cls, r: Rebellion):
        print(f"{Fore.WHITE}{Back.BLUE} Tick #{r.current_tick()} {Style.RESET_ALL}")

    @classmethod
    def grid(cls, rebellion: Rebellion):
        grid = [[PatchView.agent_str(rebellion.GRID[row][col].contents)
                for col in range(rebellion.world_width)]
                for row in range(rebellion.world_height)]
        df = pd.DataFrame(grid)
        df.columns = [_ for _ in range(len(rebellion.GRID[0]))]
        df.style.set_properties(**{'text-align': 'right'})
        print(tabulate(df, showindex=True, headers=df.columns))
        print()
