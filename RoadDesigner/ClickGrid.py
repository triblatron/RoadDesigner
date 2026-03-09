import bpy

class ClickGrid(bpy.types.Operator):
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
    bpy.utils.register_class(ClickGrid)

def unregister():
    bpy.utils.unregister_class(ClickGrid)

