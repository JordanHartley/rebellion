from simulation import run_simulations
from utils.cli import CLI, CLIArgs

if __name__ == "__main__":
    cli: CLI = CLI()
    args: CLIArgs = cli.args
    run_simulations(args.K,
                    args.threshold,
                    args.cop_density,
                    args.agent_density,
                    args.vision,
                    args.movement,
                    args.gov_legitimacy,
                    args.max_jail,
                    args.communication,
                    args.numsimulations,
                    args.height,
                    args.width,
                    args.ticks,
                    args.gui,
                    not args.no_persist,
                    args.plot,
                    args.save_plot)
