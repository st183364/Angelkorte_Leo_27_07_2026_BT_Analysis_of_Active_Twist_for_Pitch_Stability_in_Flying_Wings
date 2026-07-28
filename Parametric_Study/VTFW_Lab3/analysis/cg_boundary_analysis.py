from data.data_classes import AlphaEpsilonSimulation, CGBoundaryAnalysis, FlyingWing
from geometry.wing_geometry import mean_aerodynamic_chord, wing_aerodynamic_center
import numpy as np
from utils.common import find_simulation

def cg_boundary_analysis(flying_wing: FlyingWing, simulation_id: str, new_analysis_id: str = None):
    alpha_eps_simu = find_simulation(flying_wing, simulation_id)
    wing = flying_wing.wing_geometry

    cg_pos_array = []
    max_cg_postions = []
    min_cg_postions = []

    for alpha, eps_solver_outputs in zip(alpha_eps_simu.alpha_values, alpha_eps_simu.alpha_epsilon_array):
        current_cg_postions = []
        for epsilon, solver_output in zip(alpha_eps_simu.epsilon_values, eps_solver_outputs):

            if hasattr(solver_output, "output_data"):
                solver_output = solver_output.output_data

            CL = solver_output.get("CL")
            CD = solver_output.get("CD")

            CM = (solver_output.get("Cm") or solver_output.get("CMy"))

            
            alpha_rad = np.deg2rad(alpha)           
            current_cg_pos =  -1*(mean_aerodynamic_chord(wing)*CM)/(np.sin(alpha_rad)*CD + np.cos(alpha_rad)*CL)
            #current_cg_pos = 0.25*mean_aerodynamic_chord(wing) - (CM*mean_aerodynamic_chord(wing))/CL
            current_cg_postions.append(current_cg_pos)

        max_cg_postions.append(max(current_cg_postions))
        min_cg_postions.append(min(current_cg_postions))
        cg_pos_array.append(current_cg_postions)

    cg_max = min(max_cg_postions)
    cg_min = max(min_cg_postions)
    cg_delta = cg_max - cg_min

    if not new_analysis_id:
        new_analysis_id = f"CG_Boundary_Analysis_{len(alpha_eps_simu.analysis_data)}"


    analysis = CGBoundaryAnalysis(new_analysis_id, alpha_eps_simu, alpha_eps_simu.alpha_values, alpha_eps_simu.epsilon_values, alpha_eps_simu.velocity, 
                                                            max_cg_postions, min_cg_postions, cg_max, cg_delta, cg_min, cg_pos_array)
    
    alpha_eps_simu.analysis_data.append(analysis)
    
    return analysis





