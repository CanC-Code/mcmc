from PIL import Image
import os

def create_texture(filename, color):
    img = Image.new('RGBA', (16, 16), color)
    img.save(filename)

def main():
    # Ensure the directory exists
    os.makedirs('resource_pack/textures/blocks', exist_ok=True)
    
    # Generate Albedo (Base Color) Images
    create_texture('resource_pack/textures/blocks/chimera_oak_albedo.png', (83, 53, 10, 255)) # Brown Bark
    create_texture('resource_pack/textures/blocks/chimera_oak_leaves_albedo.png', (34, 139, 34, 200)) # Green Leaves

    # Generate MER (Metalness/Emissive/Roughness) Maps
    # A purely black/grey MER map means no glow, no metal, high roughness
    create_texture('resource_pack/textures/blocks/chimera_oak_mer.png', (0, 0, 255, 255)) 
    create_texture('resource_pack/textures/blocks/chimera_oak_leaves_mer.png', (0, 0, 255, 255))
    
    # Generate Normal Maps (Flat normal map color is #8080FF)
    create_texture('resource_pack/textures/blocks/chimera_oak_normal.png', (128, 128, 255, 255))
    create_texture('resource_pack/textures/blocks/chimera_oak_leaves_normal.png', (128, 128, 255, 255))
    
    print("Successfully generated missing texture PNGs.")

if __name__ == "__main__":
    main()
