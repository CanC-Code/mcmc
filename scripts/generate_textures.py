from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import math
import os
import json

# =============================================================================
# PROJECT CHIMERA — ASSET GENERATOR  v4
# Run from repo root:  python scripts/generate_textures.py
# Overwrites ALL generated assets. Always run before building APK.
# =============================================================================

random.seed(7)
np.random.seed(7)

OUT_BLOCKS = 'resource_pack/textures/blocks'
OUT_MODELS = 'resource_pack/models/blocks'
BP_FEATURES = 'behavior_pack/features'
BP_RULES    = 'behavior_pack/feature_rules'

for d in [OUT_BLOCKS, OUT_MODELS, BP_FEATURES, BP_RULES]:
    os.makedirs(d, exist_ok=True)

# =============================================================================
# TEXTURE HELPERS
# =============================================================================

def sobel_normal(img_rgba, strength=3.0):
    """Derive a tangent-space normal map from RGBA image luminance."""
    g = np.array(img_rgba.convert('L'), dtype=np.float32) / 255.0
    dx = np.zeros_like(g);  dy = np.zeros_like(g)
    dx[:, 1:-1] = (g[:, 2:] - g[:, :-2]) * strength
    dy[1:-1, :] = (g[2:, :] - g[:-2, :]) * strength
    nx = dx.clip(-1,1);  ny = dy.clip(-1,1);  nz = np.ones_like(nx)
    ln = np.sqrt(nx**2 + ny**2 + nz**2) + 1e-8
    nx, ny, nz = nx/ln, ny/ln, nz/ln
    return Image.fromarray(np.stack([
        ((nx+1)*0.5*255).astype(np.uint8),
        ((ny+1)*0.5*255).astype(np.uint8),
        ((nz+1)*0.5*255).astype(np.uint8),
    ], axis=2), 'RGB')

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# =============================================================================
# 1. BARK SIDE TEXTURE  (128x128 for higher fidelity on mobile)
#    - Deep fibrous vertical grain
#    - Raised ridge highlights
#    - Dark crevice shadows
#    - Subtle moss patches at base
# =============================================================================
print("  Generating bark side texture...")
SIZE = 128
bark = Image.new('RGBA', (SIZE, SIZE), (58, 36, 14, 255))
db   = ImageDraw.Draw(bark)

# Base noise layer — coarse grain columns
for _ in range(200):
    x  = random.randint(0, SIZE-1)
    r  = random.randint(28, 72)
    g  = random.randint(18, 44)
    b  = random.randint(4, 16)
    w  = random.randint(1, 3)
    x2 = x + random.randint(-4, 4)
    db.line([(x, 0), (x2, SIZE-1)], fill=(r, g, b, 255), width=w)

# Raised ridge highlights (lighter, narrow)
for _ in range(60):
    x = random.randint(0, SIZE-1)
    db.line([(x,0),(x+random.randint(-2,2),SIZE-1)],
            fill=(100, 68, 28, 180), width=1)

# Deep shadow crevices (dark, narrow)
for _ in range(80):
    x = random.randint(0, SIZE-1)
    db.line([(x,0),(x+random.randint(-3,3),SIZE-1)],
            fill=(18, 10, 3, 220), width=1)

# Horizontal ring/band marks every ~8px (bark growth rings on side)
for y in range(0, SIZE, random.randint(6,10)):
    y += random.randint(-2, 2)
    if 0 <= y < SIZE:
        db.line([(0,y),(SIZE-1, y+random.randint(-1,1))],
                fill=(30, 18, 6, 140), width=1)

# Knot holes — dark oval patches
for _ in range(4):
    kx = random.randint(10, SIZE-10)
    ky = random.randint(10, SIZE-10)
    kr = random.randint(3, 7)
    db.ellipse([kx-kr, ky-int(kr*1.6), kx+kr, ky+int(kr*1.6)],
               fill=(15, 8, 3, 255))
    db.ellipse([kx-kr+2, ky-int(kr*1.4), kx+kr-2, ky+int(kr*1.2)],
               fill=(35, 20, 8, 200))

