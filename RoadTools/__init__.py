bl_info = {
    "name": "Road Tools",
    "author": "Tony Horrobin",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Road Tools",
    "description": "Designs roads according to highway standards",
    "category": "Object",
}

import bpy
from mathutils import Vector

import sys
import os
import site
import tomllib

#   sys.path.append(os.path.dirname(__file__))
import Clothoids


def get_length(self):
    return (self.end_point - self.start_point).length


class RoadToolsProperties(bpy.types.PropertyGroup):
    profile_file: bpy.props.StringProperty(
        name="Profile",
        description="Path to a .blend file",
        subtype='FILE_PATH'
    )
    road_length: bpy.props.FloatProperty(name="Road Length",description="The length of the road", get=get_length, subtype='DISTANCE')
    road_width: bpy.props.FloatProperty(name="Road Width", description="The width of the road", subtype='DISTANCE')
    start_point: bpy.props.FloatVectorProperty(name="Start Point",description="The first point on the road", subtype='TRANSLATION')
    mid_point: bpy.props.FloatVectorProperty(name="Mid Point",description="The middle point on the road", subtype='TRANSLATION')
    end_point: bpy.props.FloatVectorProperty(name="End Point",description="The last point on the road", subtype='TRANSLATION')
    real_world_size: bpy.props.FloatVectorProperty(name="Real world size",description="The size of the road texture", size=2, subtype='TRANSLATION')

import bpy
from bpy_extras import view3d_utils

class OBJECT_OT_click_grid(bpy.types.Operator):
    bl_idname = "object.click_grid"
    bl_label = "Click on Grid"

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get 3D location from mouse position
            coord = (event.mouse_region_x, event.mouse_region_y)
            region = context.region
            rv3d = context.region_data

            # Cast a ray from mouse position
            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

            # Find where ray intersects the Z=0 plane (the grid)
            location = self.ray_to_grid(ray_origin, view_vector)

            if location:
                print(f"Clicked grid at: {location}")
                # Do something with the location, e.g. place an object
                bpy.ops.object.empty_add(location=location)

            return {'RUNNING_MODAL'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def ray_to_grid(self, origin, direction, z=0.0):
        """Intersect ray with Z plane."""
        if abs(direction.z) < 1e-6:
            return None  # Ray is parallel to grid
        t = (z - origin.z) / direction.z
        if t < 0:
            return None  # Intersection is behind the camera
        from mathutils import Vector
        return origin + t * direction

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}


def register():
    bpy.utils.register_class(OBJECT_OT_click_grid)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_click_grid)

class OBJECT_OT_create_straight(bpy.types.Operator):
    bl_idname = "object.create_straight"
    bl_label = "Create a straight road"

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

class VIEW3D_PT_road_tools_panel(bpy.types.Panel):
    bl_label = "Road Tools"
    bl_idname = "VIEW3D_PT_road_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Road Tools"   # ← this becomes a new tab in the N-panel

    def draw(self, context):
        layout = self.layout
        props = context.scene.road_tool_props
        layout.prop(props, "profile_file")
        layout.prop(props, "road_length")
        layout.prop(props, "road_width")
        layout.prop(props, "start_point")
        layout.prop(props, "mid_point")
        layout.prop(props, "end_point")
        layout.prop(props, "real_world_size")
        self.layout.operator("object.create_straight")

def register():
    bpy.utils.register_class(RoadToolsProperties)
    bpy.types.Scene.road_tool_props = bpy.props.PointerProperty(type=RoadToolsProperties)
    bpy.utils.register_class(OBJECT_OT_create_straight)
    bpy.utils.register_class(VIEW3D_PT_road_tools_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_straight)
    bpy.utils.unregister_class(RoadToolsProperties)
    bpy.utils.unregister_class(VIEW3D_PT_road_tools_panel)
    del bpy.types.Scene.road_tool_props