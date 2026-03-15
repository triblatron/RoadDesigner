try:
    from road import Quad
    from road import Polyline
    from road import Segment
    from road import Vertex
    from pyglm import glm
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
        self.quads = []

    def num_points(self):
        return len(self.points)

    # Note that the vertices are output in Blender CCW winding
    # not the internal sorted order
    def build(self):
        # Somehow build the surface.
        # for each point in the axis do:
        #   generate a quad
        vert_index = 0
        for point_index in range(len(self.axis.points)-1):
            for quad in self.profile:
                width = glm.length(quad.verts[1].position - quad.verts[0].position)
                length = glm.length(self.axis.points[point_index+1] - self.axis.points[point_index])
                real_world_size = glm.vec2(width/quad.verts[1].tex_coord.x, quad.verts[2].position.y / quad.verts[2].tex_coord.y)
                self.quads.append([-1,-1,-1,-1])
                self.points.append(quad.verts[0])
                self.quads[-1][0] = vert_index

                self.points.append(quad.verts[1])
                self.quads[-1][1] = vert_index + 1
                self.points.append(Vertex.Vertex())
                self.points[-1].position.x = quad.verts[2].position.x
                self.points[-1].position.y = self.axis.points[point_index+1].y
                self.points[-1].tex_coord.x = quad.verts[2].tex_coord.x
                self.points[-1].tex_coord.y = length / real_world_size.y
                self.quads[-1][2] = vert_index + 3
                self.points.append(Vertex.Vertex())
                self.points[-1].position.x = quad.verts[3].position.x
                self.points[-1].position.y = self.axis.points[point_index+1].y
                self.points[-1].tex_coord.x = width / real_world_size.x
                self.points[-1].tex_coord.y = length / real_world_size.y
                self.quads[-1][3] = vert_index + 2

                vert_index += 4

