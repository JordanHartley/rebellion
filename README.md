# mcss-a2

Assignment 2, 2022, SWEN90004 Modelling Complex Software Systems

# Instructions

To run our program, simply execute run.sh script from the command line (using bash or sh). To configure the simulation, simply pass relevant command line options to the script.

To see all available options, pass the -H or --help option to the script. Default options can be reconfigured in /utils/params.py.

Verbose output: pass the -v or --verbose option to the script to see the simulation’s configuration and team details before the simulation begins.

Output - raw CSV data: at the conclusion of a simulation output data is stored in a CSV file. The first row are column headers. The second row is the default quiet, active, and jailed agents, as well as the parameters for the simulation. All remaining rows correspond to the number of quiet, active and jailed agents at each tick. Use -p or --no_persist to turn off.

Output - plot: a graph of the simulation output of the simulation, which can be saved as a PNG. Use --plot and/or --save-plot (they can be used separately or together).

Output - visualisation: the entire simulation can be watched tick-by-tick on the commandline. Use -g or --gui.

- Note: if there is an underscore (\_) in front of a cop or an agent that indicates that they are standing on a patch with a jailed agent.

Running our extension: pass the -x (for “extension”) or --communication option to the script to turn on our “agent-to-agent communication” extention.
Deleting output data: .csv and .png data in /output can be cleared by running the tidy-data.sh script in the project root directory. Any files in /output/save will not be deleted by this script.

## Run script

Run the following command:

`sh ./run.sh <OPTIONS>`

## Options

Display the CLI options (--help): use `-H`

`sh ./run.sh -H`

# Team use only: installing dependencies (not required for by marking staff)

Make sure venv is active before installing:

`sh ./install.sh [your-package]`
