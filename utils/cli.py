import argparse
from functools import wraps
from subprocess import run
import pandas as pd
from colorama import Fore, Back, Style
import utils.params as params


class CLIArgs:
    """
      A class for type hinting and storing sensible defaults for CLI arguments.
    """
    # CLI
    verbose: bool = False
    gui: bool = False

    # PERSISTENCE
    no_persist: bool = True

    # SIMULATIONS
    numsimulations: int = 1
    ticks: int = params.MAX_TICKS

    # WORLD
    height: int = params.WORLD_HEIGHT
    width: int = params.WORLD_WIDTH

    # PATCH
    vision: float = params.VISION

    # REBELLION
    threshold: float = params.THRESHOLD
    K: float = params.K
    cop_density: float = params.INITIAL_COP_DENSITY
    agent_density: float = params.INITIAL_AGENT_DENSITY
    movement: float = params.MOVEMENT
    gov_legitimacy: float = params.GOVERNMENT_LEGITIMACY
    max_jail: int = params.MAX_JAIL_TERM

    # Extension(s) to base model
    communication: bool = params.COMMUNICATION

    # PLOT
    plot: bool = False
    save_plot: bool = False


class CLI:
    def __init__(self):
        self.args: CLIArgs = get_args()
        self.__echo_welcome()

    def __echo_welcome(self):
        welcome = f"{Fore.RED}{Back.RED} WELOME TO THE REBELLION, COMMRADE! {Style.RESET_ALL}"
        print(welcome)
        echo_team(self.args.verbose)
        echo_args(self.args.verbose, self.args)
        echo_venv()


def echo_venv():
    print(f"{Fore.BLUE}Using venv:{Style.RESET_ALL}")
    run(["pip", "-V"])
    print()


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=False,  # turn off - use -H for help (see below)
        usage="%(prog)s [HEIGHT] [WIDTH]...",
        description="Print or check SHA1 (160-bit) checksums."
    )
    # Set help option to "-H" instead of "-h" so we can use "-h" for height
    parser.add_argument('-H', "--help", action='help',
                        help='show this help message and exit')
    parser.add_argument('-h', "--height", type=int,
                        default=CLIArgs.height, help="Height of the world")
    parser.add_argument('-w', "--width",  type=int,
                        default=CLIArgs.width, help="Width of the world")
    parser.add_argument('-t', "--ticks",  type=int,
                        default=CLIArgs.ticks, help="Number of ticks in simulation")
    parser.add_argument('-n', "--numsimulations",  type=int,
                        default=CLIArgs.numsimulations, help="Number of simulations")
    parser.add_argument('-v', "--verbose",  action='store_true',
                        help="Verbose output")
    parser.add_argument('-g', "--gui",  action='store_true',
                        help="Display simulation on GUI (default: False)")
    parser.add_argument('-p', "--no-persist", action='store_true',
                        help="Turn off persistence to disk (default: False)")
    parser.add_argument('-T', "--threshold",  type=float,
                        default=CLIArgs.threshold, help="Threshold: how much G > N before an agent rebels")
    parser.add_argument('-K', "--K",  type=float,
                        default=CLIArgs.K, help="K: arrest probability factor")
    parser.add_argument('-C', "--cop-density",  type=float,
                        default=CLIArgs.cop_density, help="Initial cop density")
    parser.add_argument('-A', "--agent-density",  type=float,
                        default=CLIArgs.agent_density, help="Initial agent density")
    parser.add_argument('-V', "--vision",  type=float,
                        default=CLIArgs.vision, help="Turtle (cops, agents) vision")
    parser.add_argument('-M', "--movement",  action='store_true',
                        default=CLIArgs.movement, help="Turn on turtle movement if true otherwise turn off movement (default: False/off)")
    parser.add_argument('-G', "--gov_legitimacy",  type=float,
                        default=CLIArgs.gov_legitimacy, help="Government legitimacy")
    parser.add_argument('-J', "--max_jail",  type=int,
                        default=CLIArgs.max_jail, help="Maximum jail term")
    parser.add_argument("--save-plot",  action='store_true',
                        default=CLIArgs.save_plot, help="Save a plot of CSV data")
    parser.add_argument("--plot",  action='store_true',
                        default=CLIArgs.plot, help="Show a plot of CSV data")

    parser.add_argument("-x", "--communication", action='store_true',
                        default=CLIArgs.communication, help="Turn on the communication extension")

    return parser


def verbose_only(func):
    @wraps(func)
    def wrapper(verbose=False, *args, **kwargs):
        if verbose:
            func(*args, **kwargs)
        return None
    return wrapper


def get_args() -> argparse.Namespace:
    return init_argparse().parse_args()


def get_args_as_dict() -> dict:
    return vars(get_args())


@verbose_only
def echo_team() -> None:
    print(f"{Fore.BLUE}Team:{Style.RESET_ALL}")
    team = [["1335708", "Jordan",  "Hartley"],
            ["583703", "Levi", "McKenzie-Kirkbright"],
            ["1082261", "Kia", "Tan"]]
    team_df = pd.DataFrame(team,
                           columns=['Student ID', 'First name', 'Last name'])
    print(team_df.to_string(index=False))


@verbose_only
def echo_args(args: argparse.Namespace) -> None:
    print(f"{Fore.BLUE}Received arguments:{Style.RESET_ALL}")
    for arg, val in vars(args).items():
        _arg = f"{Fore.YELLOW}{arg}{Style.RESET_ALL}"
        _val = f"{Fore.GREEN}{val}{Style.RESET_ALL}"
        print(f"{_arg}={_val}")
