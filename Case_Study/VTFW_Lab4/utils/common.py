from data.data_classes import FlyingWing, SimulationData, AnalysisData
from typing import List


def find_simulation(flying_wing: FlyingWing, simulation_id: str) -> List[SimulationData]:
    simulations = []
    for current_simulation in flying_wing.simulations:
        if current_simulation.id == simulation_id:
            simulations.append(current_simulation)
    return simulations
    
def remove_simulation(flying_wing: FlyingWing, simulation_id: str):
    for simu in flying_wing.simulations:
        if simu.id == simulation_id:
            flying_wing.simulations.remove(simu)

def change_simulation_id(flying_wing: FlyingWing, old_simulation_id: str, new_simulation_id: str):
    for current_simulation in flying_wing.simulations:
        if current_simulation.id == old_simulation_id:
            current_simulation.id = new_simulation_id
 
def find_analysis(flying_wing: FlyingWing, analysis_id: str) -> List[AnalysisData]:
    analyses = []
    for current_analysis in flying_wing.analyses:
        if current_analysis.id == analysis_id:
            analyses.append(current_analysis)
    return analyses

def remove_analysis(flying_wing: FlyingWing, analysis_id: str):
    for current_analysis in flying_wing.analyses:
        if current_analysis.id == analysis_id:
            flying_wing.simulations.remove(current_analysis)

def change_analysis_id(flying_wing: FlyingWing, old_analysis_id: str, new_analysis_id: str):
    for current_analysis in flying_wing.analyses:
        if current_analysis.id == old_analysis_id:
            current_analysis.id = new_analysis_id

def print_flying_wing_data(flying_wing: FlyingWing):
    print(f"Fyling wing :   ID: {flying_wing.id}\n")
    print(f"Wing :   ID: {flying_wing.wing_geometry.id}\n")

    print(f"Simulations: \n")

    for i, current_simulation in enumerate(flying_wing.simulations):
        print(f"    - {i}: ID: {current_simulation.id}")
        
    print(f"Analyses: \n")

    for i, current_analysis in enumerate(flying_wing.analyses):
        print(f"    - {i}: ID: {current_analysis.id}")

    print()

def print_data_dict(data_dict: dict):
    for key in data_dict.keys():
        print(f"{key}: {data_dict[key]}")
    print()