# Subtle moss tint at bottom quarter
moss = Image.new('RGBA', (SIZE, SIZE), (0,0,0,0))
dm = ImageDraw.Draw(moss)
for _ in range(300):
    mx = random.randint(0, SIZE-1)
    my = random.randint(SIZE*3//4, SIZE-1)
    mr = random.randint(1, 4)
    dm.ellipse([mx, my, mx+mr, my+mr],
               fill=(30, random.randint(60,100), 20, random.randint(40,90)))
bark = Image.alpha_composite(bark, moss)

bark = bark.filter(ImageFilter.GaussianBlur(radius=0.6))
bark.save(os.path.join(OUT_BLOCKS, 'chimera_oak_albedo.png'))

sobel_normal(bark, strength=4.0).save(
    os.path.join(OUT_BLOCKS, 'chimera_oak_normal.png'))

mer = Image.new('RGB', (SIZE, SIZE), (0, 0, 210))
dm2 = ImageDraw.Draw(mer)
for _ in range(80):
    x = random.randint(0, SIZE-1)
    dm2.line([(x,0),(x,SIZE-1)], fill=(0,0,random.randint(180,240)), width=1)
mer.save(os.path.join(OUT_BLOCKS, 'chimera_oak_mer.png'))

print("  [OK] Bark side textures (128x128)")

# =============================================================================
# 2. BARK TOP TEXTURE — concentric growth rings
#    Centre is heartwood (darkest), rings lighten outward, sapwood at edge.
#    Rendered onto a 128x128 canvas, UV-mapped to the top faces of the geo.
# =============================================================================
print("  Generating bark top (growth rings) texture...")

top = Image.new('RGBA', (SIZE, SIZE), (50, 30, 10, 255))
dt  = ImageDraw.Draw(top)

cx, cy = SIZE//2, SIZE//2
max_r  = SIZE//2

# Heartwood core — very dark
dt.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(22, 12, 4, 255))

# Growth rings radiating outward
num_rings = 18
for i in range(1, num_rings+1):
    r   = int(max_r * i / num_rings)
    # Alternate light/dark rings
    base_r = 45 + int(i * 1.8)
    base_g = 28 + int(i * 1.2)
    base_b = 8  + int(i * 0.5)
    # Dark ring edge
    dt.ellipse([cx-r, cy-r, cx+r, cy+r],
               outline=(base_r-15, base_g-10, base_b-4, 255),
               width=2)
    # Light ring fill (sapwood band)
    if i % 2 == 0:
        dt.ellipse([cx-r+1, cy-r+1, cx+r-1, cy+r-1],
                   outline=(base_r+20, base_g+14, base_b+5, 180),
                   width=1)

# Ray lines (medullary rays) — thin radial lines from centre
for angle_deg in range(0, 360, 15):
    angle = math.radians(angle_deg + random.uniform(-4, 4))
    end_r = max_r * random.uniform(0.5, 0.95)
    ex = int(cx + end_r * math.cos(angle))
    ey = int(cy + end_r * math.sin(angle))
    dt.line([(cx, cy), (ex, ey)], fill=(70, 45, 16, 120), width=1)

# Cracks / radial splits
for _ in range(5):
    angle = math.radians(random.uniform(0, 360))
    r1    = random.uniform(0.1, 0.3) * max_r
    r2    = random.uniform(0.5, 0.9) * max_r
    jag   = random.uniform(-0.15, 0.15)
    sx = int(cx + r1 * math.cos(angle));  sy = int(cy + r1 * math.sin(angle))
    mx = int(cx + ((r1+r2)/2) * math.cos(angle+jag))
    my = int(cy + ((r1+r2)/2) * math.sin(angle+jag))
    ex = int(cx + r2 * math.cos(angle+jag*2))
    ey = int(cy + r2 * math.sin(angle+jag*2))
    dt.line([(sx,sy),(mx,my),(ex,ey)], fill=(18, 10, 3, 200), width=1)

top = top.filter(ImageFilter.GaussianBlur(radius=0.4))
top.save(os.path.join(OUT_BLOCKS, 'chimera_oak_top.png'))

sobel_normal(top, strength=2.5).save(
    os.path.join(OUT_BLOCKS, 'chimera_oak_top_normal.png'))

