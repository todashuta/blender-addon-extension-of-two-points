# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import bmesh


bl_info = {
    "name": "Extension Of Two Points",
    "author": "Toda Shuta",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > EditMode > Tool Bar > Tool > Extension Of Two Points",
    "description": "Extension Of Two Points",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}


class EXTENSION_OF_TWO_POINTS_OT_main(bpy.types.Operator):
    bl_idname = "object.extension_of_two_points"
    bl_label = "Extension Of Two Points"

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return context.mode == "EDIT_MESH" and context.tool_settings.mesh_select_mode[:] == (True, False, False)

    def execute(self, context):
        scene = context.scene
        obj = context.object
        if not obj.type == "MESH":
            return {"CANCELLED"}

        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        if len(bm.select_history) < 2:
            self.report({"ERROR"}, "More than one vertex must be selected.")
            return {"CANCELLED"}

        bp = bm.select_history[-2]
        ep = bm.select_history[-1]

        assert type(bp) is bmesh.types.BMVert and type(ep) is bmesh.types.BMVert, "Invalid Context"

        a = obj.matrix_world @ bp.co
        b = obj.matrix_world @ ep.co
        n = scene.extensionOfTwoPoints_length
        m = n+(a-b).length
        scene.cursor.location = ((-n*a.x+m*b.x)/(m-n), (-n*a.y+m*b.y)/(m-n), (-n*a.z+m*b.z)/(m-n))

        return {"FINISHED"}


class EXTENSION_OF_TWO_POINTS_PT_panel(bpy.types.Panel):
    bl_label = "Extension Of Two Points"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "extensionOfTwoPoints_length")
        layout.operator(EXTENSION_OF_TWO_POINTS_OT_main.bl_idname, text=EXTENSION_OF_TWO_POINTS_OT_main.bl_label)


classes = (
        EXTENSION_OF_TWO_POINTS_OT_main,
        EXTENSION_OF_TWO_POINTS_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.extensionOfTwoPoints_length = bpy.props.FloatProperty(name="Length", default=1.0)


def unregister():
    if hasattr(bpy.types.Scene, "extensionOfTwoPoints_length"):
        del bpy.types.Scene.extensionOfTwoPoints_length

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
