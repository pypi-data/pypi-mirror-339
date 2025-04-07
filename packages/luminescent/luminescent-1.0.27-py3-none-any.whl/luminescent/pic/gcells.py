
from scipy.special import comb
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
    v = p.width/2*np.array([np.cos(np.radians(p.orientation+90)),
                           np.sin(np.radians(p.orientation+90))])
    return [(c-v).tolist(), (c+v).tolist()]


def bezier_curve(points, num_points=100):
    n = len(points) - 1
    t = np.linspace(0, 1, num_points)
    curve_points = np.zeros((num_points, 2))

    for i, t_val in enumerate(t):
        for j, point in enumerate(points):
            curve_points[i] += comb(n, j) * (t_val ** j) * \
                ((1 - t_val) ** (n - j)) * point

    return curve_points


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
    # c.add_polygon(p,                       layer=layer)

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

    nports = 0
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
            nports += 1
            if nports in ports_in:
                wwg2 = wwg+taper*lwg_in
                lwg = lwg_in
            else:
                wwg2 = wwg+taper*lwg_out
                lwg = lwg_out

            name = "o"+str(nports)
            design.add_port(name, center=center, width=wwg2,
                            orientation=orientation, layer=layer)
            wg = c << gf.components.taper(
                length=lwg, width1=wwg, width2=wwg2, layer=layer)
            wg.connect("o2", design.ports[name])
            c.add_port(name, port=wg.ports["o1"])

    design = c << design
    p = []
    for i in range(nports):
        # for i in [0]:
        pi = design.ports[f'o{i+1}']
        pj = design.ports[f'o{((i+1) % nports)+1}']
        a, _ = np.array(port_bbox(pi))
        _, b = np.array(port_bbox(pj))
        n1 = - np.array([cos(np.radians(pi.orientation)),
                         sin(np.radians(pi.orientation))])
        n2 = -np.array([cos(np.radians(pj.orientation)),
                       sin(np.radians(pj.orientation))])
        v = b-a
        d = np.linalg.norm(v)
        n = v/d

        # l=[a, a+.3*d * (.5*n+.5*n1),  b+.3*d*(-.5*n+.5*n2), b]
        l = [a, a+.5*d * n1,  b+.5*d*n2, b]
        p.extend(bezier_curve(l))

        # p.extend([a+s*d * (2*s*n+(1-2*s)*n1) for s in np.linspace(0, .5, 50)])
        # p.extend(reversed([b+s*d * (-2*s*n+(1-2*s)*n2)
        #          for s in np.linspace(0, .5, 50)]))
        # c << gf.components.bends.bezier(
        #     [x.tolist() for x in l],
        #     # start_angle=pi.orientation-180,
        #     # end_angle=pj.orientation,
        #     allow_min_radius_violation=True,
        #     width=pi.width,)  # layer=layer)
    c.add_polygon(p, layer=layer)
    return c
