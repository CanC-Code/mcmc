import os
import json
import random
import numpy as np
from PIL import Image, ImageDraw

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & PATHS
# ═════════════════════════════════════════════════════════════════════════════
P_MODELS    = "resource_pack/models/blocks"
P_TEXTURES  = "resource_pack/textures/blocks"
P_BP_BLOCKS = "behavior_pack/blocks"
P_BP_FEAT   = "behavior_pack/features"
P_BP_RULES  = "behavior_pack/feature_rules"
P_RP_TEXTS  = "resource_pack/texts"

DIRECTORIES = [P_MODELS, P_TEXTURES, P_BP_BLOCKS, P_BP_FEAT, P_BP_RULES, P_RP_TEXTS, "resource_pack"]
for d in DIRECTORIES:
    os.makedirs(d, exist_ok=True)

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ═════════════════════════════════════════════════════════════════════════════
# 1. VANILLA TREE SUPPRESSION
# ═════════════════════════════════════════════════════════════════════════════
# Dictionary mapping the rule name to the feature it places
VANILLA_TREES_TO_REMOVE = {
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
    "overworld_surface_dark_oak_feature_rule": "minecraft:dark_oak_feature"
}

print("Writing Vanilla Suppression Rules...")
for rule_name, feature_name in VANILLA_TREES_TO_REMOVE.items():
    rule_data = {
        "format_version": "1.13.0",
        "minecraft:feature_rules": {
            "description": {
                "identifier": f"minecraft:{rule_name}",
                "places_feature": feature_name
            },
            "conditions": {
                "placement_pass": "surface_pass",
                "minecraft:biome_filter": [{"test": "has_biome_tag", "operator": "==", "value": "overworld"}]
            },
            "distribution": {
                "iterations": 0, # This is the key: 0 iterations means it never spawns
                "x": 0, "y": 0, "z": 0
            }
        }
    }
    write_json(f"{P_BP_RULES}/{rule_name}.json", rule_data)

# ═════════════════════════════════════════════════════════════════════════════
# 2. FIXED GEOMETRY (Single Bone)
# ═════════════════════════════════════════════════════════════════════════════
print("Writing Corrected Geometry...")
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
            # All cubes are safely inside the single "trunk" bone. No child bones used.
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

# ═════════════════════════════════════════════════════════════════════════════
# 3. CHIMERA BLOCKS & GENERATION FEATURES
# ═════════════════════════════════════════════════════════════════════════════
print("Writing Chimera Blocks and Features...")

# The High Poly Bark Block
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

# The High Poly Leaves Block
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

# The Tree Feature (Structure)
feature = {
    "format_version": "1.13.0",
    "minecraft:tree_feature": {
        "description": {"identifier": "chimera:oak_feature"},
        "base_block": ["minecraft:grass", "minecraft:dirt", "minecraft:podzol"],
        "trunk": {
            "trunk_block": "chimera:high_poly_bark",
            "trunk_height": {"range_min": 6, "range_max": 10}
        },
        "leaf_parameters": {
            "leaf_block": "chimera:high_poly_leaves",
            "fill_radius": {"range_min": 4, "range_max": 6}
        }
    }
}
write_json(f"{P_BP_FEAT}/chimera_oak_feature.json", feature)

# The Tree Rule (Placement)
rule = {
    "format_version": "1.13.0",
    "minecraft:feature_rules": {
        "description": {"identifier": "chimera:oak_feature_rule", "places_feature": "chimera:oak_feature"},
        "conditions": {
            "placement_pass": "surface_pass",
            "minecraft:biome_filter": [{"test": "has_biome_tag", "operator": "==", "value": "overworld"}]
        },
        "distribution": {
            "iterations": 20, # How many attempts to spawn per chunk
            "x": {"distribution": "uniform", "extent": [0, 16]},
            "y": "query.heightmap(variable.worldx, variable.worldz)",
            "z": {"distribution": "uniform", "extent": [0, 16]}
        }
    }
}
write_json(f"{P_BP_RULES}/chimera_oak_feature_rule.json", rule)

print("Files generated successfully!")
