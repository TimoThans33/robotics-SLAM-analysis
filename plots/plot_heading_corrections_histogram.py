#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from arams import Arams
from arams.file_specifications import *
from utils.argument_parser import *
from utils import plot
from datetime import datetime

def plot_heading_corrections_histogram(arams, output_folder=None):
    if LDC not in arams:
        print("Could not find logDriftCorrections file.")
        return
    df = arams[LDC]

    error_theta = df[LDC.ERROR_THETA.value].to_list()
    corrections_total = len(error_theta)

    # Calculate 2-norm of Heading error
    dist = np.rad2deg(np.absolute(error_theta))

    plt.suptitle("Heading corrections (deg)", fontweight='bold')
    plt.title(f'Total detected signatures: {corrections_total}')

    # Bin ranges; e.g. [5, 6] --> first bin includes values of 5 but excludes values of 6
    bins_input = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20]

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

    plt.xlabel('Heading correction L2 norm (deg)')
    # Remove y ticks
    plt.yticks([])
    # Relabel the axis as "Frequency"
    plt.ylabel("Frequency (log scale)")

    datetime_today = datetime.today()
    path_string = datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_heading_corrections_histogram.png'
    plot.save_or_show(output_folder, path_string)

if __name__ == "__main__":
    args = parse_arguments()
    arams = Arams(args["input"])

    plot_heading_corrections_histogram(arams, args["output"] if "output" in args else None)
