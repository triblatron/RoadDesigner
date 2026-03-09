from . import Polyline
from pyglm import glm

class Straight:
    def __init__(self):
        self.points = []
        self.binormals = []
        self.tangents = []
        self.normals = []
        self.tessellation = None

    def length(self):
        if len(self.points) == 2:
            diff =  self.points[1] - self.points[0]
            return glm.length(diff)
        else:
            return 0.0

    def inertialCoord(self, offset:float, distance:float, loft:float):
        if len(self.points) >= 1 and len(self.binormals) == 1 and len(self.tangents)==1 and len(self.normals) == 1:
            return {
                'x':self.points[0]+offset * self.binormals[0],
                'y':self.points[0]+distance * self.tangents[0],
                'z':self.points[0]+loft * self.normals[0],
            }
        return {}

    def build(self):
        self.tessellation = Polyline.Polyline(1)
        self.tessellation.points[0] = self.points[0]
        self.tessellation.points[1] = self.points[1]

    points: list[glm.vec3]
    tangents: list[glm.vec3]
    normals: list[glm.vec3]
    binormals: list[glm.vec3]
