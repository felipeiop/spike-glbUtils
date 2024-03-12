import bpy
import os

char_dirs = "/Users/felipepesantez/Documents/char/"
char_range = len(os.listdir(char_dirs))

def glb_process():
    for i in range(char_range):
        current_folder = f"{char_dirs}/{i}"
        glb_files = [file for file in os.listdir(current_folder) if file.endswith(".glb")]
        for glb_file in glb_files:
            bpy.ops.import_scene.gltf(filepath=f"{current_folder}/{glb_file}",bone_heuristic="BLENDER")
            # Clear selection
            bpy.ops.object.select_all(action='DESELECT')

            first_armature = None

            for obj in bpy.context.scene.objects:
                if obj.type == 'ARMATURE':
                    if first_armature is None:
                        first_armature = obj
                    else:
                        # Delete all armatures except for the first one
                        bpy.data.objects.remove(obj, do_unlink=True)

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

            # Select the first armature
            if first_armature:
                first_armature.select_set(True)

            bpy.context.view_layer.objects.active = first_armature

            # Iterate through all objects in the scene
            for obj in bpy.context.scene.objects:
                # Check if the object has an armature modifier
                if obj.type == 'MESH' and obj.modifiers.get("Armature"):
                    # Set the armature modifier to the first armature
                    obj.modifiers["Armature"].object = first_armature

        export_obj_ref_name = bpy.context.scene.objects[0].name
        export_name = export_obj_ref_name.split("_")[1]


        output_file = f"{current_folder}/{export_name}.glb"

        # Export the scene as a .glb file
        bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB', export_animations=False)

        print("Export complete. Scene exported to", output_file)
        bpy.ops.wm.read_factory_settings(use_empty=True)

        #optional
        #remove previous glb files
        #for glb_file in glb_files:
        #    os.remove(f"{current_folder}/{glb_file}")

glb_process()
