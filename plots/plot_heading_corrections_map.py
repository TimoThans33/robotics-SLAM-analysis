#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from arams import Arams
from arams.file_specifications import *
from utils.argument_parser import *
from utils import plot
from datetime import datetime

def plot_heading_corrections_map(arams, output_folder=None):
    if LDC not in arams:
        print("Could not find logDriftCorrections file.")
        return
    df = arams[LDC]

    error_theta = df[LDC.ERROR_THETA.value].to_list()
    new_pos_x = df[LDC.NEW_XPOS.value].to_list()
    new_pos_y = df[LDC.NEW_YPOS.value].to_list()

    # Calculate 2-norm of heading error
    dist = np.rad2deg(np.absolute(error_theta))

    plt.suptitle("Heading corrections (deg)", fontweight='bold')
    plt.title('Total detected signatures: %i' % len(error_theta))

    plot.add_map_coordinates(arams)

    cm = LinearSegmentedColormap.from_list("", ["green", "yellow", "red"])

    plt.scatter(new_pos_x, new_pos_y, c=dist, s=dist * 20, label="Markers", cmap=cm)
    plt.gca().set_aspect('equal', adjustable='datalim')
    plt.xlabel("X-axis (m)")
    plt.ylabel("Y-axis (m)")
    plt.grid()

    cbar = plt.colorbar(ticks=np.linspace(dist.min(), dist.max(), 10))
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    datetime_today = datetime.today()
    path_string = datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_heading_corrections_map.png'
    plot.save_or_show(output_folder, path_string)

if __name__ == "__main__":
    args = parse_arguments()
    plot_heading_corrections_map(Arams(args["input"]), args["output"] if "output" in args else None)
