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
from utils.argument_parser import *


class Writer:
    @staticmethod
    def write(graph, file_name):
        Writer(graph, file_name)

    def __init__(self, graph, file_name):
        self.output_file = open(file_name, 'w')
        self.__write_file(graph, file_name)

    def __del__(self):
        self.output_file.close()

    def __write_file(self, graph, file_name):
        records_writers = {
            G2oTags.VERTEX: lambda p: self.__write_vertex(p),
            G2oTags.EDGE:   lambda p: self.__write_edge(p),
            G2oTags.FIX:    lambda p: self.__write_fix(p)
        }

        [records_writers[G2oTags.VERTEX](v) for v in graph.vertices]
        [records_writers[G2oTags.EDGE](e) for e in graph.edges]
        [records_writers[G2oTags.FIX](f) for f in graph.fixes]

    def __write_vertex(self, vertex):
        self.output_file.write(
            f"{G2oTags.VERTEX.value} {vertex.id} {Writer.__print_pose(vertex.pose)}\n")

    def __write_edge(self, edge):
        self.output_file.write(
            f"{G2oTags.EDGE.value} {edge.id_begin} {edge.id_end} "
            f"{Writer.__print_pose(edge.pose)} {Writer.__print_inf(edge.inf)}\n")

    def __write_fix(self, fix):
        self.output_file.write(
            f"{G2oTags.FIX.value} {fix.id}\n")

    @staticmethod
    def __print_pose(pose):
        return f"{pose.x} {pose.y} {pose.th}"

    @staticmethod
    def __print_inf(inf):
        return f"{inf.x_x} {inf.x_y} {inf.x_th} {inf.y_y} {inf.y_th} {inf.th_th}"


if __name__ == "__main__":
    from reader import Reader, find_g2o_file

    args = parse_arguments()
    g2o_file = find_g2o_file(args["input"])
    if not g2o_file:
        raise Exception("Could not find g2o file.")

    graph = Reader.read(g2o_file)

    from pathlib import Path
    g2o_file_copy = Path(g2o_file)
    print(g2o_file_copy)
    g2o_file_copy = g2o_file_copy.with_name(g2o_file_copy.stem + "_copy" + g2o_file_copy.suffix)
    print(g2o_file_copy)

    Writer.write(graph, g2o_file_copy)

    graph_copy = Reader.read(g2o_file_copy)
    assert graph == graph_copy, "Implementation error, copy of file should result in the same graph"
