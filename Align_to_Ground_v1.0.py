bl_info = {
    "name": "Align to Ground",
    "author": "suhuan",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Object",
    "description": "Align selected object to the ground",
    "warning": "",
    "doc_url": "https://github.com/kukuli99/Blender-Tools/blob/main/README.md",
    "category": "Object",
}

import bpy

addon_keymaps = []

class OBJECT_OT_align_to_ground(bpy.types.Operator):
    bl_idname = "object.align_to_ground"
    bl_label = "Align to Ground"
    bl_description = "Align selected object to the ground"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object

        if obj.type != 'MESH':
            self.report({'ERROR'}, "该对象不支持对齐")
            return {'CANCELLED'}

        min_z = None
        for v in obj.data.vertices:
            v_world = obj.matrix_world @ v.co
            if min_z is None or v_world.z < min_z:
                min_z = v_world.z
        if min_z is not None:
            obj.location.z -= min_z
        return {'FINISHED'}

def menu_draw(self, context):
    self.layout.operator(OBJECT_OT_align_to_ground.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_align_to_ground)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_draw)

    # Add shortcut to the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(OBJECT_OT_align_to_ground.bl_idname, 'G', 'PRESS', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_align_to_ground)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_draw)

    # Remove shortcut from the keymap
    wm = bpy.context.window_manager
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def cleanup(dummy):
    unregister()

# Add the cleanup function as a handler
bpy.app.handlers.load_post.append(cleanup)

if __name__ == "__main__":
    register()
