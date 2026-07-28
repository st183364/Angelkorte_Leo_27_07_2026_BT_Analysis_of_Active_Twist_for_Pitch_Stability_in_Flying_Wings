from __future__ import annotations
from dataclasses import dataclass
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Iterable
from geometry.wing_geometry import WingGeometry
from pandas import DataFrame



@dataclass
class SolverOutputData:
    """
    Contains the output of a solver.
    
    Data:
        - output_data: Everything the solver returns(At least aero coefficents like CL, CM and CD).
    """
    output_data: Dict[str, Any]

@dataclass
class MetaData:
    """
    Contains the meta data of a simulation.

    Data:
        - user: The login name of the user.
        - solver: The solver used by the simulaiton.
        - solver_version: Version of the solver.
        - time_stamp: Creation time of the metadata file.
        - simulation_type: The type of simulation.
    """
    user: str
    solver: str
    solver_version: str
    time_stamp: str
    simulation_type: str


@dataclass
class Analysis:
    id: str
    simulation: Simulation


@dataclass
class CGBoundaryAnalysis(Analysis):
    """
    Contains the result of a cg boundary analysis which is based on the trim condition.

    Data:
        - alpha_values: All of the alpha values used in the simulation and analysis.
        - epsilon_values: All of the epsilon values used in the simulation and analysis.
        - velocity: Airflow velocity for the simulation and analysis.

        - cg_upper_boundary: The upper cg boundary curve of the cg postion (The max for each alpha value regardless of twist).
        - cg_lower_boundary: The lower cg boundary curve of the cg postion (The min for each alpha value regardless of twist).
        - cg_max: The max value for a constant cg postion at which trim can be satified for every alpha.
        - cg_min: The min value for a constant cg postion at which trim can be satified for every alpha.
        - cg_pos_array: An array of cg postion for each alpha and twist value.
    """
    alpha_values: Iterable
    epsilon_values: Iterable    
    velocity: float

    cg_upper_boundary: Iterable
    cg_lower_boundary: Iterable
    cg_max: float
    cg_delta: float
    cg_min: float
    cg_pos_array: List[List[float]]


@dataclass
class Simulation:
    id: str
    flying_wing: FlyingWing
    meta_data: MetaData
    analysis_data: List[Analysis]

@dataclass
class AlphaEpsilonSimulation(Simulation):
    """
    Contains the output data of an alpha epsilon simulation.

    Data:
        - meta_data: Meta data of the simulation.
        - alpha_values: All of the alpha values used in the simulation.
        - epsilon_values: All of the epsilon values used in the simulation.
        - velocity: Airflow velocity for the simulation.
        - solver_input_data: The input data given to the solver.
        - alpha_epsilon_array: Array of SolverOutputData obj based on alpha[epsilon[solver_output]].
    """
    alpha_values: Iterable
    epsilon_values: Iterable
    velocity: float
    solver_input_data: Dict[str, Any]
    alpha_epsilon_array: List[List[SolverOutputData]]

@dataclass
class FlyingWing:
    id: str
    wing_geometry: WingGeometry
    simulations: List[Simulation]