bl_info = {
    "name": "Align To Object",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Object > Align To Object",
    "description": "Aligns the active object to the selected object",
    "warning": "",
    "doc_url": "",
    "category": "Object"
}

import bpy
import mathutils

class AlignToObjectsOperator(bpy.types.Operator):
    bl_idname = "object.align_to_objects"
    bl_label = "Align to Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) != 2:
            self.report({'ERROR'}, "Please select exactly two mesh objects.")
            return {'CANCELLED'}
        object_1 = selected_objects[0]
        object_2 = selected_objects[1]
        if not object_1.type == 'MESH' or not object_2.type == 'MESH':
            self.report({'ERROR'}, "Please select two mesh objects.")
            return {'CANCELLED'}
        if object_1 == object_2:
            self.report({'ERROR'}, "Please select two different mesh objects.")
            return {'CANCELLED'}
        # Determine which object to move
        if object_1.select_get():
            object_to_move = object_1
            reference_object = object_2
        else:
            object_to_move = object_2
            reference_object = object_1
        # Get the world coordinates of the lowest point on the object to move and the highest point on the reference object
        object_to_move_verts = object_to_move.data.vertices
        lowest_point = None
        for vert in object_to_move_verts:
            world_pos = object_to_move.matrix_world @ vert.co
            if lowest_point is None or world_pos.z < lowest_point.z:
                lowest_point = world_pos
        reference_object_verts = reference_object.data.vertices
        highest_point = None
        for vert in reference_object_verts:
            world_pos = reference_object.matrix_world @ vert.co
            if highest_point is None or world_pos.z > highest_point.z:
                highest_point = world_pos
        # Calculate the necessary translation
        delta_x = reference_object.location.x - object_to_move.location.x
        delta_y = reference_object.location.y - object_to_move.location.y
        delta_z = highest_point.z - lowest_point.z
        # Apply the translation
        object_to_move.location = mathutils.Vector((reference_object.location.x, reference_object.location.y, object_to_move.location.z + delta_z))
        return {'FINISHED'}

def menu_draw(self, context):
    self.layout.separator()
    self.layout.operator("object.align_to_objects")

def register():
    bpy.utils.register_class(AlignToObjectsOperator)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(AlignToObjectsOperator)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_draw)

if __name__ == "__main__":
    register()
