from data.data_classes import AlphaEpsilonSimulation, CGBoundaryAnalysis, FlyingWing
from geometry.wing_geometry import mean_aerodynamic_chord, wing_aerodynamic_center
import numpy as np
from utils.common import find_simulation

def cg_boundary_analysis(flying_wing: FlyingWing, simulation_id: str, new_analysis_id: str = None, singularity_tolerance: float = 1e-10):
    alpha_eps_simu = find_simulation(flying_wing, simulation_id)
    wing = flying_wing.wing_geometry
    mac = mean_aerodynamic_chord(wing)

    cg_pos_array = []
    max_cg_positions = []
    min_cg_positions = []

    for alpha, eps_solver_outputs in zip(alpha_eps_simu.alpha_values, alpha_eps_simu.alpha_epsilon_array):
        current_cg_positions = []
        finite_cg_positions = []
        row_is_unconstrained = False

        alpha_rad = np.deg2rad(alpha)

        for epsilon, solver_output in zip(alpha_eps_simu.epsilon_values, eps_solver_outputs):
            if hasattr(solver_output, "output_data"):
                solver_output = solver_output.output_data

            CL = solver_output.get("CL")
            CD = solver_output.get("CD")
            CM = solver_output.get("Cm")

            if CM is None:
                CM = solver_output.get("CMy")

            if CL is None or CD is None or CM is None:
                raise KeyError(f"Missing aerodynamic coefficient at alpha={alpha}, epsilon={epsilon}: CL={CL}, CD={CD}, CM={CM}")

            CL = float(CL)
            CD = float(CD)
            CM = float(CM)

            if not np.all(np.isfinite([CL, CD, CM])):
                raise ValueError(f"Non-finite coefficient at alpha={alpha}, epsilon={epsilon}: CL={CL}, CD={CD}, CM={CM}")

            force_coefficient = (np.sin(alpha_rad) * CD+ np.cos(alpha_rad) * CL)

            denominator_is_zero = np.isclose(force_coefficient, 0.0, atol=singularity_tolerance, rtol=0.0)
            moment_is_zero = np.isclose(CM, 0.0, atol=singularity_tolerance, rtol=0.0)

            if denominator_is_zero:
                # 0 / 0:
                if moment_is_zero:
                    row_is_unconstrained = True

                # CM != 0 no finite CG solution
                current_cg_positions.append(np.nan)
                continue

            current_cg_pos = -mac * CM / force_coefficient

            if not np.isfinite(current_cg_pos):
                raise ValueError(f"Non-finite CG result at alpha={alpha}, epsilon={epsilon}")

            current_cg_positions.append(current_cg_pos)
            finite_cg_positions.append(current_cg_pos)

        cg_pos_array.append(current_cg_positions)

        if row_is_unconstrained:
            max_cg_positions.append(np.nan)
            min_cg_positions.append(np.nan)

        elif finite_cg_positions:
            max_cg_positions.append(max(finite_cg_positions))
            min_cg_positions.append(min(finite_cg_positions))

        else:
            raise ValueError(f"No finite CG solution exists for alpha={alpha}.")

    if np.all(np.isnan(max_cg_positions)):
        raise ValueError("No alpha value provides a finite CG boundary.")

    cg_max = float(np.nanmin(max_cg_positions))
    cg_min = float(np.nanmax(min_cg_positions))
    cg_delta = cg_max - cg_min

    if not new_analysis_id:
        new_analysis_id = (f"CG_Boundary_Analysis_{len(alpha_eps_simu.analysis_data)}")

    analysis = CGBoundaryAnalysis(
        new_analysis_id,
        alpha_eps_simu,
        alpha_eps_simu.alpha_values,
        alpha_eps_simu.epsilon_values,
        alpha_eps_simu.velocity,
        max_cg_positions,
        min_cg_positions,
        cg_max,
        cg_delta,
        cg_min,
        cg_pos_array,
    )

    alpha_eps_simu.analysis_data.append(analysis)

    return analysis


