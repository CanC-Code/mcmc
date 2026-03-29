import bpy
import os
import json

def setup_render_env():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.object.camera_add(location=(0, 0, 5))
    cam = bpy.context.object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 2.0
    bpy.context.scene.camera = cam
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.image_settings.color_depth = '8'
    bpy.context.scene.cycles.use_denoising = False
    bpy.context.scene.cycles.samples = 32

def create_bark_material(mat):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 15.0
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.05, 0.03, 0.01, 1) 
    ramp.color_ramp.elements[1].color = (0.15, 0.08, 0.03, 1) 
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

def create_leaf_material(mat):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.inputs['Scale'].default_value = 25.0
    alpha_ramp = nodes.new('ShaderNodeValToRGB')
    alpha_ramp.color_ramp.elements[0].position = 0.4
    alpha_ramp.color_ramp.elements[0].color = (0, 0, 0, 1) 
    alpha_ramp.color_ramp.elements[1].position = 0.5
    alpha_ramp.color_ramp.elements[1].color = (1, 1, 1, 1) 
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].color = (0.02, 0.1, 0.02, 1) 
    color_ramp.color_ramp.elements[1].color = (0.08, 0.25, 0.05, 1) 
    links.new(voronoi.outputs['Distance'], alpha_ramp.inputs['Fac'])
    links.new(voronoi.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(alpha_ramp.outputs['Color'], bsdf.inputs['Alpha'])
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

def render_texture(filename, material_setup_func):
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0,0,0))
    plane = bpy.context.object
    mat = bpy.data.materials.new(name="GenMat")
    material_setup_func(mat)
    plane.data.materials.append(mat)
    out_dir = os.path.abspath('resource_pack/textures/blocks')
    os.makedirs(out_dir, exist_ok=True)
    bpy.context.scene.render.filepath = os.path.join(out_dir, filename)
    bpy.ops.render.render(write_still=True)
    bpy.ops.object.delete()

def nuke_vanilla_trees():
    rules_dir = 'behavior_pack/feature_rules'
    os.makedirs(rules_dir, exist_ok=True)
    
    # CRITICAL FIX: Mapping the rule to the EXACT valid feature identifier
    vanilla_rules = {
        'forest_oak_feature_rule': 'minecraft:oak_tree_feature',
        'forest_birch_feature_rule': 'minecraft:birch_tree_feature',
        'overworld_surface_oak_feature_rule': 'minecraft:oak_tree_feature',
        'plains_tree_feature_rule': 'minecraft:oak_tree_feature',
        'taiga_pine_feature_rule': 'minecraft:taiga_pine_feature',
        'mega_oak_feature_rule': 'minecraft:mega_oak_feature',
        'swamp_tree_feature_rule': 'minecraft:swamp_tree_feature',
        'savanna_tree_feature_rule': 'minecraft:savanna_tree_feature',
        'jungle_tree_feature_rule': 'minecraft:jungle_tree_feature',
        'snowy_taiga_pine_feature_rule': 'minecraft:taiga_pine_feature',
        'birch_feature_rule': 'minecraft:birch_tree_feature',
        'roofed_forest_tree_feature_rule': 'minecraft:roofed_forest_tree_feature'
    }
    
    for rule, feature in vanilla_rules.items():
        null_data = {
          "format_version": "1.13.0",
          "minecraft:feature_rules": {
            "description": { "identifier": f"minecraft:{rule}", "places_feature": feature },
            "conditions": { "placement_pass": "surface_pass" },
            "distribution": { "iterations": 0, "x": 0, "y": 0, "z": 0 }
          }
        }
        with open(os.path.join(rules_dir, f"{rule}.json"), 'w') as f:
            json.dump(null_data, f, indent=4)

if __name__ == "__main__":
    nuke_vanilla_trees()
    setup_render_env()
    render_texture('chimera_oak_bark.png', create_bark_material)
    render_texture('chimera_oak_leaves.png', create_leaf_material)
