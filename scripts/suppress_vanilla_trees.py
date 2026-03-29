import os
import json

print("Starting Vanilla Tree Suppression...")

P_BP_RULES = "behavior_pack/feature_rules"
os.makedirs(P_BP_RULES, exist_ok=True)

# Master list of all vanilla tree rules and their features
VANILLA_RULES = {
    "lush_caves_azalea_tree_feature_rule": "minecraft:azalea_tree_feature",
    "cherry_tree_feature_rule": "minecraft:cherry_tree_feature",
    "mangrove_tree_feature_rule": "minecraft:mangrove_tree_feature",
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
            "description": {
                "identifier": f"minecraft:{rule_id}",
                "places_feature": feature_id
            },
            "conditions": {
                "placement_pass": "surface_pass",
                "minecraft:biome_filter": [
                    {
                        "test": "has_biome_tag",
                        "operator": "==",
                        "value": "overworld"
                    }
                ]
            },
            "distribution": {
                "iterations": 0,
                "x": 0,
                "y": 0,
                "z": 0
            }
        }
    }
    with open(f"{P_BP_RULES}/{rule_id}.json", "w") as f:
        json.dump(rule_data, f, indent=4)

print(f"[OK] {len(VANILLA_RULES)} vanilla tree spawns successfully suppressed.")
