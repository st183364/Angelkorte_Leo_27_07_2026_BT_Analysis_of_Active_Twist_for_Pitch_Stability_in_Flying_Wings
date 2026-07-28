import numpy as np
from typing import Tuple, Callable
import aerosandbox as asb
from geometry.airfoil import Airfoil
from typing import Iterable
from geometry.naca_airfoil import NACA4
#import aerosandbox.numpy as np


class WingGeometry:
    
    def __init__(self, id: str, wingspan: float, leading_edge_fn: Callable[[float], Tuple[float, float, float]], 
                 chord_len_fn: Callable[[float], float], airfoil_fn: Callable[[float], Airfoil], 
                                twist_fn: Callable[[float, float], float], current_total_twist: float = 0):
        
        self.id = id

        self.wingspan = wingspan
        self.half_span = wingspan / 2

        self._leading_edge_fn = leading_edge_fn
        self._chord_fn = chord_len_fn
        self._airfoil_fn = airfoil_fn
        self._twist_fn = twist_fn
        self.current_total_twist = current_total_twist

    def leading_edge(self, y: float):
        """
        Returns the 3D coordinates (x, y, z) of the leading edge at spanwise location y.
        """
        return self._leading_edge_fn(y)

    def chord_len(self, y: float):
        """
        Returns the chord length at spanwise location y.
        """
        return self._chord_fn(y)

    def airfoil(self, y: float):
        """
        Returns the airfoil at spanwise location y.
        """
        return self._airfoil_fn(y)

    def twist(self, y: float):
        """
        Returns the local twist at spanwise location y dependent on the total twist.
        """
        return self._twist_fn(y, self.current_total_twist)
    
    

def get_airfoil_loft_fn(sections: list[Tuple[float, Airfoil]]):
    """
    Returns a function that creates a loft between multiple airfoil cross sections. 
    The sections list should contain a tuple of the y location and the airfoil at that positon.
    """
    pass


def wing_area(wing: WingGeometry, n: int = 5000) -> float:
    ys = np.linspace(0.0, wing.half_span, n)
    chords = np.array([wing.chord_len(y) for y in ys])
    S_half = np.trapezoid(chords, ys)
    return 2.0 * S_half

def mean_aerodynamic_chord(wing: WingGeometry, n: int = 5000) -> float:
    ys = np.linspace(0.0, wing.half_span, n)
    chords = np.array([wing.chord_len(y) for y in ys])
    S = wing_area(wing, n)
    c_bar = 2.0 / S * np.trapezoid(chords**2, ys)
    return c_bar

def mac_leading_edge_position(wing: WingGeometry, n: int = 5000):
    ys = np.linspace(0.0, wing.half_span, n)
    chords = np.array([wing.chord_len(y) for y in ys])
    le_coords = np.array([wing.leading_edge(y) for y in ys])  # shape (n, 3)
    S = wing_area(wing, n)

    x_LE_MAC = float(2.0 / S * np.trapezoid(le_coords[:, 0] * chords, ys))
    y_LE_MAC = 0.0  # by symmetry
    z_LE_MAC = float(2.0 / S * np.trapezoid(le_coords[:, 2] * chords, ys))
    return x_LE_MAC, y_LE_MAC, z_LE_MAC

def wing_aerodynamic_center(wing: WingGeometry, n: int = 5000):
    c_bar = mean_aerodynamic_chord(wing, n)
    x_LE_MAC, y_LE_MAC, z_LE_MAC = mac_leading_edge_position(wing, n)

    x_ac = x_LE_MAC + 0.25 * c_bar
    y_ac = y_LE_MAC
    z_ac = z_LE_MAC  # or add quarter-chord offset if your chord line is not horizontal
    return x_ac, y_ac, z_ac

def get_sweep_angle(wing: WingGeometry):
    """
    Returns the sweep angle of the wing
    """
    return float(np.rad2deg(np.arctan(wing.leading_edge(wing.half_span)[0]/wing.half_span)))

def get_taper_ratio(wing: WingGeometry):
    """
    Returns the taper ratio of the wing
    """
    return wing.chord_len(wing.half_span)/wing.chord_len(0)


def get_aspect_ratio(wing: WingGeometry):
    """
    Returns the aspect ratio of a wing
    """
    return (wing.wingspan**2)/wing_area(wing)

def get_trapezoidal_aspect_ratio(wing: WingGeometry):
    """
    Returns the taper ratio of a trapezoidal wing
    """
    return (2*wing.wingspan)/(wing.chord_len(0) + wing.chord_len(wing.half_span))



