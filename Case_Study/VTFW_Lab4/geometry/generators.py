import numpy as np

from typing import Iterable, List, Union, Optional
from geometry.airfoil import Airfoil
from geometry.wing_geometry import WingGeometry
from geometry.naca_airfoil import NACA4


def create_trapezoidal_dimensionalized_wing(taper_ratio: float, aspect_ratio: float, sweep: float, airfoil: Airfoil):
    """
    Returns a trapezoidal wing geometry with one profile based on the given wing shape parameters with a mean aerodynamic chord of 1.0
    """
    chord_len_root = (3/2) * (1 + taper_ratio) / (1 + taper_ratio + taper_ratio**2)

    chord_len_tip = chord_len_root*taper_ratio

    wingspan = 0.5 * aspect_ratio * (chord_len_root + chord_len_tip)

    x_tip_offset = float(np.tan(np.deg2rad(sweep))*(wingspan/2))

    leading_edge_fn  = lambda y: (x_tip_offset*(2*np.abs(y))/wingspan, y, 0)
    chord_len_fn = lambda y: chord_len_root + (chord_len_tip - chord_len_root)*(2*np.abs(y))/wingspan
    twist_fn = lambda y, twist: twist*(2*np.abs(y))/wingspan

    airfoil_fn = lambda y: airfoil

    return WingGeometry(f"TR{taper_ratio}_AR{aspect_ratio}_SW{sweep}_AF{airfoil.name}", wingspan, leading_edge_fn, chord_len_fn, airfoil_fn, twist_fn)



def get_wing_geometries(taper_ratios: Iterable, aspect_ratios: Iterable, sweep_angels: Iterable, airfoils: Iterable) -> list[WingGeometry]:
    """
    Returns a list of trapezoidal flying wings with a mean aerodynamic chord of 1.0 and all possbile combinations for the given wing shape parameters
    """
    wings = []

    for current_sweep in sweep_angels:
        for current_aspect_ratio in aspect_ratios:
            for current_taper_ratio in taper_ratios:
                for airfoil in airfoils:

                    wings.append(create_trapezoidal_dimensionalized_wing(current_taper_ratio, current_aspect_ratio, current_sweep, airfoil))
    return wings