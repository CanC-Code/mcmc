"""
PROJECT CHIMERA — Asset Generator  v5
Run from repo root:  python scripts/generate_textures.py
Writes ALL generated assets (textures + every JSON) in-place.
Always run before building APK. Commit everything it outputs.
"""

from PIL import Image, ImageDraw, ImageFilter
import random, math, os, json
import numpy as np

random.seed(7)
np.random.seed(7)

# ── paths ────────────────────────────────────────────────────────────────────
P_TEXTURES   = "resource_pack/textures/blocks"
P_MODELS     = "resource_pack/models/blocks"
P_BP_BLOCKS  = "behavior_pack/blocks"
P_BP_FEAT    = "behavior_pack/features"
P_BP_RULES   = "behavior_pack/feature_rules"

for d in [P_TEXTURES, P_MODELS, P_BP_BLOCKS, P_BP_FEAT, P_BP_RULES,
          "resource_pack/textures", "resource_pack/texts"]:
    os.makedirs(d, exist_ok=True)

def jwrite(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def sobel_normal(img_rgba, strength=3.5):
    g = np.array(img_rgba.convert("L"), dtype=np.float32) / 255.0
    dx = np.zeros_like(g); dy = np.zeros_like(g)
    dx[:, 1:-1] = (g[:, 2:] - g[:, :-2]) * strength
    dy[1:-1, :] = (g[2:, :] - g[:-2, :]) * strength
    nx = dx.clip(-1,1); ny = dy.clip(-1,1); nz = np.ones_like(nx)
    ln = np.sqrt(nx**2 + ny**2 + nz**2) + 1e-8
    nx, ny, nz = nx/ln, ny/ln, nz/ln
    return Image.fromarray(np.stack([
        ((nx+1)*.5*255).astype(np.uint8),
        ((ny+1)*.5*255).astype(np.uint8),
        ((nz+1)*.5*255).astype(np.uint8),
    ], axis=2), "RGB")

def flat_mer(size=128, roughness=205):
    return Image.new("RGB", (size,size), (0, 0, roughness))

# ═════════════════════════════════════════════════════════════════════════════
# 1.  BARK SIDE TEXTURE  128×128
# ═════════════════════════════════════════════════════════════════════════════
print("Generating bark side texture…")
S = 128
bark = Image.new("RGBA", (S,S), (60, 38, 15, 255))
db   = ImageDraw.Draw(bark)

# Coarse grain columns
for _ in range(220):
    x  = random.randint(0, S-1)
    r  = random.randint(28, 75)
    g  = random.randint(17, 45)
    b  = random.randint(4,  17)
    w  = random.randint(1, 3)
    db.line([(x,0),(x+random.randint(-5,5), S-1)],
            fill=(r,g,b,255), width=w)

# Bright ridge highlights
for _ in range(70):
    x = random.randint(0, S-1)
    db.line([(x,0),(x+random.randint(-2,2),S-1)],
            fill=(105,70,30,160), width=1)

# Deep shadow crevices
for _ in range(100):
    x = random.randint(0, S-1)
    db.line([(x,0),(x+random.randint(-3,3),S-1)],
            fill=(16, 9, 2, 230), width=1)

# Horizontal growth band marks (subtle)
y = 0
while y < S:
    jitter = random.randint(-1,1)
    db.line([(0,y),(S-1,y+jitter)], fill=(28,16,5,100), width=1)
    y += random.randint(5, 11)

# Knot holes
for _ in range(5):
    kx = random.randint(8, S-8)
    ky = random.randint(8, S-8)
    kr = random.randint(3, 7)
    db.ellipse([kx-kr, ky-int(kr*1.7), kx+kr, ky+int(kr*1.7)],
               fill=(14, 7, 2, 255))
    db.ellipse([kx-kr+2, ky-int(kr*1.4), kx+kr-2, ky+int(kr*1.2)],
               fill=(38, 22, 8, 190))

# Moss at base
moss = Image.new("RGBA", (S,S), (0,0,0,0))
dm   = ImageDraw.Draw(moss)
for _ in range(400):
    mx = random.randint(0, S-1)
    my = random.randint(int(S*0.72), S-1)
    mr = random.randint(1, 4)
    dm.ellipse([mx,my,mx+mr,my+mr],
               fill=(28, random.randint(55,105), 18, random.randint(35,85)))
bark = Image.alpha_composite(bark, moss)
bark = bark.filter(ImageFilter.GaussianBlur(radius=0.7))
bark.save(f"{P_TEXTURES}/chimera_oak_albedo.png")
sobel_normal(bark, strength=4.5).save(f"{P_TEXTURES}/chimera_oak_normal.png")

mer = Image.new("RGB", (S,S), (0,0,208))
dm2 = ImageDraw.Draw(mer)
for _ in range(90):
    x = random.randint(0, S-1)
    dm2.line([(x,0),(x,S-1)], fill=(0,0,random.randint(180,235)), width=1)
mer.save(f"{P_TEXTURES}/chimera_oak_mer.png")
print("  [OK] chimera_oak_albedo / _normal / _mer")

# ═════════════════════════════════════════════════════════════════════════════
# 2.  BARK TOP TEXTURE — concentric growth rings  128×128
# ═════════════════════════════════════════════════════════════════════════════
print("Generating bark top (growth rings)…")
top = Image.new("RGBA", (S,S), (48, 28, 9, 255))
dt  = ImageDraw.Draw(top)
cx, cy, maxr = S//2, S//2, S//2 - 2

# Heartwood
dt.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(20, 10, 3, 255))

