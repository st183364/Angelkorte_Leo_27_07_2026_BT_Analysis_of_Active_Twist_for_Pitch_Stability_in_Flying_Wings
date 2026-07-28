import aerosandbox as asb
import aerosandbox.numpy as np
import re
from datetime import datetime
import getpass
from geometry.wing_geometry import WingGeometry
from geometry.airfoil import Airfoil
from data.data_classes import *
from typing import Iterable
from datetime import datetime
import getpass
import copy

from geometry.wing_geometry import WingGeometry, mean_aerodynamic_chord
from data.data_classes import MetaData, SimulationData, FlyingWing
from data.data_writer import get_data_dir



def _convert_airfoil_2asb_airfoil(airfoil: Airfoil, number_points: int):
    """
    Converts an airfoil into an aerosandbox airfoil
    """
    airfoil_surf_points = []
    for p in airfoil.get_lin_dist_surface_points(number_points):
        airfoil_surf_points.append([p[1], p[2]])

    return asb.Airfoil(coordinates=np.array(airfoil_surf_points))


def _convert_wing_2asb_wing(wing: WingGeometry, number_sections: int):
    """
    Converts a wing into an aerosandbox wing
    """
    y_sections = np.linspace(0, wing.half_span, number_sections)
    sections = [asb.WingXSec(xyz_le = wing.leading_edge(y),chord = wing.chord_len(y), 
                             airfoil=_convert_airfoil_2asb_airfoil(wing.airfoil(y), 1000), twist= wing.twist(y)) for y in y_sections]

    return asb.Wing(name="wing", symmetric=True, xsecs= sections)


def _convert_asb_result_2output_data(asb_result: dict):
    output_data = {
        "F_w": asb_result["F_w"],          
        "M_w": asb_result["M_w"],          

        "F_b": asb_result["F_b"],        
        "M_b": asb_result["M_b"], 

        "L":   asb_result["L"],    
        "Y":   asb_result["Y"],    
        "D":   asb_result["D"],    

        "CL":  asb_result["CL"],           
        "CY":  asb_result["CY"],         
        "CD":  asb_result["CD"],         

        "CM":  asb_result["Cm"]          
    }

    return output_data



def run_asb_vlm(flying_wing: FlyingWing, new_simulation_id: str, velocity: float, alpha: float, beta: float, extra_input_data: dict = {},
                                                        number_sections: int = 2, chordwise_panel_number: int = 8, spanwise_panel_number: int= 14):
    wing_geo = flying_wing.wing_geometry

   
    meta_data = MetaData(user= getpass.getuser(), solver= "AeroSandBox VML", time_stamp= str(datetime.now()), extra_data={})

    input_data = {
        "Wing geometry": copy.deepcopy(wing_geo), 
        "Velocity": velocity, 
        "Alpha": alpha, 
        "Beta": beta, 
        "Number of sections": number_sections, 
        "Chordwise panel number": chordwise_panel_number, 
        "Spanwise panel number": spanwise_panel_number}
    
    input_data.update(extra_input_data)

    airplane = asb.Airplane(name="plane", wings=[_convert_wing_2asb_wing(wing_geo, number_sections)])
    op_point = asb.OperatingPoint(velocity= velocity, alpha= alpha, beta= beta)
    vlm = asb.VortexLatticeMethod(airplane=airplane, op_point=op_point,  xyz_ref= [0.25*mean_aerodynamic_chord(wing_geo), 0, 0], chordwise_resolution= chordwise_panel_number, spanwise_resolution= spanwise_panel_number)
    vml_results = vlm.run()
    asb_output_data = {}
    asb_output_data.update(vml_results)

    simulation = SimulationData(new_simulation_id, meta_data, input_data, _convert_asb_result_2output_data(asb_output_data))
    flying_wing.simulations.append(simulation)
    return simulation


def run_multi_asb_vlm(flying_wing: FlyingWing, new_simulation_id: str, velocity_values: float, alpha_values: float, beta_values: float, 
                      extra_input_data: dict = {}, number_sections: int = 2, chordwise_panel_number: int = 8, spanwise_panel_number: int= 14):

    simulations = []
    for velocity in velocity_values:
        for alpha in alpha_values:
            for beta in beta_values:

                simulations.append(run_asb_vlm(flying_wing, new_simulation_id, velocity, alpha, beta, 
                                               extra_input_data, number_sections, chordwise_panel_number, spanwise_panel_number))

    return simulations




