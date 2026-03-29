from PIL import Image
import os

def create_texture(filename, color):
    img = Image.new('RGBA', (16, 16), color)
    img.save(filename)

def main():
    # Ensure the directory exists
    os.makedirs('resource_pack/textures/blocks', exist_ok=True)
    
    # Generate exact file names matching terrain_texture.json
    create_texture('resource_pack/textures/blocks/chimera_oak_bark.png', (83, 53, 10, 255)) # Brown
    create_texture('resource_pack/textures/blocks/chimera_oak_leaves.png', (34, 139, 34, 200)) # Green
    
    print("Successfully generated exact texture PNGs.")

if __name__ == "__main__":
    main()
