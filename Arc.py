import math
from ctypes.wintypes import LPPOINT

from pyglm import glm

from Polyline import Polyline
from Segment import Segment


class Arc:
    def __init__(self):
        self.length: float = 0.0
        self.points: list[glm.vec3] = []
        self.tangents: list[glm.vec3] = []
        self.normals: list[glm.vec3] = []
        self.binormals: list[glm.vec3] = []
        self.radius = 0.0
        self.centre = glm.vec3(0.0, 0.0, 0.0)
        self.tessellation = None

    def build(self, num_points: int):
        if self.length != 0.0 and  len(self.points) == 1 and len(self.tangents) == 1 and len(self.normals) == 1 and len(self.binormals) == 1:
            abs_radius = abs(self.radius)
            self.centre = self.points[0] + self.radius * self.binormals[0]
            theta = self.length / abs_radius
            p = (abs_radius - abs_radius * math.cos(theta)) * self.binormals[0]
            p += abs_radius * math.sin(theta) * self.tangents[0]
            self.points.append(self.points[0] + math.copysign(1, self.radius) * (abs_radius - abs_radius * math.cos(theta)) * self.binormals[0] + abs_radius * math.sin(theta) * self.tangents[0])
            sign = math.copysign(1, -self.radius)
            centre_to_point = sign * (self.points[1] - self.centre)
            centre_to_point /= self.radius
            self.binormals.append(centre_to_point)
            self.normals.append(self.normals[0])
            self.tangents.append(glm.cross(self.normals[1], self.binormals[1]))
            self.tessellate(num_points)

    def tessellate(self, num_divisions: int):
        self.tessellation = Polyline(num_divisions)
        max_theta = self.length / abs(self.radius)
        abs_radius = abs(self.radius)
        for point_index in range(num_divisions + 1):
            theta = point_index / num_divisions * max_theta
            self.tessellation.points[point_index] = (self.points[0] + math.copysign(1, self.radius) * (abs_radius - abs_radius * math.cos(theta)) * self.binormals[0] + abs_radius * math.sin(theta) * self.tangents[0])

    points: list[glm.vec3]
    tangents: list[glm.vec3]
    normals: list[glm.vec3]
    binormals: list[glm.vec3]
    length: float
    tessellation: Polyline
