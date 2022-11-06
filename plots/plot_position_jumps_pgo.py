#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from utils.g2o_parser import *
from utils.argument_parser import *
from utils import plot
from datetime import datetime


def plot_position_jumps_pgo(g2o_file, debug, output_folder=None):
    # Clip position jumps to this value
    pos_jump_lim = 0.10  # [mm]

    # Import arrays via g2o_parser
    vertices_array, edges_array, constraints_array = import_g2o(g2o_file)
    n_edges = len(edges_array)
    n_vertices = len(vertices_array)
    edges_array = np.append(edges_array, np.empty([n_edges, 10]), axis=1)
    vertices_array = np.append(vertices_array, np.empty([n_vertices, 6]), axis=1)

    # Convert edges from loop closure to world coordinates
    for i in range(n_edges):
        # First filter consecutive vertices (these are not from loop closure)
        if int(edges_array[i, 2]) - int(edges_array[i, 1]) != 1:
            vertex_a = int(np.round(edges_array[i, 1], decimals=0))
            vertex_b = int(np.round(edges_array[i, 2], decimals=0))

            theta_a = vertices_array[vertex_a, 4]
            theta_b = vertices_array[vertex_b, 4]

            x_pgo = edges_array[i, 3]
            y_pgo = edges_array[i, 4]

            # calculate edge from A->B' in world coordinates
            x_pgo_wc = np.cos(theta_a) * x_pgo - np.sin(theta_a) * y_pgo
            y_pgo_wc = np.sin(theta_a) * x_pgo + np.cos(theta_a) * y_pgo
            theta_pgo_wc = theta_a + edges_array[i, 5]

            edges_array[i, 12] = x_pgo_wc
            edges_array[i, 13] = y_pgo_wc
            edges_array[i, 14] = theta_pgo_wc  # check later

            # For an edge from vertex A to B', calculate the pose from A to B using the poses of vertex A and B
            x_ver_wc = vertices_array[vertex_b, 2] - vertices_array[vertex_a, 2]
            y_ver_wc = vertices_array[vertex_b, 3] - vertices_array[vertex_a, 3]
            theta_ver_wc = theta_b - theta_a

            edges_array[i, 15] = x_ver_wc
            edges_array[i, 16] = y_ver_wc
            edges_array[i, 17] = theta_ver_wc

            # Calculate the distance from where vertex B was originally placed
            # and where it is based on loop closure with vertex A, i.e., B-B' =  A + A->B' - B
            edges_array[i, 18] = vertices_array[vertex_a, 2] + edges_array[i, 12] - vertices_array[
                vertex_b, 2]  # x_ver_wc + x_pgo_wc
            edges_array[i, 19] = vertices_array[vertex_a, 3] + edges_array[i, 13] - vertices_array[
                vertex_b, 3]  # y_ver_wc + y_pgo_wc
            edges_array[i, 20] = vertices_array[vertex_a, 4] + edges_array[i, 14] - vertices_array[
                vertex_b, 4]  # theta_ver_wc + theta_pgo_wc
            edges_array[i, 21] = np.sqrt(np.square(edges_array[i, 18]) + np.square(edges_array[i, 19]))

    vertex_id_to_index = {}
    for i in range(n_vertices):
        vertex_id_to_index[int(vertices_array[i, 1])] = i

    n_matches = np.zeros(n_vertices)
    for j in range(n_edges):
        edge_j = edges_array[j, :]

        if int(edge_j[1]) == 0:
            continue

        # check if edge is not a results of consecutive sigs, but really from loop closure
        if abs(int(edge_j[2]) - int(edge_j[1])) <= 1:
            continue

        # look up vertex i corresponding to edge start
        i = vertex_id_to_index[int(edges_array[j, 1])]
        n_matches[i] += 1

        # one vertex can match against multiple other vertices
        # therefore first update the average per signature of the distance from where vertex B was originally placed
        # and where it is based on loop closure with vertex A
        vertices_array[i, 5] = (vertices_array[i, 5] * (n_matches[i] - 1) + edge_j[18]) / n_matches[i]
        vertices_array[i, 6] = (vertices_array[i, 6] * (n_matches[i] - 1) + edge_j[19]) / n_matches[i]
        vertices_array[i, 7] = (vertices_array[i, 7] * (n_matches[i] - 1) + edge_j[20]) / n_matches[i]

        # also update average per signature of where loop closures were found
        vertices_array[i,  8] = (vertices_array[i,  8] * (n_matches[i] - 1) + edge_j[12]) / n_matches[i]
        vertices_array[i,  9] = (vertices_array[i,  9] * (n_matches[i] - 1) + edge_j[13]) / n_matches[i]
        vertices_array[i, 10] = (vertices_array[i, 10] * (n_matches[i] - 1) + edge_j[14]) / n_matches[i]

    vertices_array[n_matches == 0, 5:7] = 0

    magnitude = np.sqrt(np.square(vertices_array[:, 5]) + np.square(vertices_array[:, 6]))

    # plot scatter plot (average per vertex) of found loop closures where color and size indicates magnitude of jump
    ax = plt.axes()
    ax.axis('equal')
    cm = LinearSegmentedColormap.from_list("", ["green", "yellow", "red"])
    sc = ax.scatter(vertices_array[:, 2], vertices_array[:, 3], s=500 * magnitude, c=magnitude,
                    cmap=cm, vmin=0, vmax=pos_jump_lim)  # np.max(magnitude))

    plt.title('Magnitude of jumps from loop closures per signature (m)')
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.grid()
    plt.colorbar(sc)
    plt.tight_layout()

    datetime_today = datetime.today()
    plot.save_or_show(output_folder, datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_plot_position_jumps_pgo_map.png')

    # Plot magnitude of jumps in histogram
    n_bins = 100
    x = edges_array[:, 21]
    ax = plt.axes()
    ax.hist(x, bins=n_bins, density=True)  # ,label = "Jump [m]")
    plt.axvline(x.mean(), color='k', linestyle='dashed', linewidth=1, label="Mean")
    min_ylim, max_ylim = plt.ylim()
    plt.text(x.mean() * 1.1, max_ylim * 0.9, 'Mean [m]: {:.2f}'.format(x.mean()))

    plt.suptitle('Magnitude of jumps from loop closures')
    plt.title(
        ['Mean [m]: {:.3f}'.format(x.mean()), 'Min [m]: {:.3f}'.format(x.min()), 'Max [m]: {:.3f}'.format(x.max())])
    plt.xlabel("Magnitude of jump [m]")
    plt.ylabel("Frequency of jump [-]")
    plt.legend()
    plt.xlim(0, pos_jump_lim)
    plt.tight_layout()

    datetime_today = datetime.today()
    plot.save_or_show(output_folder, datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_plot_position_jumps_pgo_hist.png')


    if debug:
        # Plot arrows that start where a signature is expected and ends at where it has been placed during mapping
        ax = plt.axes()
        ax.axis('equal')
        for i in range(n_vertices):
            # Basis of arrow is the vertex on which loop closures have been calculated
            ax.arrow(vertices_array[i, 2], vertices_array[i, 3], -vertices_array[i, 5], -vertices_array[i, 6],
                     head_width=0.005, head_length=0.005, fc='k', ec='k')
        plt.tight_layout()

        datetime_today = datetime.today()
        plot.save_or_show(output_folder, datetime_today.strftime("%d-%m-%y_%H-%M-%S") + '_plot_position_jumps_pgo_arrows.png')



def find_g2o_file(paths):
    for path in paths:
        if path.endswith(".g2o"):
            return path
    return None


if __name__ == "__main__":
    args = parse_arguments()
    g2o_file = find_g2o_file(args["input"])
    if not g2o_file:
        raise Exception("Could not find g2o file.")

    plot_position_jumps_pgo(g2o_file, args["debug"], args["output"] if "output" in args else None)