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


class Reader:
    @staticmethod
    def read(file_name):
        return Reader(file_name).graph

    def __init__(self, file_name):
        self.graph = Graph()
        self.__read_file(file_name)

    def __read_file(self, file_name):
        records_parsers = {
            G2oTags.VERTEX: lambda p: self.__parse_vertex(p),
            G2oTags.EDGE:   lambda p: self.__parse_edge(p),
            G2oTags.FIX:    lambda p: self.__parse_fix(p)
        }

        with open(file_name, 'r') as input_file:
            # Loop over lines
            for line in input_file:
                # Use any number of spaces as separator to split the line
                parts = line.split()

                # Based on the tag at the beginning the line, parse the remainder of the line
                tag = G2oTags(parts[0])
                records_parsers[tag](parts[1:])

    def __parse_vertex(self, parts):
        p = Pose(*map(float, parts[1:]))
        v = Graph.Vertex(int(parts[0]), p)
        self.graph.vertices.append(v)

    def __parse_edge(self, parts):
        p = Pose(*map(float, parts[2:5]))
        i = InfMatrix(*map(float, parts[5:]))
        e = Graph.Edge(*map(int, parts[0:2]), p, i)
        self.graph.edges.append(e)

    def __parse_fix(self, parts):
        f = Graph.Fix(int(*parts))
        self.graph.fixes.append(f)


def find_g2o_file(paths):
    # Being user friendly
    if not isinstance(paths, List):
        paths = [paths]

    for path in paths:
        if path.endswith(".g2o"):
            return path
    return None


if __name__ == "__main__":
    args = parse_arguments()
    g2o_file = find_g2o_file(args["input"])
    if not g2o_file:
        raise Exception("Could not find g2o file.")

    graph = Reader.read(g2o_file)

    print("Sizes")
    print(f"    vertices array: {len(graph.vertices)}")
    print(f"    edges array: {len(graph.edges)}")
    print(f"    fixes array: {len(graph.fixes)}")

    print("First entries")
    if graph.vertices:
        print(f"    {graph.vertices[0]}")
    if graph.edges:
        print(f"    {graph.edges[0]}")
    if graph.fixes:
        print(f"    {graph.fixes[0]}")
