import json
import math
import os

def create_bone(name, parent, pivot, rotation, size, uv):
    """Creates a Bedrock-compatible bone with a single cube."""
    return {
        "name": name,
        "parent": parent,
        "pivot": pivot,
        "rotation": rotation,
        "cubes": [
            {
                "origin": [pivot[0] - size[0]/2, pivot[1], pivot[2] - size[2]/2],
                "size": size,
                "uv": uv
            }
        ]
    }

def grow_branch(bones, parent_name, start_pos, length, width, angle_xz, angle_y, depth):
    if depth <= 0 or length < 1:
        return

    bone_name = f"branch_d{depth}_a{int(angle_xz)}"
    
    # Calculate end position for the next pivot
    # Bedrock rotations are in degrees
    rad_xz = math.radians(angle_xz)
    rad_y = math.radians(angle_y)
    
    # Create the current segment
    bones.append(create_bone(
        name=bone_name,
        parent=parent_name,
        pivot=start_pos,
        rotation=[angle_y, angle_xz, 0],
        size=[width, length, width],
        uv=[0, 0]
    ))

    # Calculate next start point (top of current branch)
    new_start = [start_pos[0], start_pos[1] + length, start_pos[2]]
    
    # Recursive call for two new branches (splitting)
    grow_branch(bones, bone_name, new_start, length * 0.7, width * 0.7, angle_xz + 30, 20, depth - 1)
    grow_branch(bones, bone_name, new_start, length * 0.7, width * 0.7, angle_xz - 30, -20, depth - 1)

def main():
    bones = []
    # Starting trunk
    grow_branch(bones, None, [0, 0, 0], 12, 4, 0, 0, 4)

    output = {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry.chimera_oak",
                "texture_width": 64,
                "texture_height": 64,
                "visible_bounds_width": 16,
                "visible_bounds_height": 32,
                "visible_bounds_offset": [0, 8, 0]
            },
            "bones": bones
        }]
    }

    # Ensure directory exists for local testing
    os.makedirs('resource_pack/models/blocks', exist_ok=True)
    
    with open('resource_pack/models/blocks/chimera_oak.geo.json', 'w') as f:
        json.dump(output, f, indent=4)
    print("Successfully generated high-poly tree geometry.")

if __name__ == "__main__":
    main()
