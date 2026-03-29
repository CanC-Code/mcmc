import os
import json
import random
import numpy as np
from PIL import Image, ImageDraw

random.seed(7)
np.random.seed(7)

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & PATHS
# ═════════════════════════════════════════════════════════════════════════════
P_MODELS    = "resource_pack/models/blocks"
P_TEXTURES  = "resource_pack/textures/blocks"
P_RP_TEXTS  = "resource_pack/texts"
P_BP_BLOCKS = "behavior_pack/blocks"
P_BP_FEAT   = "behavior_pack/features"
P_BP_RULES  = "behavior_pack/feature_rules"

DIRECTORIES = [P_MODELS, P_TEXTURES, P_BP_BLOCKS, P_BP_FEAT, P_BP_RULES, P_RP_TEXTS, "resource_pack/textures"]
for d in DIRECTORIES:
    os.makedirs(d, exist_ok=True)

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ═════════════════════════════════════════════════════════════════════════════
# 1. VANILLA TREE SUPPRESSION
# ═════════════════════════════════════════════════════════════════════════════
print("Writing Vanilla Suppression Rules...")
VANILLA_RULES = {
    "forest_oak_feature_rule": "minecraft:oak_tree_feature",
    "forest_birch_feature_rule": "minecraft:birch_feature",
    "mega_pine_feature_rule": "minecraft:mega_pine_feature",
    "mega_spruce_feature_rule": "minecraft:mega_spruce_feature",
    "roofed_forest_dark_oak_feature_rule": "minecraft:dark_oak_feature",
    "savanna_mutated_acacia_feature_rule": "minecraft:acacia_feature",
    "savanna_acacia_feature_rule": "minecraft:acacia_feature",
    "swampland_oak_feature_rule": "minecraft:swamp_oak_feature",
    "taiga_pine_feature_rule": "minecraft:taiga_pine_feature",
    "jungle_tree_feature_rule": "minecraft:jungle_tree_feature",
    "overworld_surface_oak_feature_rule": "minecraft:oak_tree_feature",
    "overworld_surface_birch_feature_rule": "minecraft:birch_feature",
    "overworld_surface_spruce_feature_rule": "minecraft:spruce_feature",
    "overworld_surface_jungle_feature_rule": "minecraft:jungle_tree_feature",
    "overworld_surface_acacia_feature_rule": "minecraft:acacia_feature",
    "overworld_surface_dark_oak_feature_rule": "minecraft:dark_oak_feature",
    "tall_birch_feature_rule": "minecraft:tall_birch_feature"
}

for rule_id, feature_id in VANILLA_RULES.items():
    rule_data = {
        "format_version": "1.13.0",
        "minecraft:feature_rules": {
            "description": {"identifier": f"minecraft:{rule_id}", "places_feature": feature_id},
            "conditions": {
                "placement_pass": "surface_pass",
                "minecraft:biome_filter": [{"test": "has_biome_tag", "operator": "==", "value": "overworld"}]
            },
            "distribution": {"iterations": 0, "x": 0, "y": 0, "z": 0}
        }
    }
    write_json(f"{P_BP_RULES}/{rule_id}.json", rule_data)

