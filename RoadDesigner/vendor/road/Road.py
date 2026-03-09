from enum import Enum
from typing import Any

from . import Arc
from . import Straight
from . import Quad
from pyglm import glm

class RoadType(Enum):
    STRAIGHT = 0
    ARC=1,
    CLOTHOID=2

class Road:
    def __init__(self):
        self.meshes = []
        self.segment = None

    def configure(self, config: dict):
        if "meshes" in config:
            for meshConfig in config["meshes"]:
                self.beginProfile()
                self.meshes[-1].configure(meshConfig)
                self.endProfile()

    def beginProfile(self):
        self.inMesh = True
        self.meshes.append(Quad.Quad())
        self.meshes[-1].begin()

    def vertex(self, x, y, z, u, v):
        if self.inMesh:
            self.meshes[-1].vertex(x, y, z, u, v)

    def endProfile(self):
        self.inMesh = False
        self.meshes[-1].end()

    def create_straight(self, length: float):
        self.segment = Straight.Straight()
        self.segment.points.append(glm.vec3(0.0, 0.0, 0.0))
        self.segment.points.append(glm.vec3(0.0, length, 0.0))
        self.segment.tangents.append(glm.vec3(0.0, 1.0, 0.0))
        self.segment.normals.append(glm.vec3(0.0, 0.0, 1.0))
        self.segment.binormals.append(glm.vec3(1.0, 0.0, 0.0))
        self.segment.build()

    def create_arc(self, length: float, radius: float, num_divisions: int):
        self.segment = Arc.Arc()
        self.segment.points.append(glm.vec3(0.0, 0.0, 0.0))
        self.segment.tangents.append(glm.vec3(0.0, 1.0, 0.0))
        self.segment.normals.append(glm.vec3(0.0, 0.0, 1.0))
        self.segment.binormals.append(glm.vec3(1.0, 0.0, 0.0))
        self.segment.radius = radius
        self.segment.length = length
        self.segment.build(num_divisions)

    # type of geometry
    type: RoadType
    meshes: list[Quad.Quad]
    segment: Any
    first_point: glm.vec3
    middle_point: glm.vec3
    last_point: glm.vec3
    # length along centreline [m]
    length: float
    # width [m]
    width: float
    # signed radius [m], positive ccw
    radius: float
    inMesh: bool

