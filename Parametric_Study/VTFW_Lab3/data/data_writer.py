import os 
from datetime import datetime
import tempfile
import dill 
import getpass
import re
from data.data_classes import AlphaEpsilonSimulation, MetaData, CGBoundaryAnalysis, FlyingWing

def get_data_dir(name: str, dir= tempfile.gettempdir()):
    data_dir = os.path.join(dir, f"{name}")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    return data_dir

def write_flying_wing(simu_data_dir: str, wing: FlyingWing):
    with open(os.path.join(simu_data_dir, f"flying_wing_id{wing.id}.pkl"), "wb") as file:
        dill.dump(wing, file)










