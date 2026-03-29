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
    
    # Forcefully delete ALL ghost files causing engine collisions
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
            print(f"Deleted outdated file: {file_path}")
            
    print("Successfully generated exact texture PNGs and cleaned up directory.")

if __name__ == "__main__":
    main()
