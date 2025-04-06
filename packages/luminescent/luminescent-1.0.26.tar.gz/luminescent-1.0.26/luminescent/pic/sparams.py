from .setup import *
from ..constants import *
from ..layers import *
from ..utils import *
import gdsfactory as gf
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

from gdsfactory.cross_section import Section
from gdsfactory.generic_tech import LAYER_STACK, LAYER


def make_prob(path,  nres,
              component=None,
              wavelengths=None,
              entries=None, keys=["2,1"],
              layer_stack=SOI,
              study="sparams",
              sources=None, monitors=None,
              frequencies=None,   reference_wavelength=None,
              source_port_margin=.1,
              T=None,
              **kwargs):
    if frequencies is not None:
        frequencies = wrap(frequencies)
        assert reference_wavelength is not None
        assert wavelengths is None
        wavelengths = [[reference_wavelength /
                       f for f in v] for v in frequencies]
    else:
        wavelengths = wrap(wavelengths)

    wavelengths = [sorted(w) for w in wavelengths]
    wavelengths = sorted(wavelengths, key=lambda x: x[0])
    center_wavelength = median(map(median, wavelengths))

    if not entries:
        entries = []

        for w in wavelengths:
            for k in keys:
                entries.append([w, *unpack_sparam_key(k)])

    l = []
    for w, po, mo, pi, mi in entries:
        k = [w, pi, mi, pi, mi]
        if k not in entries:
            l.append(k)
    entries.extend(l)

    imow = {}
    for w, po, mo, pi, mi in entries:
        if pi not in imow:
            imow[pi] = {}
        if mi not in imow[pi]:
            imow[pi][mi] = {}

        if po not in imow[pi][mi]:
            imow[pi][mi][po] = mo
        else:
            imow[pi][mi][po] = max(imow[pi][mi][po], mo)

    runs = []
    for _w in [1]:
        for i in imow:
            for mi in imow[i]:
                d = {
                    "sources": {
                        i: {
                            "wavelength_mode_numbers": [[w, [mi]] for w in wavelengths],
                        }},
                    "monitors": {
                        o: {
                            "wavelength_mode_numbers": [[w, list(range(imow[i][mi][o]+1))] for w in wavelengths],
                        } for o in imow[i][mi]}}
                d["sources"] = SortedDict(d["sources"])
                d["monitors"] = SortedDict(d["monitors"])
                if component is None:
                    0
                else:
                    runs.append(d)

    prob = setup(path, component=component, study=study,  nres=nres, center_wavelength=center_wavelength,
                 runs=runs,
                 source_port_margin=source_port_margin,
                 #  sources=sources, monitors=monitors,
                 layer_stack=layer_stack, **kwargs)
    prob["wavelengths"] = wavelengths
    prob["T"] = T
    save_problem(prob, path)
    return prob

    # l = [k for k in imow if port_number(k) == pi]
    # if not l:
    #     imow[f"o{pi}@{mi}"] = []
    # else:
    #     k = l[0]
    #     mn = max(mode_number(k), mi)
    #     if mn != mode_number(k):
    #         imow[i] = imow[k]
    #         del imow[k]

    # l = [k for k in imow[i] if port_number(k) == po]
    # if not l:
    #     imow[f"o{pi}@{mi}"]
    # else:
    #     k = l[0]
    #     mn = max(mode_number(k), mi)
    #     if mn != mode_number(k):
    #         imow[f"o{pi}@{mn}"] = imow[k]
    #         del imow[k]

    # if po not in imow[pi]:
    #     imow[pi]["o"][po] = mo
    # else:
    #     imow[pi]["o"][po] = max(imow[pi]["o"][po], mo)
