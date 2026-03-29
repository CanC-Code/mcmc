from PIL import Image, ImageDraw
import random
import os
import json

def build_assets():
    # 1. Generate Mobile-Safe 64x64 Textures
    out_dir = 'resource_pack/textures/blocks'
    os.makedirs(out_dir, exist_ok=True)

    bark = Image.new('RGBA', (64, 64), (60, 40, 20, 255))
    draw_bark = ImageDraw.Draw(bark)
    for _ in range(120):
        x = random.randint(0, 64)
        shade = random.randint(20, 45)
        draw_bark.line([(x, 0), (x, 64)], fill=(shade, shade-10, 10, 255), width=random.randint(1, 3))
    bark.save(os.path.join(out_dir, 'chimera_oak_bark.png'))

    leaves = Image.new('RGBA', (64, 64), (0, 0, 0, 0)) 
    draw_leaves = ImageDraw.Draw(leaves)
    for _ in range(350):
        x, y = random.randint(-5, 64), random.randint(-5, 64)
        r = random.randint(3, 8)
        green = random.randint(100, 180)
        draw_leaves.ellipse([x, y, x+r, y+r], fill=(20, green, 30, 230))
    leaves.save(os.path.join(out_dir, 'chimera_oak_leaves.png'))

    # 2. CRITICAL FIX: Eradicate blocks.json to prevent Resource Pack Crash
    blocks_json_path = 'resource_pack/blocks.json'
    if os.path.exists(blocks_json_path):
        os.remove(blocks_json_path)

    # 3. CRITICAL FIX: Schema-Perfect Vanilla Erasers
    features_dir = 'behavior_pack/features'
    os.makedirs(features_dir, exist_ok=True)
    
    vanilla_features = [
        'oak_tree_feature', 'birch_tree_feature', 'fancy_tree_feature',
        'spruce_tree_feature', 'pine_tree_feature', 'mega_oak_feature',
        'mega_pine_tree_feature', 'mega_spruce_tree_feature',
        'swamp_tree_feature', 'acacia_tree_feature', 'jungle_tree_feature'
    ]
    
    for feat in vanilla_features:
        valid_null_data = {
          "format_version": "1.13.0",
          "minecraft:tree_feature": {
            "description": { "identifier": f"minecraft:{feat}" },
            "base_block": ["minecraft:end_stone"], 
            "trunk": { 
                "trunk_block": "minecraft:dirt", 
                "trunk_height": {"range_min": 1, "range_max": 1} 
            },
            "leaf_parameters": { 
                "leaf_block": "minecraft:dirt", 
                "fill_radius": {"range_min": 0, "range_max": 0} 
            }
          }
        }
        with open(os.path.join(features_dir, f"{feat}.json"), 'w') as f:
            json.dump(valid_null_data, f, indent=4)

if __name__ == "__main__":
    build_assets()
    print("Generated textures, deleted blocks.json, and wrote strict schema overrides.")
