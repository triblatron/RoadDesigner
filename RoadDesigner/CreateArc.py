import bpy
try:
    from .vendor.road import Road
except ImportError:
    import vendor.road

class CreateArc(bpy.types.Operator):
    bl_idname = "object.create_arc"
    bl_label = "Create a circular arc road"
    def execute(self, context):
        # 1. Create a Road at the specified start point
        props = context.scene.road_tool_props
        # file_path = props.profile_file
        # print(f"Selected file: {file_path}")
        #
        # # now use it, e.g.:
        # if not file_path:
        #     self.report({'WARNING'}, "No file selected")
        #     return {'CANCELLED'}
        #
        # with bpy.data.libraries.load(file_path) as (data_from, data_to):
        #     print(data_from.meshes)
        #     data_to.meshes = data_from.meshes
        #     data_to.objects = data_from.objects

        road = Road.Road()

        road.create_arc(props.road_length, props.road_radius, props.num_divisions)

        # 2. Copy the Polyline into a mesh
        curve_data = bpy.data.curves.new("Polyline", type='CURVE')
        curve_data.dimensions = '3D'

        spline = curve_data.splines.new(type='POLY')

        # Spline starts with 1 point, add the rest
        spline.points.add(road.segment.tessellation.num_points()-1)

        print(f"Tessellation has {road.segment.tessellation.num_points()} points")
        for i, p in enumerate(road.segment.tessellation.points):
            print(f"Adding point {i} to tessellation {p}")
            spline.points[i].co = (p.x, p.y, p.z, 1.0)  # 4th value is weight

        # Make sure it's open (not closed)
        spline.use_cyclic_u = False

        obj = bpy.data.objects.new("Polyline", curve_data)
        bpy.context.collection.objects.link(obj)

        return {'FINISHED'}