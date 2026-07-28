import numpy as np

from typing import Iterable, List, Union, Optional
from geometry.airfoil import Airfoil
from geometry.wing_geometry import WingGeometry
from geometry.naca_airfoil import NACA4

def generate_naca4_codes(
    max_cambers: Iterable[Union[int, str]], camber_positions: Iterable[Union[int, str]], thicknesses: Iterable[Union[int, str]],) -> List[NACA4]:
    """
    Generate NACA 4-digit codes.

    - max_cambers: values 0..9
    - camber_positions: values 0..9
    - thicknesses: values 1..40
    - return_objects: Naca4 objects
    """
    def to_int(v, name):
        try:
            iv = int(float(v))
        except Exception:
            raise ValueError(f"Invalid {name}: {v}")
        return iv

    codes = []
    for mc in max_cambers:
        mc_i = to_int(mc, "max_camber")
        if not (0 <= mc_i <= 9):
            raise ValueError(f"max_camber must be 0..9, got {mc}")
        for cp in camber_positions:
            cp_i = to_int(cp, "camber_position")
            if not (0 <= cp_i <= 9):
                raise ValueError(f"camber_position must be 0..9, got {cp}")
            for th in thicknesses:
                th_i = to_int(th, "thickness")
                if not (1 <= th_i <= 40):
                    raise ValueError(f"thickness must be 1..40, got {th}")
                thickness_str = f"{th_i:02d}"          # two digits
                code = f"{mc_i}{cp_i}{thickness_str}"  # exactly 4 chars
                if len(code) != 4:
                    raise RuntimeError(f"Generated code has wrong length: {code}")
                codes.append(NACA4(code))
    return codes


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