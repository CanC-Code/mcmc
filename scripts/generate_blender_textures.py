import bpy
import os

def setup_render_env():
    # Clear default scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Setup Orthographic Camera
    bpy.ops.object.camera_add(location=(0, 0, 5))
    cam = bpy.context.object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 2.0
    bpy.context.scene.camera = cam
    
    # Render Settings (256x256 for high quality Bedrock textures)
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.resolution_x = 256
    bpy.context.scene.render.resolution_y = 256
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    
    # CRITICAL FIX: Disable Denoising for Headless Linux Runners
    bpy.context.scene.cycles.use_denoising = False
    
    # Optional: Lower samples for faster GitHub Actions builds
    bpy.context.scene.cycles.samples = 32

def create_bark_material(mat):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Procedural Noise for Bark Grooves
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 10.0
    
    # Color Ramp for deep browns
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.05, 0.03, 0.01, 1) # Dark brown
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[1].color = (0.15, 0.08, 0.03, 1) # Light bark
    
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
    
    # Voronoi for leaf clusters and alpha cutouts
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.inputs['Scale'].default_value = 25.0
    
    # Alpha threshold (creates gaps in the leaves)
    alpha_ramp = nodes.new('ShaderNodeValToRGB')
    alpha_ramp.color_ramp.elements[0].position = 0.4
    alpha_ramp.color_ramp.elements[0].color = (0, 0, 0, 1) # Transparent
    alpha_ramp.color_ramp.elements[1].position = 0.5
    alpha_ramp.color_ramp.elements[1].color = (1, 1, 1, 1) # Opaque
    
    # Green color variation
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].color = (0.02, 0.1, 0.02, 1) # Dark green
    color_ramp.color_ramp.elements[1].color = (0.08, 0.25, 0.05, 1) # Bright green
    
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

def clean_old_files():
    bad_files = [
        'resource_pack/textures/blocks/chimera_oak_bark.texture_set.json',
        'resource_pack/textures/blocks/chimera_oak_leaves.texture_set.json',
        'behavior_pack/features/chimera_dummy_void.json',
        'behavior_pack/blocks/chimera_oak_tree.json',
        'resource_pack/models/blocks/chimera_oak.geo.json'
    ]
    for file_path in bad_files:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    clean_old_files()
    setup_render_env()
    render_texture('chimera_oak_bark.png', create_bark_material)
    render_texture('chimera_oak_leaves.png', create_leaf_material)
