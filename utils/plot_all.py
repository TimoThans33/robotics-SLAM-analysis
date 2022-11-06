from arams import Arams
from utils.argument_parser import *

from calculate_time_offset import *
from plot_distance_between_corrections_histogram import *
from plot_distance_between_corrections_map import *
from plot_map_visualization import *

def plot_all_arams(input_paths, output_folder=None):
    scripts = [
        plot_distance_between_corrections_histogram,
        plot_distance_between_corrections_map,
        plot_map_visualization
    ]

    arams = Arams(input_paths)
    LastPowerCycleFilter.filter_all(arams)

    for script in scripts:
        script(arams, output_folder)

def plot_all():
    args = parse_arguments(velocity=False)
    output_folder = args["output"] if "output" in args else None

    print("=" * 6 + " Time offset plots " + "=" * 6)
    time_offset_file = find_time_offset_file(args["input"])
    if time_offset_file:
        calculate_time_offset(time_offset_file, args["velocity"], args["debug"], output_folder)
    else:
        print("Could not find time offset file.")

    print("=" * 6 + " PGO plots " + "=" * 6)
    g2o_file = find_g2o_file(args["input"])
    debug = args["debug"]
    if g2o_file:
        plot_position_jumps_pgo(g2o_file, debug, output_folder)
    else:
        print("Could not find g2o file.")

    print("=" * 6 + " Arams plots " + "=" * 6)
    plot_all_arams(args["input"], output_folder)
    print("=" * 6 + " Done " + "=" * 6)

if __name__ == "__main__":
    plot_all()