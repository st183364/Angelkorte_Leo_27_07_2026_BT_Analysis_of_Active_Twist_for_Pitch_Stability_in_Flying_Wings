from __future__ import annotations
from dataclasses import dataclass
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Iterable
from geometry.wing_geometry import WingGeometry
from pandas import DataFrame

@dataclass
class MetaData:
    """
    Contains the meta data of a simulation.

    Data:
        - user: The login name of the user.
        - solver: The solver used by the simulaiton.
        - version: Version of VTFW_LAB.
        - time_stamp: Creation time of the metadata file.
    """
    user: str
    solver: str
    version = "4.0"
    time_stamp: str
    extra_data: Dict

@dataclass
class AnalysisData:
    id: str
    input_data: Dict
    output_data: Dict

@dataclass
class SimulationData:
    """
    Output data:
        - 'F_w' : an [Drag, Side, Lift] list of forces in wind axes [N]
        - 'M_w' : an [Roll, Pitch, Yaw] list of moments about wind axes [Nm]

        - 'F_b' : an [x, y, z] list of forces in body axes [N]
        - 'M_b' : an [x, y, z] list of moments about body axes [Nm]

        - 'L' : the lift force [N]. Definitionally, this is in wind axes.
        - 'Y' : the side force [N]. This is in wind axes.
        - 'D' : the drag force [N]. Definitionally, this is in wind axes.

        - 'CL', the lift coefficient [-]. Definitionally, this is in wind axes.
        - 'CY', the sideforce coefficient [-]. This is in wind axes.
        - 'CD', the drag coefficient [-]. Definitionally, this is in wind axes.
        - 'Cm', the pitching coefficient [-], this is in wind axes

    """
    id: str
    meta_data: MetaData
    input_data: Dict
    output_data: Dict



@dataclass
class FlyingWing:
    id: str
    wing_geometry: WingGeometry
    simulations: List[SimulationData]
    analyses: List[AnalysisData]

