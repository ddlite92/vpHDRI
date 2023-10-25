import bpy
import os
import sys

scene = bpy.context.scene
for area in bpy.context.screen.areas: # iterate through areas in current screen
    if area.type == 'VIEW_3D':
        for space in area.spaces: # iterate through spaces in current VIEW_3D area
            if space.type == 'VIEW_3D': # check if space is a 3D view
                space.shading.type = 'RENDERED' # set the viewport shading to rendered
                space.shading.use_scene_world_render = False
                
bpy.data.worlds["World"].use_nodes = True

C = bpy.context
scn = C.scene

# Get the environment node tree of the current scene
node_tree = scn.world.node_tree
tree_nodes = node_tree.nodes

# Clear all nodes
tree_nodes.clear()

# Add nodes

node_coor = tree_nodes.new(type='ShaderNodeTexCoord')
node_coor.location = -700,42

node_lgtpath = tree_nodes.new(type='ShaderNodeLightPath')
node_lgtpath.location = -500,335

node_map = tree_nodes.new(type='ShaderNodeMapping')
node_map.location = -500,13

node_environment = tree_nodes.new('ShaderNodeTexEnvironment')
node_environment.image = bpy.data.images.load("//textures/sunrise.exr") # Relative path
node_environment.location = -240,50

node_multiply = tree_nodes.new(type='ShaderNodeMath')
node_multiply.operation = 'MULTIPLY'
node_multiply.inputs[1].default_value = 1
node_multiply.location = -240,335

node_mix = tree_nodes.new(type='ShaderNodeMixRGB')
node_mix.inputs[2].default_value = [0.050876, 0.050876, 0.050876, 1.000000]
node_mix.location = 100,335

node_background = tree_nodes.new(type='ShaderNodeBackground')
node_background.location = 340,335


node_output = tree_nodes.new(type='ShaderNodeOutputWorld')   
node_output.location = 600,335

# Link all nodes
links = node_tree.links
link = links.new(node_coor.outputs["Generated"], node_map.inputs["Vector"])
link = links.new(node_map.outputs["Vector"], node_environment.inputs["Vector"])
link = links.new(node_lgtpath.outputs["Is Camera Ray"], node_multiply.inputs["Value"])
link = links.new(node_multiply.outputs["Value"], node_mix.inputs["Fac"])
link = links.new(node_environment.outputs["Color"], node_mix.inputs["Color1"])
link = links.new(node_mix.outputs["Color"], node_background.inputs["Color"])
link = links.new(node_background.outputs["Background"], node_output.inputs["Surface"])


bpy.data.scenes["Scene"].render.image_settings.file_format = "OPEN_EXR_MULTILAYER"
bpy.ops.wm.save_mainfile(compress=True,relative_remap=True,)



""" if scene.cgru:
    bpy.context.scene.cgru.pause = True
    bpy.context.scene.cgru.relativePaths = True
    bpy.context.scene.cgru.use_all_scenes = False
    bpy.context.scene.cgru.fpertask = 1
    bpy.ops.cgru.submit() """