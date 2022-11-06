#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

from arams import Arams
from arams.file_specifications import *
from utils.argument_parser import *
from utils import plot
from datetime import datetime

def plot_distance_between_signatures_map(arams, output_folder=None):
    if FMC not in arams:
        print("Could not find floor_map_coordinates file.")
        return
    df = arams[FMC]

    cluster_ids_distinct = df[FMC.CLUSTER_ID.value].unique()
    marker_x, marker_y, dist = [], [], []

    for cluster_id in cluster_ids_distinct:
        df_filtered = df[df[FMC.CLUSTER_ID.value] == cluster_id]
        df_filtered = df_filtered.sort_values(by=[FMC.IDX_IN_MAP.value])

        marker_x_cluster = df_filtered[FMC.SIG_POS_X.value].to_list()
        marker_y_cluster = df_filtered[FMC.SIG_POS_Y.value].to_list()

        # Euclidean distance between consecutive markers
        dist_cluster = np.sqrt(np.diff(marker_x_cluster) ** 2 +
                               np.diff(marker_y_cluster) ** 2)

        marker_x.extend(marker_x_cluster[1:])
        marker_y.extend(marker_y_cluster[1:])
        dist.extend(dist_cluster)

    plt.title("Map visualization")
    plt.xlabel("X-axis (m)")
    plt.ylabel("Y-axis (m)")

    plt.scatter(marker_x, marker_y, c=dist, s=[d * 1 for d in dist])
    plt.gca().set_aspect('equal', adjustable='datalim')

    cbar = plt.colorbar(ticks=np.linspace(min(dist), max(dist), 10))
    cbar.ax.set_title('Distance (m)')
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

    plt.grid()

    datetime_today = datetime.today()
    path_string = datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_distance_between_signatures_map.png'
    plot.save_or_show(output_folder, path_string)

if __name__ == "__main__":
    args = parse_arguments()
    arams = Arams(args["input"])

    plot_distance_between_signatures_map(arams, args["output"] if "output" in args else None)
