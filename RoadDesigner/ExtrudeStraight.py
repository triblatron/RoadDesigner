import bpy
from mathutils import Vector
import bl_math
class ExtrudeStraight(bpy.types.Operator):
    bl_idname = "object.extrude_straight"
    bl_label = "Extrude a straight road"

    def execute(self, context):
        props = context.scene.road_tool_props
        file_path = props.profile_file
        print(f"Selected file: {file_path}")

        # now use it, e.g.:
        if not file_path:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}

        with bpy.data.libraries.load(file_path) as (data_from, data_to):
            print(data_from.meshes)
            data_to.meshes = data_from.meshes
            data_to.objects = data_from.objects

        print(data_to)
        road = None

        for obj in data_to.objects:
            print(obj.name)
            if "bed" in obj.name:
                road = obj.copy()  # independent duplicate

        bb = road.bound_box
        # 8 corners, each is a Vector with (x, y, z)
        for i, corner in enumerate(bb):
            print(f"Corner {i}: {corner[0]:.2f}, {corner[1]:.2f}, {corner[2]:.2f}")

        xs = [v[0] for v in road.bound_box]
        ys = [v[1] for v in road.bound_box]
        zs = [v[2] for v in road.bound_box]

        min_corner = Vector((min(xs), min(ys), min(zs)))
        max_corner = Vector((max(xs), max(ys), max(zs)))
        dimensions = max_corner - min_corner

        print(f"min_corner: {min_corner}, max_corner: {max_corner}")

        mesh = road.data  # the Mesh data block

        for vert in mesh.vertices:
            print(vert.index, vert.co)  # co is a Vector (x, y, z) in local space

        mesh.vertices[2].co.y = context.scene.road_tool_props.end_point.y
        mesh.vertices[3].co.y = context.scene.road_tool_props.end_point.y

        # Get the active UV layer
        uv_layer = mesh.uv_layers.active.data


        # Build a map from vertex index to loop indices
        # Extract real-world size of texture from original UVs
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                loop = mesh.loops[loop_index]
                if loop.vertex_index == 0:
                    uv_layer[loop.index].uv = (0.0, 0.0)
                if loop.vertex_index == 1:
                    real_world_size = (props.road_width / uv_layer[loop.index].uv[0],
                                       0.0)
                    print(f"real world size[{loop.vertex_index}]:{real_world_size}")
                    uv_layer[loop_index].uv = (props.road_width / real_world_size[0], 0.0)
                if loop.vertex_index == 2:  # target vertex index
                    real_world_size = (0.0,
                                       max_corner.y / uv_layer[loop.index].uv[1])
                    print(f"real world size[{loop.vertex_index}]:{real_world_size}")
                    uv_layer[loop_index].uv = (0.0,props.road_length / real_world_size[1])
                if loop.vertex_index == 3:
                    real_world_size = (props.road_width / uv_layer[loop.index].uv[0],
                                       max_corner.y / uv_layer[loop.index].uv[1])
                    print(f"real world size[{loop.vertex_index}]:{real_world_size}")
                    uv_layer[loop_index].uv = (props.road_width / real_world_size[0],props.road_length / real_world_size[1])

        #obj = bpy.data.objects.new("profile", mesh_copy)
        bpy.context.collection.objects.link(road)

        return {'FINISHED'}
