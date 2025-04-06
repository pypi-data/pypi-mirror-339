
from ..constants import *
from ..utils import *
import gdsfactory as gf
from gdsfactory.cross_section import Section
from networkx import center
from numpy import cumsum
from gdsfactory.generic_tech import LAYER_STACK, LAYER

# import .utils as utils
# from layers import *


def port_bbox(p):
    c = np.array(p.center)
    v = p.width/2*np.array([np.sin(np.radians(p.orientation)),
                           -np.cos(np.radians(p.orientation))])
    return [(c-v).tolist(), (c+v).tolist()]


def mimo(l, w,
         west=0, east=0, south=0, north=0,
         lwg_in=None, lwg_out=None, taper=0.04,
         wwg=.5,  wwg_west=None, wwg_east=None, wwg_south=None, wwg_north=None,
         ports_in=[],
         layer=LAYER.WG,           canvas_layer=CANVAS_LAYER,
         **kwargs):
    design = gf.Component()
    c = gf.Component(**kwargs)
    if lwg_in is None:
        lwg_in = wwg
    if lwg_out is None:
        lwg_out = 2*wwg

    p = [(0, 0), (l, 0), (l, w), (0, w)]
    design.add_polygon(p,                       layer=canvas_layer)
    c.add_polygon(p,                       layer=layer)

    port_pos_sides = [west, north,  east, south]
    for i, v, d in zip(range(4), port_pos_sides, [w, w, l, l]):
        if type(v) is int:
            port_pos_sides[i] = [(.5+j)*d/v for j in range(v)]

    wwg_sides = [wwg_west, wwg_east, wwg_south, wwg_north]
    for i, v in enumerate(wwg_sides):
        n = len(port_pos_sides[i])
        if v is None:
            v = wwg
        if type(v) is float or type(v) is int:
            wwg_sides[i] = [v]*n

    portnum = 1
    for (i, x, y, ds, wwgs, orientation) in zip(
        range(4),
        [0,  0, l, l],
        [0, w, w, 0],
        port_pos_sides,
        wwg_sides,
        [180, 90, 0, -90]
    ):
        for wwg, d in zip(wwgs, ds):
            center = [x+cos(np.radians(orientation-90))*d, y +
                      sin(np.radians(orientation-90))*d]
            if portnum in ports_in:
                wwg2 = wwg+taper*lwg_in
                lwg = lwg_in
            else:
                wwg2 = wwg+taper*lwg_out
                lwg = lwg_out

            name = "o"+str(portnum)
            design.add_port(name, center=center, width=wwg2,
                            orientation=orientation, layer=layer)
            wg = c << gf.components.taper(
                length=lwg, width1=wwg, width2=wwg2, layer=layer)
            wg.connect("o2", design.ports[name])
            c.add_port(name, port=wg.ports["o1"])
            portnum += 1

    design = c << design
    # for i in ports_in:
    #     for j in out_ports:
    #         pi = design.ports[f'o{i}']
    #         pj = design.ports[f'o{j}']
    #         # a = port_bbox(design.ports[f'o{i}'])
    #         # b = port_bbox(design.ports[f'o{j}'])
    #         p1 = np.array(pi.center)
    #         p2 = np.array(pj.center)
    #         n1 = np.array([cos(np.radians(pi.orientation)),
    #                        sin(np.radians(pi.orientation))])
    #         n2 = np.array([cos(np.radians(pj.orientation)),
    #                        sin(np.radians(pj.orientation))])
    #         v = p2-p1
    #         d = np.linalg.norm(v)
    #         v = v/d
    #         l = [p1,
    #              p1-.4*d*n1,
    #              #  p1+.5*d*(.3*v-.7*n1),
    #              #  p2+.5*d*(-.3*v-.7*n2),
    #              p2-.4*d*n2,
    #              p2]
    #         c << gf.components.bends.bezier(
    #             [x.tolist() for x in l],
    #             # start_angle=pi.orientation-180,
    #             # end_angle=pj.orientation,
    #             allow_min_radius_violation=True,
    #             width=pi.width,)  # layer=layer)
    #         # c.add_polygon(a+b, layer=layer)
    return c
