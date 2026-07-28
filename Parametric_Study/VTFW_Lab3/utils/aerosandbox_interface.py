import aerosandbox as asb
import aerosandbox.numpy as np
import re
from datetime import datetime
import getpass
from geometry.wing_geometry import WingGeometry
from geometry.airfoil import Airfoil
from data.data_classes import *


def convert_airfoil_2aersandbox_airfoil(airfoil: Airfoil, number_points: int):
    """
    Converts an airfoil into an aerosandbox airfoil
    """
    airfoil_surf_points = []
    for p in airfoil.get_lin_dist_surface_points(number_points):
        airfoil_surf_points.append([p[1], p[2]])

    return asb.Airfoil(coordinates=np.array(airfoil_surf_points))


def convert_wing_2aerosandbox_wing(wing: WingGeometry, number_sections: int):
    """
    Converts a wing into an aerosandbox wing
    """
    y_sections = np.linspace(0, wing.half_span, number_sections)
    sections = [asb.WingXSec(xyz_le = wing.leading_edge(y),chord = wing.chord_len(y), 
                             airfoil=convert_airfoil_2aersandbox_airfoil(wing.airfoil(y), 1000), twist= wing.twist(y)) for y in y_sections]

    return asb.Wing(name="wing", symmetric=True, xsecs= sections)


def convert_wing_2aerosandbox_wing_tw_2ax(wing: WingGeometry, number_sections: int):
    """
    Converts a wing into an aerosandbox wing
    """
    y_sections = np.linspace(0, wing.half_span, number_sections)
    sections = [asb.WingXSec(xyz_le = [wing.leading_edge(y)[0], wing.leading_edge(y)[1], wing.leading_edge(y)[2]], chord = wing.chord_len(y), airfoil=convert_airfoil_2aersandbox_airfoil(wing.airfoil(y), 1000), twist= wing.twist(y)) for y in y_sections]

    return asb.Wing(name="wing", symmetric=True, xsecs= sections)