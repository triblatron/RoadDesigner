from pyglm import glm
try:
    from . import Vertex
except ImportError:
    import Vertex
from functools import cmp_to_key

class Quad:
    def __init__(self):
        self.verts = []

    def configure(self, config):
        if "verts" in config:
            for vertConfig in config["verts"]:
                vert = Vertex.Vertex()
                vert.configure(vertConfig)
                self.verts.append(vert)
        self.sort()

    def sort(self):
        self.verts = sorted(self.verts, key=cmp_to_key(Vertex.Vertex.compare) )

    def addVertex(self, vertex: Vertex.Vertex):
        self.verts.append(vertex)

    def begin(self):
        pass

    def end(self):
        self.sort()

    def vertex(self, x, y, z, u, v):
        self.verts.append(Vertex.Vertex())
        self.verts[-1].position = glm.vec3(x, y, z)
        self.verts[-1].tex_coord = glm.vec2(u, v)

    def width(self):
        return glm.length(self.verts[1]-self.verts[0])

    def length(self):
        return glm.length(self.verts[2] - self.verts[0])

    verts : list[Vertex.Vertex]
