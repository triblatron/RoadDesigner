try:
    from .vendor.road import Quad
    from .vendor.road import Polyline
    from .vendor.road import Segment
    from .vendor.road import Vertex
    from .vendor.pyglm import glm
except ImportError:
    import Quad
    import Polyline
    import Segment
    import Vertex
    from pyglm import glm

class SweptSurface:
    def __init__(self, profile:list[Quad.Quad], axis:Segment.Segment):
        self.profile = profile
        self.axis = axis
        self.points = []

    def num_points(self):
        return len(self.points)

    def build(self):
        # Somehow build the surface.
        # for each point in the axis do:
        #   generate a quad
        for quad in self.profile:
            width = glm.length(quad.verts[1].position - quad.verts[0].position)
            length = glm.length(self.axis.points[1] - self.axis.points[0])
            real_world_size = glm.vec2(width/quad.verts[1].tex_coord.x, quad.verts[2].position.y / quad.verts[2].tex_coord.y)
            self.points.append(quad.verts[0])
            self.points.append(quad.verts[1])
            self.points.append(Vertex.Vertex())
            self.points[-1].position.x = quad.verts[2].position.x
            self.points[-1].position.y = self.axis.points[1].y
            self.points[-1].tex_coord.x = quad.verts[2].tex_coord.x
            self.points[-1].tex_coord.y = length / real_world_size.y
            self.points.append(Vertex.Vertex())
            self.points[-1].position.x = quad.verts[3].position.x
            self.points[-1].position.y = self.axis.points[1].y
            self.points[-1].tex_coord.x = width / real_world_size.x
            self.points[-1].tex_coord.y = length / real_world_size.y


