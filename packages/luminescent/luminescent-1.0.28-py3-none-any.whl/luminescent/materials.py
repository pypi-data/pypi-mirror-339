from gdsfactory.technology import LogicalLayer, LayerLevel, LayerStack
from gdsfactory.generic_tech.layer_map import LAYER
import gdsfactory as gf
import copy
from gdsfactory.generic_tech import LAYER_STACK, LAYER
LAYER_WG = LAYER.WG
LAYER_SUB = (2, 0)
CANVAS_LAYER = (8888, 1)

MATERIALS = {
    'air': {'epsilon': 1.0},

    "cSi": {'epsilon': 3.48**2},
    "SiO2": {'epsilon': 1.44**2},
    "SiN": {'epsilon': 2.0**2},
    "Ge": {'epsilon': 4.0**2},
    "Si": {'epsilon': 3.48**2},
    'ZeSe': {'epsilon': 5.7},

    'FR4': {'epsilon': 4.4},
    'Al2O3': {'epsilon': 9.9},

    'canvas': {'epsilon': None},
    'PEC': {'epsilon': 1000},
}

ks = copy.deepcopy(list(MATERIALS.keys()))
for k in ks:
    MATERIALS[k.lower()] = MATERIALS[k]


nm = 1e-3
thickness_wg = 220 * nm
thickness_slab_deep_etch = 90 * nm
thickness_slab_shallow_etch = 150 * nm

sidewall_angle_wg = 0
layer_core = LogicalLayer(layer=LAYER.WG)
layer_shallow_etch = LogicalLayer(layer=LAYER.SHALLOW_ETCH)
layer_deep_etch = LogicalLayer(layer=LAYER.DEEP_ETCH)

layers = {
    "core": LayerLevel(
        layer=LogicalLayer(layer=LAYER.WG),
        thickness=thickness_wg,
        zmin=0.0,
        material="si",
        mesh_order=2,
    ),
    # "shallow_etch": LayerLevel(
    #     layer=LogicalLayer(layer=LAYER.SHALLOW_ETCH),
    #     thickness=thickness_wg - thickness_slab_shallow_etch,
    #     zmin=0.0,
    #     material="si",
    #     mesh_order=1,
    #     derived_layer=LogicalLayer(layer=LAYER.SLAB150),
    # ),
    # "deep_etch": LayerLevel(
    #     layer=LogicalLayer(layer=LAYER.DEEP_ETCH),
    #     thickness=thickness_wg - thickness_slab_deep_etch,
    #     zmin=0.0,
    #     material="si",
    #     mesh_order=1,
    #     derived_layer=LogicalLayer(layer=LAYER.SLAB90),
    # ),
    # "slab150": LayerLevel(
    #     layer=LogicalLayer(layer=LAYER.SLAB150),
    #     thickness=150e-3,
    #     zmin=0,
    #     material="si",
    #     mesh_order=3,
    # ),
    # "slab90": LayerLevel(
    #     layer=LogicalLayer(layer=LAYER.SLAB90),
    #     thickness=thickness_slab_deep_etch,
    #     zmin=0.0,
    #     material="si",
    #     mesh_order=2,
    # ),
}


SOI = LayerStack(layers=layers)
SOI.layers['default'] = {
    'material': 'SiO2'
}

th_sub = 1.6
layers = {
    "top": LayerLevel(
        layer=LogicalLayer(layer=LAYER.WG),
        thickness=.1,
        zmin=th_sub,
        material="PEC",
        mesh_order=1,
    ),
    'core': LayerLevel(
        layer=LogicalLayer(layer=(2, 0)),
        thickness=th_sub,
        zmin=0.0,
        material="FR4",
        mesh_order=2,
    ),
    'bot': LayerLevel(
        layer=LogicalLayer(layer=(2, 0)),
        thickness=.1,
        zmin=-.1,
        material="PEC",
        mesh_order=3,
    ),
}


MS = LayerStack(layers=layers)
MS.layers['default'] = {
    'material': 'air'
}
BBOX = (8888, 8888)


MATKEYS = {
    "si": "cSi",
    "Si": "cSi",

    "sio2": "SiO2",
    "sin": "SiN",
    "ge": "Ge",

}


def matname(k):
    if k in MATKEYS:
        return MATKEYS[k]
    return k.capitalize()
