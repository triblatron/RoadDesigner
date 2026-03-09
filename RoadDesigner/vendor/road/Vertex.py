from pyglm import glm

from . import Configurable

class Vertex:
    def __init__(self):
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.tex_coord = glm.vec2(0.0,0.0)

    def configure(self,config):
        self.position.x = Configurable.Configurable.readConfig(config, "x", 0.0)
        self.position.y = Configurable.Configurable.readConfig(config, "y", 0.0)
        self.position.z = Configurable.Configurable.readConfig(config, "z", 0.0)
        self.tex_coord.x = Configurable.Configurable.readConfig(config, "u", 0.0)
        self.tex_coord.y = Configurable.Configurable.readConfig(config, "v", 0.0)

    @classmethod
    def compare(cls,a,b):
        if a.position.y < b.position.y:
            return -1
        elif a.position.y > b.position.y:
            return 1
        elif a.position.x < b.position.x:
            return -1
        elif a.position.x > b.position.x:
            return 1
        elif a.position.z < b.position.z:
            return -1
        elif a.position.z > b.position.z:
            return 1

        return 0

    position : glm.vec3
    tex_coord : glm.vec2