# ═════════════════════════════════════════════════════════════════════════════
# 2. FIXED GEOMETRY
# ═════════════════════════════════════════════════════════════════════════════
print("Writing Geometry...")
bark_geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.round_bark",
            "texture_width": 128, "texture_height": 128,
            "visible_bounds_width": 2, "visible_bounds_height": 2, "visible_bounds_offset": [0, 0.5, 0]
        },
        "bones": [{
            "name": "trunk",
            "pivot": [0, 0, 0],
            "cubes": [
                {"origin": [-2, 0, -7], "size": [4, 16, 14], "uv": {"north": {"uv": [0,0], "uv_size": [4,16]}, "south": {"uv": [0,0], "uv_size": [4,16]}, "east": {"uv": [0,0], "uv_size": [14,16]}, "west": {"uv": [0,0], "uv_size": [14,16]}, "up": {"uv": [0,0], "uv_size": [4,14]}, "down": {"uv": [0,0], "uv_size": [4,14]}}},
                {"origin": [-7, 0, -2], "size": [14, 16, 4], "uv": {"north": {"uv": [0,0], "uv_size": [14,16]}, "south": {"uv": [0,0], "uv_size": [14,16]}, "east": {"uv": [0,0], "uv_size": [4,16]}, "west": {"uv": [0,0], "uv_size": [4,16]}, "up": {"uv": [0,0], "uv_size": [14,4]}, "down": {"uv": [0,0], "uv_size": [14,4]}}},
                {"origin": [-3, 0, -6], "size": [6, 16, 12], "uv": {"north": {"uv": [0,0], "uv_size": [6,16]}, "south": {"uv": [0,0], "uv_size": [6,16]}, "east": {"uv": [0,0], "uv_size": [12,16]}, "west": {"uv": [0,0], "uv_size": [12,16]}, "up": {"uv": [0,0], "uv_size": [6,12]}, "down": {"uv": [0,0], "uv_size": [6,12]}}},
                {"origin": [-6, 0, -3], "size": [12, 16, 6], "uv": {"north": {"uv": [0,0], "uv_size": [12,16]}, "south": {"uv": [0,0], "uv_size": [12,16]}, "east": {"uv": [0,0], "uv_size": [6,16]}, "west": {"uv": [0,0], "uv_size": [6,16]}, "up": {"uv": [0,0], "uv_size": [12,6]}, "down": {"uv": [0,0], "uv_size": [12,6]}}},
                {"origin": [-4, 0, -5], "size": [8, 16, 10], "uv": {"north": {"uv": [0,0], "uv_size": [8,16]}, "south": {"uv": [0,0], "uv_size": [8,16]}, "east": {"uv": [0,0], "uv_size": [10,16]}, "west": {"uv": [0,0], "uv_size": [10,16]}, "up": {"uv": [0,0], "uv_size": [8,10]}, "down": {"uv": [0,0], "uv_size": [8,10]}}},
                {"origin": [-5, 0, -4], "size": [10, 16, 8], "uv": {"north": {"uv": [0,0], "uv_size": [10,16]}, "south": {"uv": [0,0], "uv_size": [10,16]}, "east": {"uv": [0,0], "uv_size": [8,16]}, "west": {"uv": [0,0], "uv_size": [8,16]}, "up": {"uv": [0,0], "uv_size": [10,8]}, "down": {"uv": [0,0], "uv_size": [10,8]}}}
            ]
        }]
    }]
}
write_json(f"{P_MODELS}/round_bark.geo.json", bark_geo)

leaves_geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.chimera_leaves",
            "texture_width": 64, "texture_height": 64,
            "visible_bounds_width": 2, "visible_bounds_height": 2, "visible_bounds_offset": [0, 0.5, 0]
        },
        "bones": [{
            "name": "canopy",
            "pivot": [0, 0, 0],
            "cubes": [{"origin": [-8, 0, -8], "size": [16, 16, 16], "uv": {"north": {"uv": [0,0], "uv_size": [64,64]}, "south": {"uv": [0,0], "uv_size": [64,64]}, "east": {"uv": [0,0], "uv_size": [64,64]}, "west": {"uv": [0,0], "uv_size": [64,64]}, "up": {"uv": [0,0], "uv_size": [64,64]}, "down": {"uv": [0,0], "uv_size": [64,64]}}}]
        }]
    }]
}
write_json(f"{P_MODELS}/leaves.geo.json", leaves_geo)

