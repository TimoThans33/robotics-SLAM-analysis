#!/usr/bin/env python3

from arams import Arams
from arams.filter import *
from utils.argument_parser import *
from plots.plot_map_visualization import *
from plots.plot_distance_between_corrections_map import * 
from plots.plot_distance_between_corrections_histogram import *
from plots.plot_position_corrections_map import *
from plots.plot_position_corrections_histogram import *
from plots.plot_heading_corrections_histogram import *
from plots.plot_heading_corrections_map import *
from plots.plot_distance_between_signatures_map import *
from plots.plot_position_jumps_pgo import *

def plot_all_arams(input_paths, output_folder=None):
    scripts = [
        plot_distance_between_corrections_map,
        plot_map_visualization,
        plot_distance_between_corrections_histogram,
        plot_position_corrections_map,
        plot_position_corrections_histogram,
        plot_heading_corrections_histogram,
        plot_heading_corrections_map,
        plot_distance_between_signatures_map
    ]

    arams = Arams(input_paths)
    LastPowerCycleFilter.filter_all(arams)

    for script in scripts:
        script(arams, output_folder)

if __name__ == "__main__":
    args = parse_arguments()
    output_folder = args["output"] if "output" in args else None

    print("=" * 6 + " PGO plots " + "=" * 6)
    g2o_file = find_g2o_file(args["input"])
    debug = args["debug"]
    if g2o_file:
        plot_position_jumps_pgo(g2o_file, debug, output_folder)
    else:
        print("Could not find g2o file.")

    plot_all_arams(args["input"], output_folder)