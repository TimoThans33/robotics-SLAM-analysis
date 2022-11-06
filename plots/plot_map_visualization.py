#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

from arams import Arams
from arams.file_specifications import *
from utils.argument_parser import *
from utils import plot
from datetime import datetime


def plot_map_visualization(arams, output_folder=None):
    if FMC not in arams:
        print("Could not find floor_map_coordinates file.")
        return
    df = arams[FMC]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[14, 6])
    fig.suptitle("Map visualization")

    ax.set_xlabel("X-axis (m)")
    ax.set_ylabel("Y-axis (m)")

    cluster_ids_distinct = df[FMC.CLUSTER_ID.value].unique()
    colors = iter(cm.rainbow(np.linspace(0, 1, len(cluster_ids_distinct))))

    for cluster_id in cluster_ids_distinct:
        df_filtered = df[df[FMC.CLUSTER_ID.value] == cluster_id]
        x_pos = df_filtered[FMC.SIG_POS_X.value]
        y_pos = df_filtered[FMC.SIG_POS_Y.value]

        ax.scatter(x_pos, y_pos, color=next(colors), marker="s")

    ax.set_aspect('equal', adjustable='datalim')
    fig.legend(labels=[FMC.CLUSTER_ID.value + " " + str(clusterId) for clusterId in cluster_ids_distinct],
               loc="upper right")

    plt.grid()
    datetime_today = datetime.today()
    path_string = datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_map_visualization.png'
    plot.save_or_show(output_folder, path_string)

if __name__ == "__main__":
    args = parse_arguments()
    arams = Arams(args["input"])

    plot_map_visualization(arams, args["output"] if "output" in args else None)