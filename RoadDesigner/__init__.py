import os
import sys
# Get absolute path to vendor directory
vendor_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "vendor")
print(vendor_path)
if vendor_path not in sys.path:
    sys.path.insert(0, vendor_path)
from . import ExtrudeStraight
from . import CreateStraight
from . import CreateArc
from road import *

# import debugpy
# debugpy.listen(5678)
# debugpy.wait_for_client()  # pauses until VS Code attaches

bl_info = {
    "name": "Road Designer",
    "author": "Tony Horrobin",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Road Designer",
    "description": "Designs roads according to highway standards",
    "category": "Object",
}

import bpy.props


#   sys.path.append(os.path.dirname(__file__))


def get_length(self):
    return (self.end_point - self.start_point).length

def set_length(self, value):
    pass  # read-only; ignore attempts to set it, or implement accordingly

class RoadDesignerProperties(bpy.types.PropertyGroup):
    profile_file: bpy.props.StringProperty(
        name="Profile",
        description="Path to a .blend file",
        subtype='FILE_PATH',
        default='/Users/tony/tartings/blender/RoadTools/models/profile_rural.blend'
    )
    road_length: bpy.props.FloatProperty(name="Road Length", description="The length of the road", get=get_length, set=set_length, subtype='DISTANCE',)
    road_width: bpy.props.FloatProperty(name="Road Width", description="The width of the road", subtype='DISTANCE', default=7.3)
    road_radius: bpy.props.FloatProperty(name="Road Radius", description="The radius of the road", subtype='DISTANCE', default=750.0)
    num_divisions: bpy.props.IntProperty(name="Number of divisions", description="The number of divisions in the swept surface of the road", default=1)
    start_point: bpy.props.FloatVectorProperty(name="Start Point",description="The first point on the road", subtype='TRANSLATION')
    mid_point: bpy.props.FloatVectorProperty(name="Mid Point",description="The middle point on the road", subtype='TRANSLATION')
    end_point: bpy.props.FloatVectorProperty(name="End Point",description="The last point on the road", subtype='TRANSLATION', default=(0.0,252.0,0.0))
    real_world_size: bpy.props.FloatVectorProperty(name="Real world size",description="The size of the road texture", size=2, subtype='TRANSLATION')
import bpy


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
        layout.prop(props, "road_radius")
        layout.prop(props, "num_divisions")
        self.layout.operator("object.create_straight")
        self.layout.operator("object.create_arc")
        self.layout.operator("object.extrude_straight")

def register():
    bpy.utils.register_class(RoadDesignerProperties)
    bpy.types.Scene.road_tool_props = bpy.props.PointerProperty(type=RoadDesignerProperties)
    bpy.utils.register_class(ExtrudeStraight.ExtrudeStraight)
    bpy.utils.register_class(CreateStraight.CreateStraight)
    bpy.utils.register_class(CreateArc.CreateArc)
    bpy.utils.register_class(VIEW3D_PT_road_tools_panel)

def unregister():
    bpy.utils.unregister_class(ExtrudeStraight.ExtrudeStraight)
    bpy.utils.unregister_class(CreateStraight.CreateStraight)
    bpy.utils.unregister_class(CreateArc.CreateArc)
    bpy.utils.unregister_class(RoadDesignerProperties)
    bpy.utils.unregister_class(VIEW3D_PT_road_tools_panel)
    del bpy.types.Scene.road_tool_props