# ═════════════════════════════════════════════════════════════════════════════
# 3. CHIMERA BLOCKS & FEATURES
# ═════════════════════════════════════════════════════════════════════════════
print("Writing Chimera Blocks and Features...")
bark_block = {
    "format_version": "1.20.80",
    "minecraft:block": {
        "description": {"identifier": "chimera:high_poly_bark", "menu_category": {"category": "nature"}},
        "components": {
            "minecraft:geometry": "geometry.round_bark",
            "minecraft:collision_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
            "minecraft:selection_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 1.5},
            "minecraft:material_instances": {
                "*": {"texture": "chimera_oak_bark", "render_method": "opaque"},
                "top": {"texture": "chimera_oak_top", "render_method": "opaque"},
                "down": {"texture": "chimera_oak_top", "render_method": "opaque"}
            }
        }
    }
}
write_json(f"{P_BP_BLOCKS}/chimera_high_poly_bark.json", bark_block)

leaves_block = {
    "format_version": "1.20.80",
    "minecraft:block": {
        "description": {"identifier": "chimera:high_poly_leaves", "menu_category": {"category": "nature"}},
        "components": {
            "minecraft:geometry": "geometry.chimera_leaves",
            "minecraft:collision_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
            "minecraft:selection_box": {"origin": [-8, 0, -8], "size": [16, 16, 16]},
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 0.2},
            "minecraft:light_dampening": 0,
            "minecraft:material_instances": {
                "*": {"texture": "chimera_oak_leaves", "render_method": "alpha_test"}
            }
        }
    }
}
write_json(f"{P_BP_BLOCKS}/chimera_high_poly_leaves.json", leaves_block)

feature = {
    "format_version": "1.13.0",
    "minecraft:tree_feature": {
        "description": {"identifier": "chimera:oak_feature"},
        "base_block": ["minecraft:grass", "minecraft:dirt", "minecraft:podzol"],
        "trunk": {"trunk_block": "chimera:high_poly_bark", "trunk_height": {"range_min": 6, "range_max": 10}},
        "leaf_parameters": {"leaf_block": "chimera:high_poly_leaves", "fill_radius": {"range_min": 4, "range_max": 6}}
    }
}
write_json(f"{P_BP_FEAT}/chimera_oak_feature.json", feature)

rule = {
    "format_version": "1.13.0",
    "minecraft:feature_rules": {
        "description": {"identifier": "chimera:oak_feature_rule", "places_feature": "chimera:oak_feature"},
        "conditions": {
            "placement_pass": "surface_pass",
            "minecraft:biome_filter": [{"test": "has_biome_tag", "operator": "==", "value": "overworld"}]
        },
        "distribution": {
            "iterations": 20, 
            "x": {"distribution": "uniform", "extent": [0, 16]},
            "y": "query.heightmap(variable.worldx, variable.worldz)",
            "z": {"distribution": "uniform", "extent": [0, 16]}
        }
    }
}
write_json(f"{P_BP_RULES}/chimera_oak_feature_rule.json", rule)

# ═════════════════════════════════════════════════════════════════════════════
# 4. RESOURCE PACK MAPPINGS (Critical Fixes Here)
# ═════════════════════════════════════════════════════════════════════════════
print("Writing Resource Pack Mappings...")

rp_blocks = {
    "format_version": "1.1.0",
    "chimera:high_poly_bark": {"textures": "chimera_oak_bark", "sound": "wood"},
    "chimera:high_poly_leaves": {"textures": "chimera_oak_leaves", "sound": "grass"}
}
write_json("resource_pack/blocks.json", rp_blocks)

# NEW: Bedrock absolutely requires this to map names to files
terrain_texture = {
    "resource_pack_name": "chimera_rp",
    "texture_name": "atlas.terrain",
    "padding": 8,
    "num_mip_levels": 4,
    "texture_data": {
        "chimera_oak_bark": {"textures": "textures/blocks/chimera_oak_bark"},
        "chimera_oak_top": {"textures": "textures/blocks/chimera_oak_top"},
        "chimera_oak_leaves": {"textures": "textures/blocks/chimera_oak_leaves"}
    }
}
write_json("resource_pack/textures/terrain_texture.json", terrain_texture)

