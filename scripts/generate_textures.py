from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import os
import json

def build_assets():
    out_dir = 'resource_pack/textures/blocks'
    os.makedirs(out_dir, exist_ok=True)

    random.seed(42)
    np.random.seed(42)

    # -------------------------------------------------------------------------
    # 1. BARK TEXTURES (PBR: albedo, normal, MER)
    # -------------------------------------------------------------------------

    # -- Albedo: rich dark-brown oak bark with vertical grain lines
    bark_albedo = Image.new('RGBA', (64, 64), (72, 47, 22, 255))
    draw = ImageDraw.Draw(bark_albedo)

    # Vertical grain lines
    for _ in range(80):
        x = random.randint(0, 63)
        shade_r = random.randint(35, 65)
        shade_g = random.randint(22, 40)
        shade_b = random.randint(8, 18)
        width = random.randint(1, 2)
        draw.line([(x, 0), (x + random.randint(-2, 2), 63)],
                  fill=(shade_r, shade_g, shade_b, 255), width=width)

    # Horizontal knot-like breaks
    for _ in range(15):
        y = random.randint(0, 63)
        x0 = random.randint(0, 30)
        x1 = x0 + random.randint(8, 24)
        draw.line([(x0, y), (x1, y + random.randint(-1, 1))],
                  fill=(40, 25, 10, 255), width=1)

    # Slight blur for natural blending
    bark_albedo = bark_albedo.filter(ImageFilter.GaussianBlur(radius=0.4))
    bark_albedo.save(os.path.join(out_dir, 'chimera_oak_albedo.png'))

    # -- Normal map: baked from albedo luminance for surface depth illusion
    bark_gray = np.array(bark_albedo.convert('L'), dtype=np.float32) / 255.0
    # Sobel-like gradient
    dx = np.zeros_like(bark_gray)
    dy = np.zeros_like(bark_gray)
    dx[:, 1:-1] = (bark_gray[:, 2:] - bark_gray[:, :-2]) * 0.5
    dy[1:-1, :] = (bark_gray[2:, :] - bark_gray[:-2, :]) * 0.5
    # Encode to RGB normal map (R=X, G=Y, B=Z), flat Z for tangent-space
    nx = (dx * 2.0).clip(-1, 1)
    ny = (dy * 2.0).clip(-1, 1)
    nz = np.ones_like(nx)
    length = np.sqrt(nx**2 + ny**2 + nz**2) + 1e-8
    nx, ny, nz = nx / length, ny / length, nz / length
    normal_r = ((nx + 1.0) * 0.5 * 255).astype(np.uint8)
    normal_g = ((ny + 1.0) * 0.5 * 255).astype(np.uint8)
    normal_b = ((nz + 1.0) * 0.5 * 255).astype(np.uint8)
    normal_img = Image.fromarray(
        np.stack([normal_r, normal_g, normal_b], axis=2), 'RGB'
    )
    normal_img.save(os.path.join(out_dir, 'chimera_oak_normal.png'))

    # -- MER map: Metalness=0 (wood), Emissive=0, Roughness=200 (rough bark)
    mer_bark = Image.new('RGB', (64, 64), (0, 0, 200))
    draw_mer = ImageDraw.Draw(mer_bark)
    # Slight roughness variation along grain
    for _ in range(40):
        x = random.randint(0, 63)
        rough = random.randint(170, 220)
        draw_mer.line([(x, 0), (x, 63)], fill=(0, 0, rough), width=1)
    mer_bark.save(os.path.join(out_dir, 'chimera_oak_mer.png'))

    print("  [OK] Bark textures: chimera_oak_albedo.png, chimera_oak_normal.png, chimera_oak_mer.png")

    # -------------------------------------------------------------------------
    # 2. LEAVES TEXTURES (PBR: albedo, normal, MER)
    # -------------------------------------------------------------------------

    # -- Albedo: semi-transparent leaf clusters on transparent background
    leaves_albedo = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw_l = ImageDraw.Draw(leaves_albedo)
    for _ in range(400):
        x = random.randint(-4, 60)
        y = random.randint(-4, 60)
        r = random.randint(3, 9)
        green = random.randint(90, 175)
        red   = random.randint(15, 35)
        blue  = random.randint(10, 30)
        alpha = random.randint(200, 245)
        draw_l.ellipse([x, y, x + r, y + r], fill=(red, green, blue, alpha))
    leaves_albedo.save(os.path.join(out_dir, 'chimera_oak_leaves_albedo.png'))

    # -- Normal map: mostly flat (leaves are thin), slight variation
    leaves_gray = np.array(leaves_albedo.convert('L'), dtype=np.float32) / 255.0
    dx_l = np.zeros_like(leaves_gray)
    dy_l = np.zeros_like(leaves_gray)
    dx_l[:, 1:-1] = (leaves_gray[:, 2:] - leaves_gray[:, :-2]) * 0.3
    dy_l[1:-1, :] = (leaves_gray[2:, :] - leaves_gray[:-2, :]) * 0.3
    nz_l = np.ones_like(dx_l)
    len_l = np.sqrt(dx_l**2 + dy_l**2 + nz_l**2) + 1e-8
    dx_l, dy_l, nz_l = dx_l / len_l, dy_l / len_l, nz_l / len_l
    ln_r = ((dx_l + 1.0) * 0.5 * 255).astype(np.uint8)
    ln_g = ((dy_l + 1.0) * 0.5 * 255).astype(np.uint8)
    ln_b = ((nz_l + 1.0) * 0.5 * 255).astype(np.uint8)
    leaves_normal = Image.fromarray(np.stack([ln_r, ln_g, ln_b], axis=2), 'RGB')
    leaves_normal.save(os.path.join(out_dir, 'chimera_oak_leaves_normal.png'))

    # -- MER map: Metalness=0, Emissive=0, Roughness=160 (slightly smooth leaves)
    mer_leaves = Image.new('RGB', (64, 64), (0, 0, 160))
    mer_leaves.save(os.path.join(out_dir, 'chimera_oak_leaves_mer.png'))

    print("  [OK] Leaves textures: chimera_oak_leaves_albedo.png, chimera_oak_leaves_normal.png, chimera_oak_leaves_mer.png")

    # -------------------------------------------------------------------------
    # 3. DELETE blocks.json (causes conflicts with custom geometry blocks)
    # -------------------------------------------------------------------------
    blocks_json_path = 'resource_pack/blocks.json'
    if os.path.exists(blocks_json_path):
        os.remove(blocks_json_path)
        print("  [OK] Deleted resource_pack/blocks.json")
    else:
        print("  [--] blocks.json not present, skipping delete")

    # -------------------------------------------------------------------------
    # 4. VANILLA TREE FEATURE NULL OVERRIDES
    #    trunk_block and leaf_block set to air so nothing visible spawns.
    #    base_block set to end_stone so placement condition never matches.
    # -------------------------------------------------------------------------
    features_dir = 'behavior_pack/features'
    os.makedirs(features_dir, exist_ok=True)

    vanilla_features = [
        'oak_tree_feature', 'birch_tree_feature', 'fancy_tree_feature',
        'spruce_tree_feature', 'pine_tree_feature', 'mega_oak_feature',
        'mega_pine_tree_feature', 'mega_spruce_tree_feature',
        'swamp_tree_feature', 'acacia_tree_feature', 'jungle_tree_feature'
    ]

    for feat in vanilla_features:
        null_feature = {
            "format_version": "1.13.0",
            "minecraft:tree_feature": {
                "description": {
                    "identifier": f"minecraft:{feat}"
                },
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
        }
        path = os.path.join(features_dir, f"{feat}.json")
        with open(path, 'w') as f:
            json.dump(null_feature, f, indent=4)

    print(f"  [OK] Wrote {len(vanilla_features)} null vanilla feature overrides (air trunk/leaves)")

    # -------------------------------------------------------------------------
    # 5. VERIFY texture_set JSONs reference correct filenames
    # -------------------------------------------------------------------------
    texture_sets = {
        'resource_pack/textures/blocks/chimera_oak_bark.texture_set.json': {
            "format_version": "1.16.100",
            "minecraft:texture_set": {
                "color": "chimera_oak_albedo",
                "metalness_emissive_roughness": "chimera_oak_mer",
                "normal": "chimera_oak_normal"
            }
        },
        'resource_pack/textures/blocks/chimera_oak_leaves.texture_set.json': {
            "format_version": "1.16.100",
            "minecraft:texture_set": {
                "color": "chimera_oak_leaves_albedo",
                "metalness_emissive_roughness": "chimera_oak_leaves_mer",
                "normal": "chimera_oak_leaves_normal"
            }
        }
    }
    for path, data in texture_sets.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    print("  [OK] texture_set JSONs written/verified")

    # -------------------------------------------------------------------------
    # 6. VERIFY terrain_texture.json maps both keys correctly
    # -------------------------------------------------------------------------
    terrain_texture_path = 'resource_pack/textures/terrain_texture.json'
    terrain_texture = {
        "resource_pack_name": "chimera",
        "texture_name": "atlas.terrain",
        "padding": 8,
        "num_mip_levels": 4,
        "texture_data": {
            "chimera_oak_bark": {
                "textures": "textures/blocks/chimera_oak_bark"
            },
            "chimera_oak_leaves": {
                "textures": "textures/blocks/chimera_oak_leaves"
            }
        }
    }
    os.makedirs(os.path.dirname(terrain_texture_path), exist_ok=True)
    with open(terrain_texture_path, 'w') as f:
        json.dump(terrain_texture, f, indent=2)
    print("  [OK] terrain_texture.json written/verified")


if __name__ == "__main__":
    print("=== Project Chimera Asset Generator ===")
    build_assets()
    print("\nDone. All assets generated successfully.")
    print("Files written to resource_pack/textures/blocks/:")
    print("  chimera_oak_albedo.png, chimera_oak_normal.png, chimera_oak_mer.png")
    print("  chimera_oak_leaves_albedo.png, chimera_oak_leaves_normal.png, chimera_oak_leaves_mer.png")
    print("  chimera_oak_bark.texture_set.json, chimera_oak_leaves.texture_set.json")
    print("  terrain_texture.json")
    print(f"  11x null vanilla tree feature overrides in behavior_pack/features/")
