from typing import Iterable
from datetime import datetime
import getpass

from geometry.wing_geometry import WingGeometry
from data.data_classes import MetaData, AlphaEpsilonSimulation, FlyingWing, SolverOutputData
from data.data_writer import get_data_dir
from solver.aerosandbox_solver import abs_vortex_lattice_method

def __get_max_aero_coff_error(prev_solver_output: SolverOutputData, new_solver_output: SolverOutputData):
    cl_err = float(abs(new_solver_output.output_data["CL"] - prev_solver_output.output_data["CL"])/abs(prev_solver_output.output_data["CL"]))
    cm_err = float(abs(new_solver_output.output_data["Cm"] - prev_solver_output.output_data["Cm"])/abs(prev_solver_output.output_data["Cm"]))
    cd_err = float(abs(new_solver_output.output_data["CD"] - prev_solver_output.output_data["CD"])/abs(prev_solver_output.output_data["CD"]))
    return max([cl_err, cm_err, cd_err])



def alpha_epsilon_simulation(flying_wing: FlyingWing, new_simulation_id: str, alpha_values: Iterable, twist_values: Iterable, velocity: float, 
                                number_sections: int = 2, chordwise_panel_number: int = 8, spanwise_panel_number: int = 8, target_aero_coff_error: float = 0.01):

    wing_geo = flying_wing.wing_geometry

    meta_data = MetaData(user= getpass.getuser(), solver= "AeroSandBox VML", solver_version= "0.0", time_stamp= str(datetime.now()), simulation_type= "Alpha/Twist Simulation")
    solver_input = {"chordwise_panel_number": chordwise_panel_number, "spanwise_panel_number": spanwise_panel_number, "number_sections": number_sections}

    if not target_aero_coff_error is None:

        wing_geo.current_total_twist = 0
        max_aero_coff_error = None

        while max_aero_coff_error is None or max_aero_coff_error > target_aero_coff_error:

            prev_solver_output = abs_vortex_lattice_method(wing_geo, velocity, 5, 0,  number_sections, chordwise_panel_number , spanwise_panel_number)
            chordwise_panel_number += 2
            spanwise_panel_number += 2
            new_solver_output = abs_vortex_lattice_method(wing_geo, velocity, 5, 0,  number_sections, chordwise_panel_number , spanwise_panel_number)
            max_aero_coff_error = __get_max_aero_coff_error(prev_solver_output, new_solver_output)

    #print(f"Error: {max_aero_coff_error}, Panel numbers: {spanwise_panel_number}x{chordwise_panel_number}")

    alpha_epsilon_array = []

    for alpha in alpha_values:

        solver_outputs = []
        
        for twist in twist_values:

            wing_geo.current_total_twist = twist
            solver_outputs.append(abs_vortex_lattice_method(wing_geo, velocity, alpha, 0,  number_sections, chordwise_panel_number, spanwise_panel_number))

        alpha_epsilon_array.append(solver_outputs)

    wing_geo.current_total_twist = 0
    simu_data = AlphaEpsilonSimulation(new_simulation_id, flying_wing, meta_data, [], alpha_values, twist_values, velocity, solver_input, alpha_epsilon_array)

    if not new_simulation_id:
        new_simulation_id = f"Alpha_Epsilon_Simulation_{len(flying_wing.simulations)}"

    return simu_data














