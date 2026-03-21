import traceback

import bpy
try:
    from road import Road
    from . import SweptSurfaceConverter
except ImportError:
    traceback.print_exc()
    import vendor.road

class CreateStraight(bpy.types.Operator):
    bl_idname = "object.create_straight"
    bl_label = "Create a straight road"
    def execute(self, context):
        # 1. Create a Road at the specified start point
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

        # Get the active UV layer

        road = Road.Road()
        index = 0
        for mesh in data_to.meshes:
            uv_layer = mesh.uv_layers.active.data
            for poly in mesh.polygons:
                self.report({'INFO'}, "Creating profile: " + mesh.name)
                parent_obj = [obj for obj in bpy.data.objects if obj.data == mesh]
                assert(len(parent_obj)==1)
                road.beginProfile(parent_obj[0].name, index)
                for loop_index in poly.loop_indices:
                    loop = mesh.loops[loop_index]
                    vert = mesh.vertices[loop.vertex_index]
#                    uv_layer[loop_index].uv = (props.road_width / real_world_size[0], 0.0)
                    road.vertex(vert.co[0], vert.co[1], vert.co[2], uv_layer[loop_index].uv[0], uv_layer[loop_index].uv[1])
                self.report({'INFO'}, "Ending profile: " + mesh.name)
                self.report({'INFO'}, "Road: " + str(road))
                road.endProfile()
                index += 1
        road.create_straight(props.road_length,props.num_divisions) 

        # 2. Copy the Polyline into a mesh
        curve_data = bpy.data.curves.new("Polyline", type='CURVE')
        curve_data.dimensions = '3D'

        spline = curve_data.splines.new(type='POLY')

        # Spline starts with 1 point, add the rest
        spline.points.add(props.num_divisions)

        print(f"Tessellation has {road.segment.tessellation.num_points()} points")
        for i, p in enumerate(road.segment.tessellation.points):
            print(f"Adding point {i} to tessellation {p}")
            spline.points[i].co = (p.x, p.y, p.z, 1.0)  # 4th value is weight

        converter = SweptSurfaceConverter.SweptSurfaceConverter(road.surface)
        road_objs = []
        for name in road.profiles.keys():
            road_objs.append(bpy.data.objects[name])
        #["shoulder_left"], bpy.data.objects["bed"], bpy.data.objects["shoulder_right"]]
        converter.convert(self, context, road_objs, data_to.meshes)

        # Make sure it's open (not closed)
        spline.use_cyclic_u = False

        obj = bpy.data.objects.new("Polyline", curve_data)
        bpy.context.collection.objects.link(obj)

        return {'FINISHED'}