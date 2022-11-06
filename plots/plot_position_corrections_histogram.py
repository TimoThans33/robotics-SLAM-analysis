#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from arams import Arams
from arams.file_specifications import *
from utils.argument_parser import *
from utils import plot
from datetime import datetime

def plot_position_corrections_histogram(arams, output_folder=None):
    if LDC not in arams:
        print("Could not find logDriftCorrections file.")
        return
    df = arams[LDC]

    error_x = df[LDC.ERROR_X.value].to_list()
    error_y = df[LDC.ERROR_Y.value].to_list()
    corrections_total = len(error_x)

    # Calculate 2-norm of position error
    dist = np.linalg.norm([error_x, error_y], axis=0)

    plt.suptitle("Position corrections (m)", fontweight='bold')
    plt.title(f'Total detected signatures: {corrections_total}')

    # Bin ranges; e.g. [5, 6] --> first bin includes values of 5 but excludes values of 6
    bins_input = [0, 0.025, 0.05, 0.075, 0.10]

    # Combine values outside of bin range in final bin
    dist = np.clip(dist, bins_input[0], bins_input[-1])

    # Generate histogram
    hist_arrays, bins, patches = plt.hist(dist, bins=bins_input, histtype='bar', rwidth=0.75, align='left', log=True)

    # Display count label for each bin
    for i in range(0, len(bins) - 1):
        text = f"{hist_arrays[i] / corrections_total * 100:.2f}%"
        plt.text(bins[i], hist_arrays[i], text,
                 horizontalalignment='center',
                 verticalalignment='baseline',
                 fontweight='bold')

    # Leave out first label and append '+' to last label to emphasize all values above
    xlabels = [str(x) for x in bins[1:]]
    xlabels[-1] += "+"
    plt.xticks(bins[:-1], xlabels)

    plt.xlabel('Position correction L2 norm [m]')
    # Remove y ticks
    plt.yticks([])
    # Relabel the axis as "Frequency"
    plt.ylabel("Frequency (log scale)")

    datetime_today = datetime.today()
    path_string = datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_position_corrections_histogram.png'
    plot.save_or_show(output_folder, path_string)

if __name__ == "__main__":
    args = parse_arguments()
    arams = Arams(args["input"])

    plot_position_corrections_histogram(arams, args["output"] if "output" in args else None)