# Concentric rings — alternating dark/light
NUM_RINGS = 22
for i in range(1, NUM_RINGS+1):
    r    = int(maxr * i / NUM_RINGS)
    base = 40 + int(i * 1.6)
    dark = (max(base-18,10), max(base//2-8,5), max(base//4-3,1), 255)
    lite = (min(base+22,120), min(base//2+12,70), min(base//4+5,22), 200)
    dt.ellipse([cx-r, cy-r, cx+r, cy+r], outline=dark, width=2)
    if i % 2 == 0:
        dt.ellipse([cx-r+1, cy-r+1, cx+r-1, cy+r-1], outline=lite, width=1)

# Medullary rays
for angle_deg in range(0, 360, 12):
    angle = math.radians(angle_deg + random.uniform(-3,3))
    end_r = maxr * random.uniform(0.45, 0.92)
    ex = int(cx + end_r * math.cos(angle))
    ey = int(cy + end_r * math.sin(angle))
    dt.line([(cx,cy),(ex,ey)], fill=(68,42,14,110), width=1)

# Radial cracks
for _ in range(6):
    a1 = math.radians(random.uniform(0,360))
    r1 = random.uniform(0.08, 0.25) * maxr
    r2 = random.uniform(0.5,  0.92) * maxr
    jag = random.uniform(-0.18, 0.18)
    pts = [
        (cx + r1*math.cos(a1),           cy + r1*math.sin(a1)),
        (cx + ((r1+r2)/2)*math.cos(a1+jag), cy + ((r1+r2)/2)*math.sin(a1+jag)),
        (cx + r2*math.cos(a1+jag*2),      cy + r2*math.sin(a1+jag*2)),
    ]
    dt.line([(int(x),int(y)) for x,y in pts], fill=(16, 8, 2, 210), width=1)

top = top.filter(ImageFilter.GaussianBlur(radius=0.5))
top.save(f"{P_TEXTURES}/chimera_oak_top.png")
sobel_normal(top, strength=2.8).save(f"{P_TEXTURES}/chimera_oak_top_normal.png")
flat_mer(S, 195).save(f"{P_TEXTURES}/chimera_oak_top_mer.png")
print("  [OK] chimera_oak_top / _normal / _mer")

# ═════════════════════════════════════════════════════════════════════════════
# 3.  LEAVES TEXTURES  64×64
# ═════════════════════════════════════════════════════════════════════════════
print("Generating leaves textures…")
leaves = Image.new("RGBA", (64,64), (0,0,0,0))
dl = ImageDraw.Draw(leaves)
for _ in range(620):
    x = random.randint(-8,62); y = random.randint(-8,62)
    r = random.randint(2,11)
    dl.ellipse([x,y,x+r,y+r],
               fill=(random.randint(10,38), random.randint(72,198),
                     random.randint(5,28),  random.randint(208,255)))
for _ in range(30):
    x = random.randint(0,62); y = random.randint(0,62)
    dl.ellipse([x,y,x+3,y+3], fill=(50,215,55,145))
leaves.save(f"{P_TEXTURES}/chimera_oak_leaves_albedo.png")
sobel_normal(leaves, strength=0.5).save(f"{P_TEXTURES}/chimera_oak_leaves_normal.png")
flat_mer(64, 150).save(f"{P_TEXTURES}/chimera_oak_leaves_mer.png")
print("  [OK] chimera_oak_leaves_albedo / _normal / _mer")

# ═════════════════════════════════════════════════════════════════════════════
# 4.  TERRAIN TEXTURE JSON
# ═════════════════════════════════════════════════════════════════════════════
jwrite("resource_pack/textures/terrain_texture.json", {
    "resource_pack_name": "chimera",
    "texture_name": "atlas.terrain",
    "padding": 8,
    "num_mip_levels": 4,
    "texture_data": {
        "chimera_oak_bark":   {"textures": "textures/blocks/chimera_oak_bark"},
        "chimera_oak_top":    {"textures": "textures/blocks/chimera_oak_top"},
        "chimera_oak_leaves": {"textures": "textures/blocks/chimera_oak_leaves"},
    }
})
print("  [OK] terrain_texture.json")

# ═════════════════════════════════════════════════════════════════════════════
# 5.  TEXTURE SET JSONs
# ═════════════════════════════════════════════════════════════════════════════
for fname, color, mer_name, norm in [
    ("chimera_oak_bark",   "chimera_oak_albedo",       "chimera_oak_mer",      "chimera_oak_normal"),
    ("chimera_oak_top",    "chimera_oak_top",          "chimera_oak_top_mer",  "chimera_oak_top_normal"),
    ("chimera_oak_leaves", "chimera_oak_leaves_albedo","chimera_oak_leaves_mer","chimera_oak_leaves_normal"),
]:
    jwrite(f"{P_TEXTURES}/{fname}.texture_set.json", {
        "format_version": "1.16.100",
        "minecraft:texture_set": {
            "color": color,
            "metalness_emissive_roughness": mer_name,
            "normal": norm
        }
    })
print("  [OK] texture_set JSONs")

# ═════════════════════════════════════════════════════════════════════════════
# 6.  DELETE blocks.json  (conflicts with custom geometry in 1.20.80+)
# ═════════════════════════════════════════════════════════════════════════════
bj = "resource_pack/blocks.json"
if os.path.exists(bj):
    os.remove(bj)
    print("  [OK] Deleted resource_pack/blocks.json")

# ═════════════════════════════════════════════════════════════════════════════
# 7.  BLOCK DEFINITIONS
# ═════════════════════════════════════════════════════════════════════════════
jwrite(f"{P_BP_BLOCKS}/chimera_high_poly_bark.json", {
    "format_version": "1.20.80",
    "minecraft:block": {
        "description": {
            "identifier": "chimera:high_poly_bark",
            "menu_category": {"category": "nature"}
        },
        "components": {
            "minecraft:geometry": "geometry.round_bark",
            # Full 16x16 box — our geo fits within this exactly
            "minecraft:collision_box":  {"origin": [-8,0,-8], "size": [16,16,16]},
            "minecraft:selection_box":  {"origin": [-8,0,-8], "size": [16,16,16]},
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 1.5},
            "minecraft:material_instances": {
                "*":    {"texture": "chimera_oak_bark", "render_method": "opaque"},
                "top":  {"texture": "chimera_oak_top",  "render_method": "opaque"},
                "down": {"texture": "chimera_oak_top",  "render_method": "opaque"}
            }
        }
    }
})

jwrite(f"{P_BP_BLOCKS}/chimera_high_poly_leaves.json", {
    "format_version": "1.20.80",
    "minecraft:block": {
        "description": {
            "identifier": "chimera:high_poly_leaves",
            "menu_category": {"category": "nature"}
        },
        "components": {
            "minecraft:geometry": "geometry.chimera_leaves",
            "minecraft:collision_box": {"origin": [-8,0,-8], "size": [16,16,16]},
            "minecraft:selection_box": {"origin": [-8,0,-8], "size": [16,16,16]},
            "minecraft:destructible_by_mining": {"seconds_to_destroy": 0.2},
            "minecraft:material_instances": {
                "*": {"texture": "chimera_oak_leaves", "render_method": "alpha_test"}
            },
            "minecraft:light_dampening": 0
        }
    }
})
print("  [OK] block definitions")

# ═════════════════════════════════════════════════════════════════════════════
# 8.  ROUND BARK GEOMETRY  — single-bone 12-slab cylinder
#
#  CRITICAL: Bedrock block geometry does NOT support bone parenting.
#  All cubes must live in exactly ONE bone. Previous version had a child
#  "top_cap" bone which caused the tilting/floating rendering bug.
#
#  The "top" and "down" material instances on the block definition handle
#  the texture swap on top/bottom faces — no separate bone needed.
#
#  12-sided polygon cross-section from 6 axis-aligned slab pairs:
#    sx  sz   role
#     4  14   thin X / full Z  (front-back columns)
#    14   4   full X / thin Z  (left-right columns)
#     6  12   chamfer 1
#    12   6   chamfer 1 rotated
#     8  10   chamfer 2
#    10   8   chamfer 2 rotated
# ═════════════════════════════════════════════════════════════════════════════
def uv(u, v, uw, uh):
    return {"uv": [u,v], "uv_size": [uw,uh]}

SLABS = [
    (-2, -7,  4, 14),
    (-7, -2, 14,  4),
    (-3, -6,  6, 12),
    (-6, -3, 12,  6),
    (-4, -5,  8, 10),
    (-5, -4, 10,  8),
]

cubes = []
for (ox, oz, sx, sz) in SLABS:
    cubes.append({
        "origin": [ox, 0, oz],
        "size":   [sx, 16, sz],
        "uv": {
            "north": uv(0, 0, sx, 16),
            "south": uv(0, 0, sx, 16),
            "east":  uv(0, 0, sz, 16),
            "west":  uv(0, 0, sz, 16),
            "up":    uv(0, 0, sx, sz),
            "down":  uv(0, 0, sx, sz),
        }
    })

jwrite(f"{P_MODELS}/round_bark.geo.json", {
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
        "bones": [{
            "name":  "trunk",
            "pivot": [0, 0, 0],
            "cubes": cubes
        }]
    }]
})
print("  [OK] round_bark.geo.json (single-bone 12-slab cylinder)")

# ═════════════════════════════════════════════════════════════════════════════
# 9.  LEAVES GEOMETRY
# ═════════════════════════════════════════════════════════════════════════════
jwrite(f"{P_MODELS}/leaves.geo.json", {
    "format_version": "1.12.0",
    "minecraft:geometry": [{
        "description": {
            "identifier": "geometry.chimera_leaves",
            "texture_width": 64, "texture_height": 64,
            "visible_bounds_width": 2, "visible_bounds_height": 2,
            "visible_bounds_offset": [0, 0.5, 0]
        },
        "bones": [{"name": "canopy", "pivot": [0,0,0], "cubes": [{
            "origin": [-8,0,-8], "size": [16,16,16],
            "uv": {
                "north": {"uv":[0,0],"uv_size":[16,16]},
                "south": {"uv":[0,0],"uv_size":[16,16]},
                "east":  {"uv":[0,0],"uv_size":[16,16]},
                "west":  {"uv":[0,0],"uv_size":[16,16]},
                "up":    {"uv":[0,0],"uv_size":[16,16]},
                "down":  {"uv":[0,0],"uv_size":[16,16]},
            }
        }]}]
    }]
})
print("  [OK] leaves.geo.json")

# ═════════════════════════════════════════════════════════════════════════════
# 10. CHIMERA OAK FEATURE  — written every run, correct Bedrock identifiers
# ═════════════════════════════════════════════════════════════════════════════
jwrite(f"{P_BP_FEAT}/chimera_oak_feature.json", {
    "format_version": "1.13.0",
    "minecraft:tree_feature": {
        "description": {"identifier": "chimera:oak_feature"},
        "base_block": [
            "minecraft:grass",   # Bedrock: grass, NOT grass_block
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
print("  [OK] chimera_oak_feature.json")

# ═════════════════════════════════════════════════════════════════════════════
# 11. CHIMERA OAK RULE
# ═════════════════════════════════════════════════════════════════════════════
jwrite(f"{P_BP_RULES}/chimera_oak_rule.json", {
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
            "x": {"distribution": "uniform", "extent": [0,16]},
            "y": "query.heightmap(variable.worldx, variable.worldz)",
            "z": {"distribution": "uniform", "extent": [0,16]}
        }
    }
})
print("  [OK] chimera_oak_rule.json")

# ═════════════════════════════════════════════════════════════════════════════
# 12. VANILLA TREE FEATURE NULL OVERRIDES
# ═════════════════════════════════════════════════════════════════════════════
VANILLA_FEATS = [
    "oak_tree_feature", "birch_tree_feature", "fancy_tree_feature",
    "spruce_tree_feature", "pine_tree_feature", "mega_oak_feature",
    "mega_pine_tree_feature", "mega_spruce_tree_feature",
    "swamp_tree_feature", "acacia_tree_feature", "jungle_tree_feature",
    "jungle_transformation_tree_feature", "mega_jungle_tree_feature",
]
for feat in VANILLA_FEATS:
    jwrite(f"{P_BP_FEAT}/{feat}.json", {
        "format_version": "1.13.0",
        "minecraft:tree_feature": {
            "description": {"identifier": f"minecraft:{feat}"},
            "base_block": ["minecraft:end_stone"],
            "trunk": {"trunk_block": "minecraft:air",
                      "trunk_height": {"range_min":1,"range_max":1}},
            "leaf_parameters": {"leaf_block": "minecraft:air",
                                "fill_radius": {"range_min":0,"range_max":0}}
        }
    })
print(f"  [OK] {len(VANILLA_FEATS)} null vanilla tree overrides")

# ═════════════════════════════════════════════════════════════════════════════
# 13. VANILLA FEATURE RULE SUPPRESSORS
# ═════════════════════════════════════════════════════════════════════════════
VANILLA_RULES = [
    ("forest_oak_feature_rule",             "oak_tree_feature"),
    ("forest_birch_feature_rule",           "birch_tree_feature"),
    ("overworld_surface_oak_feature_rule",  "oak_tree_feature"),
    ("overworld_surface_birch_feature_rule","birch_tree_feature"),
    ("plains_oak_feature_rule",             "oak_tree_feature"),
    ("taiga_spruce_feature_rule",           "spruce_tree_feature"),
    ("taiga_pine_feature_rule",             "pine_tree_feature"),
    ("mega_taiga_spruce_feature_rule",      "mega_spruce_tree_feature"),
    ("mega_taiga_pine_feature_rule",        "mega_pine_tree_feature"),
    ("swamp_tree_feature_rule",             "swamp_tree_feature"),
    ("jungle_tree_feature_rule",            "jungle_tree_feature"),
    ("mega_jungle_tree_feature_rule",       "mega_jungle_tree_feature"),
    ("savanna_acacia_feature_rule",         "acacia_tree_feature"),
]
for name, places in VANILLA_RULES:
    jwrite(f"{P_BP_RULES}/{name}.json", {
        "format_version": "1.13.0",
        "minecraft:feature_rules": {
            "description": {
                "identifier": f"minecraft:{name}",
                "places_feature": f"minecraft:{places}"
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
print(f"  [OK] {len(VANILLA_RULES)} vanilla rule suppressors")

# ═════════════════════════════════════════════════════════════════════════════
# 14. LANG FILE
# ═════════════════════════════════════════════════════════════════════════════
os.makedirs("resource_pack/texts", exist_ok=True)
with open("resource_pack/texts/en_US.lang", "w") as f:
    f.write("tile.chimera:high_poly_bark.name=Round Oak Log\n")
    f.write("tile.chimera:high_poly_leaves.name=Round Oak Leaves\n")
print("  [OK] en_US.lang")

print("""
╔══════════════════════════════════════════════════════╗
║   Project Chimera Asset Generator — Complete         ║
╠══════════════════════════════════════════════════════╣
║  COMMIT ALL OUTPUT FILES BEFORE BUILDING APK         ║
║                                                      ║
║  Natural spawn checklist:                            ║
║  1. Script ran with no errors (✓ you're here)        ║
║  2. git add -A && git commit                         ║
║  3. Build fresh APK                                  ║
║  4. NEW world only — existing chunks never update    ║
║  5. Forest biome — /locate biome forest if needed    ║
║  6. Both BP + RP active in world settings            ║
╚══════════════════════════════════════════════════════╝
""")
