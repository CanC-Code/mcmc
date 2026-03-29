import json
import math

def create_branch(name, origin, size, rotation, parent=None):
    return {
        "name": name,
        "parent": parent,
        "pivot": origin,
        "rotation": rotation,
        "cubes": [
            {
                "origin": [origin[0] - size[0]/2, origin[1], origin[2] - size[2]/2],
                "size": size,
                "uv": [0, 0]
            }
        ]
    }

def generate_tree_geo():
    bones = []
    # Create a trunk
    bones.append(create_branch("trunk", [0, 0, 0], [4, 12, 4], [0, 0, 0]))
    
    # Generate recursive branches for "Realism"
    for i in range(5):
        angle = (360 / 5) * i
        rad = math.radians(angle)
        # Tapered branches extending outward
        bones.append(create_branch(
            f"branch_{i}", 
            [0, 10, 0], 
            [2, 8, 2], 
            [30, angle, 0], 
            parent="trunk"
        ))

    geo_data = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.chimera_oak",
                    "texture_width": 64,
                    "texture_height": 64,
                    "visible_bounds_width": 10,
                    "visible_bounds_height": 20,
                    "visible_bounds_offset": [0, 10, 0]
                },
                "bones": bones
            }
        ]
    }

    with open('resource_pack/models/blocks/chimera_oak.geo.json', 'w') as f:
        json.dump(geo_data, f, indent=4)

if __name__ == "__main__":
    generate_tree_geo()