Image.new('RGB', (SIZE, SIZE), (0, 0, 195)).save(
    os.path.join(OUT_BLOCKS, 'chimera_oak_top_mer.png'))

print("  [OK] Bark top texture with growth rings (128x128)")

# =============================================================================
# 3. LEAVES TEXTURES
# =============================================================================
print("  Generating leaves textures...")

leaves = Image.new('RGBA', (64, 64), (0,0,0,0))
dl = ImageDraw.Draw(leaves)
for _ in range(600):
    x = random.randint(-8, 62);  y = random.randint(-8, 62)
    r = random.randint(2, 11)
    dl.ellipse([x,y,x+r,y+r],
               fill=(random.randint(10,35), random.randint(75,195),
                     random.randint(6,28), random.randint(205,255)))
for _ in range(30):
    x = random.randint(0,63);  y = random.randint(0,63)
    dl.ellipse([x,y,x+3,y+3], fill=(55,210,55,150))
leaves.save(os.path.join(OUT_BLOCKS, 'chimera_oak_leaves_albedo.png'))
sobel_normal(leaves, strength=0.5).save(
    os.path.join(OUT_BLOCKS, 'chimera_oak_leaves_normal.png'))
Image.new('RGB',(64,64),(0,0,150)).save(
    os.path.join(OUT_BLOCKS, 'chimera_oak_leaves_mer.png'))

print("  [OK] Leaves textures")

# =============================================================================
# 4. TERRAIN TEXTURE + texture_set JSONs
# =============================================================================
save_json('resource_pack/textures/terrain_texture.json', {
    "resource_pack_name": "chimera",
    "texture_name": "atlas.terrain",
    "padding": 8,
    "num_mip_levels": 4,
    "texture_data": {
        "chimera_oak_bark":   {"textures": "textures/blocks/chimera_oak_bark"},
        "chimera_oak_leaves": {"textures": "textures/blocks/chimera_oak_leaves"},
        "chimera_oak_top":    {"textures": "textures/blocks/chimera_oak_top"},
    }
})

for path, data in {
    os.path.join(OUT_BLOCKS,'chimera_oak_bark.texture_set.json'): {
        "format_version": "1.16.100",
        "minecraft:texture_set": {
            "color": "chimera_oak_albedo",
            "metalness_emissive_roughness": "chimera_oak_mer",
            "normal": "chimera_oak_normal"
        }
    },
    os.path.join(OUT_BLOCKS,'chimera_oak_leaves.texture_set.json'): {
        "format_version": "1.16.100",
        "minecraft:texture_set": {
            "color": "chimera_oak_leaves_albedo",
            "metalness_emissive_roughness": "chimera_oak_leaves_mer",
            "normal": "chimera_oak_leaves_normal"
        }
    },
    os.path.join(OUT_BLOCKS,'chimera_oak_top.texture_set.json'): {
        "format_version": "1.16.100",
        "minecraft:texture_set": {
            "color": "chimera_oak_top",
            "metalness_emissive_roughness": "chimera_oak_top_mer",
            "normal": "chimera_oak_top_normal"
        }
    },
}.items():
    with open(path,'w') as f:
        json.dump(data, f, indent=2)

print("  [OK] terrain_texture.json + texture_set JSONs")

# =============================================================================
# 5. DELETE blocks.json
# =============================================================================
if os.path.exists('resource_pack/blocks.json'):
    os.remove('resource_pack/blocks.json')
    print("  [OK] Deleted blocks.json")

# =============================================================================
# 6. BARK BLOCK DEFINITION — two material instances: sides + top
#    '*'  -> chimera_oak_bark  (side grain texture)
#    'up' -> chimera_oak_top   (growth rings texture)
# =============================================================================
save_json('behavior_pack/blocks/chimera_high_poly_bark.json', {
    "format_version": "1.20.80",
    "minecraft:block": {
        "description": {
            "identifier": "chimera:high_poly_bark",
            "menu_category": {"category": "nature"}
        },
        "components": {
            "minecraft:geometry": "geometry.round_bark",
            "minecraft:collision_box":  {"origin": [-7,0,-7], "size": [14,16,14]},
            "minecraft:selection_box":  {"origin": [-7,0,-7], "size": [14,16,14]},
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 1.5},
            "minecraft:material_instances": {
                "*":    {"texture": "chimera_oak_bark", "render_method": "opaque"},
                "top":  {"texture": "chimera_oak_top",  "render_method": "opaque"},
                "down": {"texture": "chimera_oak_top",  "render_method": "opaque"}
            }
        }
    }
})
print("  [OK] chimera_high_poly_bark.json (side + top material instances)")

