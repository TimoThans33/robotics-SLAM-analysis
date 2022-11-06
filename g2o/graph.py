#!/usr/bin/env python3
"""
 Copyright (c) 2017-2021, Accerion (Unconstrained Robotics B.V.)
 * All rights reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


@dataclass
class Pose:
    x: float = 0
    y: float = 0
    th: float = 0


@dataclass
class InfMatrix:
    x_x: float = 0
    x_y: float = 0
    x_th: float = 0
    y_y: float = 0
    y_th: float = 0
    th_th: float = 0


@dataclass
class Graph:
    @dataclass
    class Vertex:
        id: int = 0
        pose: Pose = Pose()

    @dataclass
    class Edge:
        id_begin: int = 0
        id_end: int = 0
        pose: Pose = Pose()
        inf: InfMatrix = InfMatrix()

    @dataclass
    class Fix:
        id: int = 0

    vertices: List[Vertex] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    fixes: List[Fix] = field(default_factory=list)


class G2oTags(Enum):
    VERTEX = "VERTEX_SE2"
    EDGE = "EDGE_SE2"
    FIX = "FIX"
