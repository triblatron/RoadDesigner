import bpy
import bmesh

try:
    from road import SweptSurface
except:
    import vendor.road

class SweptSurfaceConverter:
    def __init__(self, surface):
        self.surface = surface
        self.mesh = None
        self.obj = None
        self.bm = None

    def add_vert(self, vert):
        if self.bm is not None:
            v1 = self.bm.verts.new((vert.position.x, vert.position.y, vert.position.z))
            return v1

        return None

    def convert(self, op, context, profile_objs, profile_meshes):
        self.mesh = bpy.data.meshes.new("RoadMesh")
        self.obj = bpy.data.objects.new("surface", self.mesh)
        context.collection.objects.link(self.obj)
        
        material_index_map = {}
        for quad_index, quad in enumerate(profile_meshes):
            mat = profile_objs[quad_index].data.materials[0]
            if mat.name not in material_index_map:
                material_index_map[mat.name] = len(self.obj.data.materials)
                self.obj.data.materials.append(mat)  # ✅ correct way to add

        self.bm = bmesh.new()
        uv_layer = self.bm.loops.layers.uv.new("UVMap")
        for quad_index, quad in enumerate(self.surface.quads):
            v1 = self.add_vert(self.surface.points[quad[0]])
            v2 = self.add_vert(self.surface.points[quad[1]])
            v3 = self.add_vert(self.surface.points[quad[2]])
            v4 = self.add_vert(self.surface.points[quad[3]])

            face = self.bm.faces.new([v1, v2, v3, v4])
            mat = profile_objs[quad_index % len(profile_objs)].data.materials[0]
            face.material_index = material_index_map[mat.name]            
            for loop, vert_index in zip(face.loops, quad):
                op.report({'INFO'}, f"Adding loop {loop} to UVMap with vertex index {vert_index} position {self.surface.points[vert_index].position} uv {self.surface.points[vert_index].tex_coord}")
                loop[uv_layer].uv = (self.surface.points[vert_index].tex_coord.x, self.surface.points[vert_index].tex_coord.y)


        self.bm.to_mesh(self.mesh)
        self.bm.free()

    def add_mesh_with_uvs(self,context):
        mesh = bpy.data.meshes.new("MyMesh")
        obj = bpy.data.objects.new("MyObject", mesh)
        context.collection.objects.link(obj)

        bm = bmesh.new()

        # Create geometry
        v1 = bm.verts.new((0, 0, 0))
        v2 = bm.verts.new((1, 0, 0))
        v3 = bm.verts.new((1, 1, 0))
        v4 = bm.verts.new((0, 1, 0))
        face = bm.faces.new([v1, v2, v3, v4])

        # Create UV layer
        uv_layer = bm.loops.layers.uv.new("UVMap")

        # Assign UV coordinates per loop (vertex-per-face)
        uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for loop, uv in zip(face.loops, uvs):
            loop[uv_layer].uv = uv

        bm.to_mesh(mesh)
        bm.free()