with open(f"{P_RP_TEXTS}/en_US.lang", "w") as f:
    f.write("tile.chimera:high_poly_bark.name=Round Oak Log\n")
    f.write("tile.chimera:high_poly_leaves.name=Round Oak Leaves\n")

# ═════════════════════════════════════════════════════════════════════════════
# 5. TEXTURE GENERATION & PBR MAPPING
# ═════════════════════════════════════════════════════════════════════════════
print("Generating Textures with PIL...")

def sobel_normal(img_rgba, strength=3.5):
    g = np.array(img_rgba.convert("L"), dtype=np.float32) / 255.0
    dx = np.zeros_like(g); dy = np.zeros_like(g)
    dx[:, 1:-1] = (g[:, 2:] - g[:, :-2]) * strength
    dy[1:-1, :] = (g[2:, :] - g[:-2, :]) * strength
    nx = dx.clip(-1,1); ny = dy.clip(-1,1); nz = np.ones_like(nx)
    ln = np.sqrt(nx**2 + ny**2 + nz**2) + 1e-8
    nx, ny, nz = nx/ln, ny/ln, nz/ln
    return Image.fromarray(np.stack([
        ((nx+1)*.5*255).astype(np.uint8), ((ny+1)*.5*255).astype(np.uint8), ((nz+1)*.5*255).astype(np.uint8),
    ], axis=2), "RGB")

def flat_mer(size=128, roughness=205):
    return Image.new("RGB", (size,size), (0, 0, roughness))

S = 128

# --- BARK ---
bark = Image.new("RGBA", (S,S), (60, 38, 15, 255))
db = ImageDraw.Draw(bark)
for _ in range(220):
    x = random.randint(0, S-1)
    db.line([(x,0),(x+random.randint(-5,5), S-1)], fill=(random.randint(28,75),random.randint(17,45),random.randint(4,17),255), width=random.randint(1,3))

bark.save(f"{P_TEXTURES}/chimera_oak_bark.png")
sobel_normal(bark, strength=4.5).save(f"{P_TEXTURES}/chimera_oak_bark_normal.png")
flat_mer(S, 208).save(f"{P_TEXTURES}/chimera_oak_bark_mer.png")

# PBR Texture Set for Bark
write_json(f"{P_TEXTURES}/chimera_oak_bark.texture_set.json", {
    "format_version": "1.16.100",
    "minecraft:texture_set": {
        "color": "chimera_oak_bark",
        "metalness_emissive_roughness": "chimera_oak_bark_mer",
        "normal": "chimera_oak_bark_normal"
    }
})

# --- TOP ---
top = Image.new("RGBA", (S,S), (48, 28, 9, 255))
top.save(f"{P_TEXTURES}/chimera_oak_top.png")
sobel_normal(top, strength=2.8).save(f"{P_TEXTURES}/chimera_oak_top_normal.png")
flat_mer(S, 195).save(f"{P_TEXTURES}/chimera_oak_top_mer.png")

write_json(f"{P_TEXTURES}/chimera_oak_top.texture_set.json", {
    "format_version": "1.16.100",
    "minecraft:texture_set": {
        "color": "chimera_oak_top",
        "metalness_emissive_roughness": "chimera_oak_top_mer",
        "normal": "chimera_oak_top_normal"
    }
})

# --- LEAVES (NEW: Procedurally generated with transparency for alpha test) ---
leaves = Image.new("RGBA", (S,S), (0, 0, 0, 0)) # Fully transparent base
dl = ImageDraw.Draw(leaves)
for _ in range(1500):
    x, y = random.randint(-5, S), random.randint(-5, S)
    r = random.randint(3, 8)
    color = (random.randint(30, 60), random.randint(100, 160), random.randint(20, 50), 255)
    dl.ellipse([x, y, x+r, y+r], fill=color)

leaves.save(f"{P_TEXTURES}/chimera_oak_leaves.png")
# No MER/Normal needed for leaves usually, but you can add them later if desired.

print("Files and textures generated successfully!")
