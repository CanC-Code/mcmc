import nbtlib
from nbtlib.tag import *
import os

def create_tree_structure():
    # Grid Dimensions (X, Y, Z)
    size_x, size_y, size_z = 7, 12, 7
    
    # Palette definition matching our JSON blocks
    palette_data = List[Compound]([
        Compound({"name": String("minecraft:air"), "states": Compound({})}),
        Compound({"name": String("chimera:high_poly_bark"), "states": Compound({})}),
        Compound({"name": String("chimera:high_poly_leaves"), "states": Compound({})})
    ])

    total_blocks = size_x * size_y * size_z
    block_indices = [0] * total_blocks

    def get_index(x, y, z):
        return (x * size_y * size_z) + (y * size_z) + z

    center_x, center_z = size_x // 2, size_z // 2

    # 1. Generate Trunk
    for y in range(0, size_y - 3):
        block_indices[get_index(center_x, y, center_z)] = 1

    # 2. Generate Organic Canopy
    for y in range(size_y - 5, size_y):
        for x in range(center_x - 2, center_x + 3):
            for z in range(center_z - 2, center_z + 3):
                if (x - center_x)**2 + (y - (size_y-3))**2 + (z - center_z)**2 < 8:
                    if block_indices[get_index(x, y, z)] == 0:
                        block_indices[get_index(x, y, z)] = 2

    structure_nbt = Compound({
        "format_version": Int(1),
        "size": List[Int]([Int(size_x), Int(size_y), Int(size_z)]),
        "structure_world_origin": List[Int]([Int(0), Int(0), Int(0)]),
        "structure": Compound({
            "block_indices": List[List[Int]]([List[Int](list(map(Int, block_indices)))]),
            "entities": List[Compound]([]),
            "palette": Compound({
                "default": Compound({
                    "block_palette": palette_data,
                    "block_position_data": Compound({})
                })
            })
        })
    })

    os.makedirs('behavior_pack/structures/mystructure', exist_ok=True)
    nbt_file = nbtlib.File(structure_nbt)
    nbt_file.save('behavior_pack/structures/mystructure/chimera_oak_1.mcstructure', byteorder='little')
    print("Successfully compiled procedural tree to .mcstructure")

if __name__ == "__main__":
    create_tree_structure()
