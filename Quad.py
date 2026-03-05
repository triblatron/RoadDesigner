from pyglm import glm
from Vertex import Vertex
from functools import cmp_to_key

class Quad:
    def __init__(self):
        self.verts = []

    def configure(self, config):
        if "verts" in config:
            for vertConfig in config["verts"]:
                vert = Vertex()
                vert.configure(vertConfig)
                self.verts.append(vert)
        self.sort()

    def sort(self):
        self.verts = sorted(self.verts, key=cmp_to_key(Vertex.compare) )

    verts : list[Vertex]
