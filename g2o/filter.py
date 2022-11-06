#!/usr/bin/env python3
"""
 Copyright (c) 2017-2021, Accerion (Unconstrained Robotics B.V.)
 * All rights reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from g2o.graph import *


class Filter:
    @staticmethod
    def identify_odometry_edges(graph):
        """Return the list of indices to the edges that are odometry edges, identified by the vertex indices being
        separated by one.
        """
        return [index for index, edge in enumerate(graph.edges) if abs(edge.id_end - edge.id_begin) == 1]

    @staticmethod
    def identify_loop_closure_edges(graph):
        """Return the list of indices to the edges that are loop closure edges, identified by the vertex indices being
        separated by more than one.
        """
        return [index for index, edge in enumerate(graph.edges) if abs(edge.id_end - edge.id_begin) != 1]


if __name__ == "__main__":
    from utils.argument_parser import parse_arguments
    from reader import Reader, find_g2o_file

    args = parse_arguments()
    g2o_file = find_g2o_file(args["input"])
    if not g2o_file:
        raise Exception("Could not find g2o file.")

    graph = Reader.read(g2o_file)

    print("Amounts")
    print(f"    all edges: {len(graph.edges)}")
    print(f"    odometry edges: {len(Filter.identify_odometry_edges(graph))}")
    print(f"    loop closure edges: {len(Filter.identify_loop_closure_edges(graph))}")
