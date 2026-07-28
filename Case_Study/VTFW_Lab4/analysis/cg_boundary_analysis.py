from data.data_classes import AnalysisData, SimulationData, FlyingWing
from geometry.wing_geometry import mean_aerodynamic_chord, wing_aerodynamic_center
import numpy as np
import pandas as pd
from utils.common import find_simulation

def get_lin_cm_cg(simulation: SimulationData, X_CG: float):
        CL = simulation.output_data.get("CL")
        CD = simulation.output_data.get("CD")
        CM = simulation.output_data.get("CM")

        alpha_rad = np.deg2rad(simulation.input_data.get("Alpha"))    
        wing_geometry =  simulation.input_data.get("Wing geometry")

        C_MAC = mean_aerodynamic_chord(wing_geometry)
        X_AC = 0.25*C_MAC

        return CL*(X_CG - X_AC)/C_MAC + CM

def get_lin_cg_for_trim(simulation: SimulationData):
        CL = simulation.output_data.get("CL")
        CD = simulation.output_data.get("CD")
        CM = simulation.output_data.get("CM")


        alpha_rad = np.deg2rad(simulation.input_data.get("Alpha"))    
        wing_geometry =  simulation.input_data.get("Wing geometry")

        C_MAC = mean_aerodynamic_chord(wing_geometry)
        X_AC = 0.25*C_MAC

        return X_AC -1*(C_MAC*CM)/CL

def get_cm_cg(simulation: SimulationData, X_CG: float):
        CL = simulation.output_data.get("CL")
        CD = simulation.output_data.get("CD")
        CM = simulation.output_data.get("CM")

        alpha_rad = np.deg2rad(simulation.input_data.get("Alpha"))    
        wing_geometry =  simulation.input_data.get("Wing geometry")

        C_MAC = mean_aerodynamic_chord(wing_geometry)
        X_AC = 0.25*C_MAC

        return (CL*np.cos(alpha_rad) + CD*np.sin(alpha_rad))*(X_CG - X_AC)/C_MAC + CM


def get_cg_for_trim(simulation: SimulationData):
        CL = simulation.output_data.get("CL")
        CD = simulation.output_data.get("CD")
        CM = simulation.output_data.get("CM")


        alpha_rad = np.deg2rad(simulation.input_data.get("Alpha"))    
        wing_geometry =  simulation.input_data.get("Wing geometry")

        C_MAC = mean_aerodynamic_chord(wing_geometry)
        X_AC = 0.25*C_MAC

        current_cg_pos = X_AC -1*(C_MAC*CM)/(np.sin(alpha_rad)*CD + np.cos(alpha_rad)*CL)

        return current_cg_pos


def cg_boundary_twist_analysis(flying_wing: FlyingWing, simulation_id: str, new_analysis_id: str, smoothing= True, extra_input: dict = {}):

    input_data = {
        "Simulation ID": simulation_id,
        "Smoothing:": smoothing
    }

    input_data.update(extra_input)

    simulations = find_simulation(flying_wing, simulation_id)
    rows = []

    for current_simulation in simulations:

        current_cg_pos =  get_cg_for_trim(current_simulation)
        
        rows.append({
            "Alpha": current_simulation.input_data["Alpha"],
            "Twist": current_simulation.input_data["Wing geometry"].current_total_twist,
            "CG Postion": current_cg_pos})

    df = pd.DataFrame(rows)

    output_data = dict()


    alphas = df["Alpha"].unique().tolist()

    upper_bound = []
    lower_bound = []

    for alpha in alphas:

        curr_upper_cg_bound = max(df[df["Alpha"] == alpha]["CG Postion"].unique().tolist())
        upper_bound.append(curr_upper_cg_bound)

        curr_lower_cg_bound = min(df[(df["Alpha"] == alpha)]["CG Postion"].unique().tolist())
        lower_bound.append(curr_lower_cg_bound)

    if smoothing:
        lower_bound = pd.Series(lower_bound).rolling(3, center= True,  min_periods=1).median().rolling(3, center= True,  min_periods=1).mean().to_list()
        upper_bound = pd.Series(upper_bound).rolling(3, center= True,  min_periods=1).median().rolling(3, center= True,  min_periods=1).mean().to_list()

    upper_cg_limit = min(upper_bound)
    lower_cg_limit = max(lower_bound)

    delta_cg = upper_cg_limit - lower_cg_limit


    output_data[f"Delta CG limit"] = delta_cg
    output_data[f"Upper CG limit"] = upper_cg_limit
    output_data[f"Lower CG limit"] = lower_cg_limit
    output_data[f"CG postion"] = lower_cg_limit + delta_cg/2

    output_data[f"Alpha values"]= alphas

    output_data[f"Lower CG boundary"] = lower_bound
    output_data[f"Upper CG boundary"] = upper_bound


    analysis = AnalysisData(new_analysis_id, input_data, output_data)

    flying_wing.analyses.append(analysis)

    return analysis

        








    