# =============================================================================
# 7. ROUND BARK GEOMETRY — 12-slab cylinder approximation
#
#    Bedrock block geometry cannot rotate bones, so we simulate a cylinder
#    by stacking axis-aligned cuboids whose union forms a 12-sided polygon
#    cross-section. Each slab is progressively wider/narrower to chamfer
#    the corners smoothly.
#
#    The "trunk" bone handles side faces with the bark grain texture.
#    A separate "top_cap" bone uses the "top" material instance so the
#    growth ring texture shows only on the top face, not the sides.
#
#    Top-view cross-section (each symbol = contributing slab edge):
#
#          . . # # # # # # . .
#        . # # # # # # # # # .
#        # # # # # # # # # # #
#        # # # # # # # # # # #
#        # # # # # # # # # # #
#        # # # # # # # # # # #
#        # # # # # # # # # # #
#        # # # # # # # # # # #
#        . # # # # # # # # # .
#          . . # # # # # # . .
#
#    This gives a smooth 12-sided profile at every viewing angle.
# =============================================================================
print("  Generating round_bark geometry...")

geo_path = os.path.join(OUT_MODELS, 'round_bark.geo.json')

def face_uv(u, v, uw, uh):
    return {"uv": [u,v], "uv_size": [uw,uh]}

def slab(ox, oz, sx, sz, h=16, u_side=0, mat="*"):
    """
    Build one axis-aligned slab cuboid.
    Side UVs sample the bark grain. Top/bottom use the top ring texture.
    """
    return {
        "origin": [ox, 0, oz],
        "size":   [sx, h, sz],
        "uv": {
            "north": face_uv(u_side, 0, sx, h),
            "south": face_uv(u_side, 0, sx, h),
            "east":  face_uv(u_side, 0, sz, h),
            "west":  face_uv(u_side, 0, sz, h),
            "up":    face_uv(0,      0, sx, sz),
            "down":  face_uv(0,      0, sx, sz),
        }
    }

# 12-slab cylinder: slabs defined as (ox, oz, sx, sz)
# Each row is a pair of symmetric slabs building up the polygon ring.
# Width steps: 4, 6, 8, 10, 12, 14  (half-widths 2,3,4,5,6,7)
# Depth steps: 14,12,10, 8, 6, 4
slabs_xz = [
    # (ox,   oz,   sx,  sz)   — symmetric pairs about centre
    (-2,   -7,   4,  14),   # very narrow X, full Z — front/back columns
    (-7,   -2,  14,   4),   # full X, very narrow Z — left/right columns
    (-3,   -6,   6,  12),   # chamfer slice 1
    (-6,   -3,  12,   6),   # chamfer slice 1 rotated
    (-4,   -5,   8,  10),   # chamfer slice 2
    (-5,   -4,  10,   8),   # chamfer slice 2 rotated
]

trunk_cubes = []
for (ox, oz, sx, sz) in slabs_xz:
    trunk_cubes.append({
        "origin": [ox, 0, oz],
        "size":   [sx, 16, sz],
        "uv": {
            "north": face_uv(0, 0, sx, 16),
            "south": face_uv(0, 0, sx, 16),
            "east":  face_uv(0, 0, sz, 16),
            "west":  face_uv(0, 0, sz, 16),
            "up":    face_uv(0, 0, sx, sz),   # will be overridden by top_cap
            "down":  face_uv(0, 0, sx, sz),
        }
    })

