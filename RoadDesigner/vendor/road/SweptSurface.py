try:
    from .vendor.road import Quad
    from .vendor.road import Polyline
    from .vendor.road import Segment
    from .vendor.road import Vertex
except ImportError:
    import Quad
    import Polyline
    import Segment
    import Vertex

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
            self.points.append(quad.verts[0])
            self.points.append(quad.verts[1])
            self.points.append(Vertex.Vertex())
            self.points[-1].position.x = quad.verts[2].position.x
            self.points[-1].position.y = self.axis.points[1].y
            self.points.append(Vertex.Vertex())
            self.points[-1].position.x = quad.verts[3].position.x
            self.points[-1].position.y = self.axis.points[1].y


