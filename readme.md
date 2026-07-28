## Directory Structure
```text
.
├── Case_Study/
│   ├── bat_cg_pos_analysis.ipynb
│   ├── bat_p_controller.ipynb
│   ├── data/
│   └── VTFW_Lab4/
├── Parametric_Study/
│   ├── bat_symmetric_airfoils.ipynb
│   ├── bat_cambered_airfoils.ipynb
│   ├── bat_reflexed_airfoils.ipynb
│   ├── data/
│   └── VTFW_Lab3/
├── requirements.txt
├── README.md
└── Analysis_of_Active_Twist_for_Pitch_Stability_in_Flying_Wings.pdf
```

### `Case_Study/`

Contains all files required to reproduce the detailed case study of the two selected flying-wing configurations.
```text
Case_Study/
├── bat_cg_pos_analysis.ipynb
├── bat_p_controller.ipynb
├── data/
└── VTFW_Lab4/
```

- **`bat_cg_pos_analysis.ipynb`** – Performs the detailed center of gravity (CG) position limit analysis for the selected wing configurations.
- **`bat_p_controller.ipynb`** – Evaluates the static proportional twist controller and reproduces the pitching moment analyses presented in the thesis.
- **`data/`** – Contains the serialized wing models (`.pkl` files) used throughout the case study.
- **`VTFW_Lab4/`** – Python implementation used by the case study notebooks. It contains the same core functionality as the parametric study framework together with the additional controller implementation required for the case study.

### `Parametric_Study/`

Contains all files required to reproduce the parametric study presented in the thesis.

```text
Parametric_Study/
├── bat_symmetric_airfoils.ipynb
├── bat_cambered_airfoils.ipynb
├── bat_reflexed_airfoils.ipynb
├── data/
└── VTFW_Lab3/
```

- **`bat_symmetric_airfoils.ipynb`** – Parametric study for symmetric NACA airfoils.
- **`bat_cambered_airfoils.ipynb`** – Parametric study for cambered NACA airfoils.
- **`bat_reflexed_airfoils.ipynb`** – Parametric study for reflexed NACA airfoils.
- **`data/`** – Contains serialized simulation results (`.pkl` files) generated during the parametric study. These files are reused by the notebooks to avoid repeating computationally expensive VLM simulations.
- **`VTFW_Lab3/`** – Python implementation of the analysis framework used by the notebooks. It contains modules for wing geometry generation, AeroSandbox interfaces, CG position limit analysis, data handling, plotting, and other helper utilities.

### `requirements.txt`

Lists the Python packages required to execute the notebooks.

### `README.md`

Contains installation instructions and an overview of the project.

## Installation

This project was tested with Python 3.13. 

> **Warning:** Running the notebooks with **Python 3.14** causes the Jupyter kernel to crash due to dependency incompatibilities. To ensure successful execution, please use **Python 3.13**.

1. Ensure that Python is installed on your system.
2. Open the project folder in your preferred IDE or open a terminal in the project directory.
3. Install the required Python libraries by running:

```bash
pip install -r requirements.txt
```

## Implementation Notes

The submitted notebooks reproduce the methodology presented in Sections 4.5 and 4.6 of the thesis.

### Parametric Study

The parametric study is divided into three notebooks, each corresponding to one airfoil group:

- `bat_symmetric_airfoils.ipynb`
- `bat_cambered_airfoils.ipynb`
- `bat_reflexed_airfoils.ipynb`

Each notebook performs the following workflow:

1. Generate trapezoidal flying wing geometries from the specified wing parameters.
2. Run AeroSandbox Vortex Lattice Method (VLM) simulations for all combinations of angle of attack and wing twist.
3. Apply the center of gravity (CG) position limit analysis to determine stabilizable CG ranges.
4. Store the calculated wing objects and simulation results as serialized `.pkl` files.
5. Generate all figures, statistical evaluations, and tables presented in the thesis.

If previously generated data already is not deleted in the corresponding data directories, it will be reused instead of recomputing the aerodynamic simulations.

### Case Study

The case study consists of two notebooks:

- `bat_cg_pos_analysis.ipynb`
- `bat_p_controller.ipynb`

The workflow is:

1. Generate the selected wing configurations.
2. Perform detailed CG position limit analyses.
3. Evaluate a static proportional twist controller using AeroSandbox VLM simulations.
4. Generate the CG boundary plots and pitching moment curves presented in the thesis.

Unlike the CG position analysis notebook, the controller notebook performs new VLM simulations for each evaluated angle of attack.

### Generated Data

Simulation results are stored as serialized Python (`.pkl`) objects. These files contain:

- Wing geometry
- Aerodynamic simulation results
- CG position limit analysis results

## Computational Time

The aerodynamic simulations performed in the parametric study are computationally intensive. On the system used for this thesis, the approximate execution times are:

- **Symmetric airfoils:** ~2 hours
- **Cambered airfoils:** ~4 hours
- **Reflexed airfoils:** ~4 hours

The total computation time can be reduced if reproducing the complete data set is not required. This can be achieved in two ways:

- **Skip the remaining simulations:** The simulation process may be stopped manually once a sufficient number of configurations has been evaluated. The analysis sections of the notebooks can then be executed independently using the simulation data that has already been generated.
- **Reduce the parameter space:** The number of simulated configurations can be reduced by modifying the lists of investigated wing shape parameters (e.g., aspect ratio, taper ratio, or sweep angle) and/or by reducing the number of analyzed airfoils.




























