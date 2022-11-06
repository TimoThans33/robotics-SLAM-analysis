#!/usr/bin/env python3
import numpy as np
from utils.argument_parser import *

def import_g2o(file_name):
    # Initialize some arrays
    edges_array = np.empty([1, 12])
    temp_edges_array = np.empty([1, 12])
    vertices_array = np.empty([1, 5])
    temp_vertices_array = np.empty([1, 5])
    constraints_array = np.empty([1, 2])
    temp_constraints_array = np.empty([1, 2])

    edges_no = 0
    vertices_no = 0
    constraints_no = 0

    with open(file_name, 'r') as input_file:
        # Loop over lines
        for line in input_file:
            # Use any number of spaces as separator
            sline = line.split()

            # Separate Edges and put in array
            if sline[0] == 'EDGE_SE2':
                # Only import edges from loop closures
                if abs(int(sline[2])-int(sline[1])) > 1:
                    for i in range(np.size(sline)):
                        if i == 0:
                            temp_edges_array[0, i] = edges_no
                        else:
                            temp_edges_array[0, i] = float(sline[i])

                    # Replace array once, then append for the remainder
                    if edges_no == 0:
                        edges_array = temp_edges_array
                    else:
                        edges_array = np.vstack((edges_array, temp_edges_array))

                    edges_no += 1

            # Separate vertices and put in an array
            if sline[0] == 'VERTEX_SE2':
                for i in range(np.size(sline)):
                    if i == 0:
                        temp_vertices_array[0, i] = vertices_no
                    else:
                        temp_vertices_array[0, i] = float(sline[i])

                if vertices_no == 0:
                    vertices_array = temp_vertices_array
                else:
                    vertices_array = np.vstack((vertices_array, temp_vertices_array))

                vertices_no += 1


            if sline[0] == 'FIX':
                for i in range(np.size(sline)):
                    if i == 0:
                        temp_constraints_array[0, i] = constraints_no
                    else:
                        temp_constraints_array[0, i] = float(sline[i])

                if constraints_no == 0:
                    constraints_array = temp_constraints_array
                else:
                    constraints_array = np.vstack((constraints_array, temp_constraints_array))

                constraints_no += 1

    return vertices_array, edges_array, constraints_array
if __name__ == "__main__":
    args = parse_arguments()
    filename = args["input"][0]
    vertices_array, edges_array, constraints_array = import_g2o(filename)
    # For debugging
    print("vertices array:", vertices_array[-1,:])
    print("edges array:", edges_array[-1,:])
    print("constraints array:", constraints_array[-1,:])