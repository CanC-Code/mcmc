from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import os
import json

# =============================================================================
# PROJECT CHIMERA - ASSET GENERATOR
# Run from the repo root: python scripts/generate_textures.py
# Overwrites all generated assets in-place. Safe to re-run at any time.
# =============================================================================

def build_assets():
    random.seed(42)
    np.random.seed(42)

    # =========================================================================
    # 1. BARK TEXTURES  (albedo + normal + MER)
    # =========================================================================
    out_dir = 'resource_pack/textures/blocks'
    os.makedirs(out_dir, exist_ok=True)

    bark_albedo = Image.new('RGBA', (64, 64), (72, 47, 22, 255))
    draw = ImageDraw.Draw(bark_albedo)
    for _ in range(90):
        x = random.randint(0, 63)
        draw.line(
            [(x, 0), (x + random.randint(-3, 3), 63)],
            fill=(random.randint(35,68), random.randint(22,42), random.randint(8,18), 255),
            width=random.randint(1, 2)
        )
    for _ in range(18):
        y = random.randint(2, 61)
        x0 = random.randint(0, 28)
        draw.line(
            [(x0, y), (x0 + random.randint(6,22), y + random.randint(-1,1))],
            fill=(38, 22, 8, 255), width=1
        )
    for _ in range(12):
        x = random.randint(0, 63)
        draw.line([(x, 0), (x, 63)], fill=(90, 60, 28, 120), width=1)
    bark_albedo = bark_albedo.filter(ImageFilter.GaussianBlur(radius=0.5))
    bark_albedo.save(os.path.join(out_dir, 'chimera_oak_albedo.png'))

    bg = np.array(bark_albedo.convert('L'), dtype=np.float32) / 255.0
    dx = np.zeros_like(bg);  dy = np.zeros_like(bg)
    dx[:, 1:-1] = (bg[:, 2:] - bg[:, :-2]) * 2.5
    dy[1:-1, :] = (bg[2:, :] - bg[:-2, :]) * 2.5
    nx = dx.clip(-1,1);  ny = dy.clip(-1,1);  nz = np.ones_like(nx)
    ln = np.sqrt(nx**2 + ny**2 + nz**2) + 1e-8
    nx, ny, nz = nx/ln, ny/ln, nz/ln
    Image.fromarray(np.stack([
        ((nx+1)*0.5*255).astype(np.uint8),
        ((ny+1)*0.5*255).astype(np.uint8),
        ((nz+1)*0.5*255).astype(np.uint8)
    ], axis=2), 'RGB').save(os.path.join(out_dir, 'chimera_oak_normal.png'))

    mer_bark = Image.new('RGB', (64, 64), (0, 0, 200))
    dm = ImageDraw.Draw(mer_bark)
    for _ in range(50):
        x = random.randint(0, 63)
        dm.line([(x,0),(x,63)], fill=(0, 0, random.randint(175,225)), width=1)
    mer_bark.save(os.path.join(out_dir, 'chimera_oak_mer.png'))

    print("  [OK] Bark textures written")

    # =========================================================================
    # 2. LEAVES TEXTURES  (albedo + normal + MER)
    # =========================================================================
    leaves_albedo = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    dl = ImageDraw.Draw(leaves_albedo)
    for _ in range(500):
        x = random.randint(-6, 62);  y = random.randint(-6, 62)
        r = random.randint(3, 10)
        dl.ellipse([x, y, x+r, y+r],
                   fill=(random.randint(12,38), random.randint(80,185),
                         random.randint(8,28),  random.randint(210,255)))
    for _ in range(20):
        x = random.randint(0,63);  y = random.randint(0,63)
        dl.ellipse([x,y,x+2,y+2], fill=(60,200,60,160))
    leaves_albedo.save(os.path.join(out_dir, 'chimera_oak_leaves_albedo.png'))

    lg = np.array(leaves_albedo.convert('L'), dtype=np.float32) / 255.0
    dx_l = np.zeros_like(lg);  dy_l = np.zeros_like(lg)
    dx_l[:, 1:-1] = (lg[:, 2:] - lg[:, :-2]) * 0.4
    dy_l[1:-1, :] = (lg[2:, :] - lg[:-2, :]) * 0.4
    nz_l = np.ones_like(dx_l)
    ll = np.sqrt(dx_l**2 + dy_l**2 + nz_l**2) + 1e-8
    dx_l, dy_l, nz_l = dx_l/ll, dy_l/ll, nz_l/ll
    Image.fromarray(np.stack([
        ((dx_l+1)*0.5*255).astype(np.uint8),
        ((dy_l+1)*0.5*255).astype(np.uint8),
        ((nz_l+1)*0.5*255).astype(np.uint8)
    ], axis=2), 'RGB').save(os.path.join(out_dir, 'chimera_oak_leaves_normal.png'))
    Image.new('RGB', (64,64), (0,0,155)).save(
        os.path.join(out_dir, 'chimera_oak_leaves_mer.png'))

    print("  [OK] Leaves textures written")

    # =========================================================================
    # 3. texture_set JSONs
    # =========================================================================
    for path, data in {
        os.path.join(out_dir, 'chimera_oak_bark.texture_set.json'): {
            "format_version": "1.16.100",
            "minecraft:texture_set": {
                "color": "chimera_oak_albedo",
                "metalness_emissive_roughness": "chimera_oak_mer",
                "normal": "chimera_oak_normal"
            }
        },
        os.path.join(out_dir, 'chimera_oak_leaves.texture_set.json'): {
            "format_version": "1.16.100",
            "minecraft:texture_set": {
                "color": "chimera_oak_leaves_albedo",
                "metalness_emissive_roughness": "chimera_oak_leaves_mer",
                "normal": "chimera_oak_leaves_normal"
            }
        }
    }.items():
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    print("  [OK] texture_set JSONs written")

    # =========================================================================
    # 4. terrain_texture.json
    # =========================================================================
    terrain_path = 'resource_pack/textures/terrain_texture.json'
    os.makedirs(os.path.dirname(terrain_path), exist_ok=True)
    with open(terrain_path, 'w') as f:
        json.dump({
            "resource_pack_name": "chimera",
            "texture_name": "atlas.terrain",
            "padding": 8,
            "num_mip_levels": 4,
            "texture_data": {
                "chimera_oak_bark":   {"textures": "textures/blocks/chimera_oak_bark"},
                "chimera_oak_leaves": {"textures": "textures/blocks/chimera_oak_leaves"}
            }
        }, f, indent=2)
    print("  [OK] terrain_texture.json written")

    # =========================================================================
    # 5. DELETE blocks.json
    # =========================================================================
    blocks_json = 'resource_pack/blocks.json'
    if os.path.exists(blocks_json):
        os.remove(blocks_json)
        print("  [OK] Deleted resource_pack/blocks.json")

    # =========================================================================
    # 6. ROUND BARK GEOMETRY
    #
    #    A true 8-sided cylinder approximation using ONLY the natural top faces
    #    of each slab. NO separate top-cap box — that was the square lid bug.
    #
    #    Cross-section layout (top view, each letter = one slab):
    #
    #         . X X X X X .
    #         D X X X X X D      X  = core 8x8 square (all slabs overlap here)
    #         X X X X X X X      D  = diagonal 45° chamfer slabs (NW-SE, NE-SW)
    #         X X X X X X X      |  = X-axis wide slab tips
    #         D X X X X X D      —  = Z-axis wide slab tips
    #         . X X X X X .
    #
    #    Five cuboids, NO top cap disc. The tops of the 5 slabs together
    #    form an octagonal face — naturally round at the top.
    # =========================================================================
    geo_path = 'resource_pack/models/blocks/round_bark.geo.json'
    os.makedirs(os.path.dirname(geo_path), exist_ok=True)

    def uv(u, v, uw, uh):
        return {"uv": [u, v], "uv_size": [uw, uh]}

    # Helper: build a full-face cube dict
    def cube(ox, oy, oz, sx, sy, sz, u_off=0):
        return {
            "origin": [ox, oy, oz],
            "size":   [sx, sy, sz],
            "uv": {
                "north": uv(u_off, 0, sx, sy),
                "south": uv(u_off, 0, sx, sy),
                "east":  uv(u_off, 0, sz, sy),
                "west":  uv(u_off, 0, sz, sy),
                "up":    uv(u_off, 0, sx, sz),
                "down":  uv(u_off, 0, sx, sz),
            }
        }

    geo = {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": "geometry.round_bark",
                "texture_width": 64,
                "texture_height": 64,
                "visible_bounds_width": 2,
                "visible_bounds_height": 2,
                "visible_bounds_offset": [0, 0.5, 0]
            },
            "bones": [{
                "name": "trunk",
                "pivot": [0, 0, 0],
                "cubes": [
                    # 1. Core square pillar  (8 x 16 x 8)
                    cube(-4, 0, -4,  8, 16,  8, u_off=0),
                    # 2. Wide slab X-axis    (14 x 16 x 4)  — left/right wings
                    cube(-7, 0, -2, 14, 16,  4, u_off=8),
                    # 3. Wide slab Z-axis    (4 x 16 x 14)  — front/back wings
                    cube(-2, 0, -7,  4, 16, 14, u_off=8),
                    # 4. Diagonal NW-SE      (12 x 16 x 10)
                    cube(-6, 0, -5, 12, 16, 10, u_off=0),
                    # 5. Diagonal NE-SW      (10 x 16 x 12)
                    cube(-5, 0, -6, 10, 16, 12, u_off=0),
                ]
            }]
        }]
    }

    with open(geo_path, 'w') as f:
        json.dump(geo, f, indent=4)
    print("  [OK] round_bark.geo.json written (5-slab cylinder, no square lid)")

    # =========================================================================
    # 7. CHIMERA OAK FEATURE  — written fresh every run to override old file
    #
    #    ROOT CAUSES OF FAILED NATURAL SPAWNING (now fixed):
    #    a) 'minecraft:grass_block' is a Java identifier. Bedrock = 'minecraft:grass'
    #    b) 'branches' is a Java-only key. Bedrock silently rejects the whole file.
    # =========================================================================
    oak_feature = {
        "format_version": "1.13.0",
        "minecraft:tree_feature": {
            "description": {"identifier": "chimera:oak_feature"},
            "base_block": [
                "minecraft:grass",
                "minecraft:dirt",
                "minecraft:podzol"
            ],
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
    feat_path = 'behavior_pack/features/chimera_oak_feature.json'
    os.makedirs(os.path.dirname(feat_path), exist_ok=True)
    with open(feat_path, 'w') as f:
        json.dump(oak_feature, f, indent=4)
    print("  [OK] chimera_oak_feature.json written (grass, no branches)")

    # =========================================================================
    # 8. VANILLA TREE FEATURE NULL OVERRIDES
    #    base_block=end_stone -> never matches;  trunk/leaf=air -> nothing placed
    # =========================================================================
    features_dir = 'behavior_pack/features'
    os.makedirs(features_dir, exist_ok=True)

    vanilla_features = [
        'oak_tree_feature', 'birch_tree_feature', 'fancy_tree_feature',
        'spruce_tree_feature', 'pine_tree_feature', 'mega_oak_feature',
        'mega_pine_tree_feature', 'mega_spruce_tree_feature',
        'swamp_tree_feature', 'acacia_tree_feature', 'jungle_tree_feature',
        'jungle_transformation_tree_feature', 'mega_jungle_tree_feature',
    ]
    for feat in vanilla_features:
        with open(os.path.join(features_dir, f"{feat}.json"), 'w') as f:
            json.dump({
                "format_version": "1.13.0",
                "minecraft:tree_feature": {
                    "description": {"identifier": f"minecraft:{feat}"},
                    "base_block": ["minecraft:end_stone"],
                    "trunk": {
                        "trunk_block": "minecraft:air",
                        "trunk_height": {"range_min": 1, "range_max": 1}
                    },
                    "leaf_parameters": {
                        "leaf_block": "minecraft:air",
                        "fill_radius": {"range_min": 0, "range_max": 0}
                    }
                }
            }, f, indent=4)
    print(f"  [OK] {len(vanilla_features)} null vanilla feature overrides written")

    # =========================================================================
    # 9. VANILLA FEATURE RULE SUPPRESSORS  (iterations=0, covers all biomes)
    # =========================================================================
    rules_dir = 'behavior_pack/feature_rules'
    os.makedirs(rules_dir, exist_ok=True)

    vanilla_rules = [
        ('minecraft:forest_oak_feature_rule',             'minecraft:oak_tree_feature'),
        ('minecraft:forest_birch_feature_rule',           'minecraft:birch_tree_feature'),
        ('minecraft:overworld_surface_oak_feature_rule',  'minecraft:oak_tree_feature'),
        ('minecraft:overworld_surface_birch_feature_rule','minecraft:birch_tree_feature'),
        ('minecraft:plains_oak_feature_rule',             'minecraft:oak_tree_feature'),
        ('minecraft:taiga_spruce_feature_rule',           'minecraft:spruce_tree_feature'),
        ('minecraft:taiga_pine_feature_rule',             'minecraft:pine_tree_feature'),
        ('minecraft:mega_taiga_spruce_feature_rule',      'minecraft:mega_spruce_tree_feature'),
        ('minecraft:mega_taiga_pine_feature_rule',        'minecraft:mega_pine_tree_feature'),
        ('minecraft:swamp_tree_feature_rule',             'minecraft:swamp_tree_feature'),
        ('minecraft:jungle_tree_feature_rule',            'minecraft:jungle_tree_feature'),
        ('minecraft:mega_jungle_tree_feature_rule',       'minecraft:mega_jungle_tree_feature'),
        ('minecraft:savanna_acacia_feature_rule',         'minecraft:acacia_tree_feature'),
    ]
    for rule_id, places in vanilla_rules:
        filename = rule_id.replace('minecraft:', '') + '.json'
        with open(os.path.join(rules_dir, filename), 'w') as f:
            json.dump({
                "format_version": "1.13.0",
                "minecraft:feature_rules": {
                    "description": {
                        "identifier": rule_id,
                        "places_feature": places
                    },
                    "conditions": {
                        "placement_pass": "surface_pass",
                        "minecraft:biome_filter": [
                            {"test": "has_biome_tag", "operator": "==", "value": "overworld"}
                        ]
                    },
                    "distribution": {"iterations": 0, "x": 0, "y": 0, "z": 0}
                }
            }, f, indent=4)
    print(f"  [OK] {len(vanilla_rules)} vanilla feature rule suppressors written")


if __name__ == "__main__":
    print("=== Project Chimera Asset Generator ===\n")
    build_assets()
    print("""
=== Done ===
IMPORTANT — natural spawning checklist:
  1. Run this script BEFORE building the APK (it overwrites chimera_oak_feature.json)
  2. Confirm your manifest.json BP dependency UUID matches the RP header UUID
  3. Test in a BRAND NEW world — existing chunks never regenerate
  4. The chimera rule targets biome tag 'forest'. Test in a forest biome.
""")
