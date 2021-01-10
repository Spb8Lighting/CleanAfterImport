# ====================== BEGIN GPL LICENSE BLOCK ======================
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
# ======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

import bpy # noqa pylint: disable=import-error
bl_info = {
    "author": "Sylvain Guiblain (spb8)",
    "name": "Clean After Import",
    "location": "Object > Clean After Import",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "description": "Clean Objects and Meshs by batch",
    "category": "Object",
    "tracker_url": "https://github.com/Spb8Lighting/CleanAfterImport"
}


class CleanAfterImport(bpy.types.Operator):
    """Clean After Import"""
    bl_idname = "object.clean_after_import"
    bl_label = "Clean After Import"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Parse all objects
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                # Remove last _ or _1
                if obj.name[-1] == '_':
                    obj.name = obj.name[:-1]
                elif obj.name[-2] == '_1':
                    obj.name = obj.name[:-2]
                # Rename MESH with Object Name in UPPERCASE
                obj.name = obj.name.upper()
                obj.data.name = obj.name
                # Remove Double Vextex
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(
                    use_extend=False, use_expand=False, type='VERT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=0.0001)
                bpy.ops.object.mode_set(mode='OBJECT')
                # Apply Normals: Auto Smooth with an angle of 32.9°
                obj.data.use_auto_smooth = True
                obj.data.auto_smooth_angle = 0.5742127510917031
                # Add modifier "Decimate as 0.5° Planar and Normal
                obj.modifiers.clear()
                if len(obj.data.polygons) > 1:
                    modDec = obj.modifiers.new('Decimate', type='DECIMATE')
                    modDec.decimate_type = 'DISSOLVE'
                    modDec.angle_limit = 0.00872665
                    modDec.delimit = {'NORMAL'}
                    modDec.name = 'Clean'

        # Apply all transform except location
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=True)
        
        # Set UNITS values
        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.scale_length = 0.01
        bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(CleanAfterImport.bl_idname)


def register():
    bpy.utils.register_class(CleanAfterImport)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CleanAfterImport)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