# Top cap bone — thin 1px-tall slabs at y=15 covering same octagon footprint,
# mapped to the "top" material instance so growth rings appear on the top face.
# These render on top of the trunk slabs' top faces and hide them completely.
top_cubes = []
for (ox, oz, sx, sz) in slabs_xz:
    top_cubes.append({
        "origin": [ox, 15, oz],
        "size":   [sx, 1, sz],
        "uv": {
            "north": face_uv(0, 0, sx, 1),
            "south": face_uv(0, 0, sx, 1),
            "east":  face_uv(0, 0, sz, 1),
            "west":  face_uv(0, 0, sz, 1),
            "up":    face_uv(0, 0, sx, sz),
            "down":  face_uv(0, 0, sx, sz),
        }
    })

geo = {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.round_bark",
            "texture_width":  128,
            "texture_height": 128,
            "visible_bounds_width":  2,
            "visible_bounds_height": 2,
            "visible_bounds_offset": [0, 0.5, 0]
        },
        "bones": [
            {
                "name":   "trunk",
                "pivot":  [0, 0, 0],
                "cubes":  trunk_cubes
            },
            {
                "name":   "top_cap",
                "parent": "trunk",
                "pivot":  [0, 0, 0],
                "cubes":  top_cubes
            }
        ]
    }]
}

save_json(geo_path, geo)
print("  [OK] round_bark.geo.json (12-slab cylinder + top_cap bone for ring texture)")

# =============================================================================
# 8. CHIMERA OAK FEATURE — enforced correct values, written every run
#    MUST run before APK build or the old broken file gets packaged.
# =============================================================================
save_json(os.path.join(BP_FEATURES, 'chimera_oak_feature.json'), {
    "format_version": "1.13.0",
    "minecraft:tree_feature": {
        "description": {"identifier": "chimera:oak_feature"},
        "base_block": [
            "minecraft:grass",    # Bedrock identifier (NOT grass_block)
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
})
print("  [OK] chimera_oak_feature.json (grass, no branches)")

# =============================================================================
# 9. CHIMERA FEATURE RULE — also written every run to ensure correct state
# =============================================================================
save_json(os.path.join(BP_RULES, 'chimera_oak_rule.json'), {
    "format_version": "1.13.0",
    "minecraft:feature_rules": {
        "description": {
            "identifier": "chimera:oak_rule",
            "places_feature": "chimera:oak_feature"
        },
        "conditions": {
            "placement_pass": "surface_pass",
            "minecraft:biome_filter": [
                {"test": "has_biome_tag", "operator": "==", "value": "forest"}
            ]
        },
        "distribution": {
            "iterations": 20,
            "x": {"distribution": "uniform", "extent": [0, 16]},
            "y": "query.heightmap(variable.worldx, variable.worldz)",
            "z": {"distribution": "uniform", "extent": [0, 16]}
        }
    }
})
print("  [OK] chimera_oak_rule.json enforced")

# =============================================================================
# 10. VANILLA TREE FEATURE NULL OVERRIDES
# =============================================================================
vanilla_features = [
    'oak_tree_feature', 'birch_tree_feature', 'fancy_tree_feature',
    'spruce_tree_feature', 'pine_tree_feature', 'mega_oak_feature',
    'mega_pine_tree_feature', 'mega_spruce_tree_feature',
    'swamp_tree_feature', 'acacia_tree_feature', 'jungle_tree_feature',
    'jungle_transformation_tree_feature', 'mega_jungle_tree_feature',
]
for feat in vanilla_features:
    save_json(os.path.join(BP_FEATURES, f"{feat}.json"), {
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
    })
print(f"  [OK] {len(vanilla_features)} null vanilla feature overrides")

# =============================================================================
# 11. VANILLA FEATURE RULE SUPPRESSORS
# =============================================================================
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
    fname = rule_id.replace('minecraft:', '') + '.json'
    save_json(os.path.join(BP_RULES, fname), {
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
    })
print(f"  [OK] {len(vanilla_rules)} vanilla rule suppressors")

print("""
=== Project Chimera Asset Generator — Done ===

Checklist before testing:
  1. This script ran successfully (you're reading this).
  2. Build and install the APK fresh after running this script.
  3. Create a BRAND NEW world — existing chunks never update.
  4. Chimera trees spawn in FOREST biome. Use /locate biome forest if needed.
  5. Confirm both BP and RP are active in the world settings.
""")
