from data.data_classes import FlyingWing


def find_simulation(flying_wing: FlyingWing, simulation_id: str):
    for simu in flying_wing.simulations:
        if simu.id == simulation_id:
            return simu
    

def find_analysis(flying_wing: FlyingWing, analysis_id: str):
    for simu in flying_wing.simulations:
        for analysis in simu.analysis_data:
            if analysis.id == analysis_id:
                return analysis










