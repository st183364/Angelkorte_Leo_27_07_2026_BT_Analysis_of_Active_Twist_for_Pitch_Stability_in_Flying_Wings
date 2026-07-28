import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
from geometry.airfoil import Airfoil
from geometry.wing_geometry import WingGeometry
from data.data_classes import CGBoundaryAnalysis
from scipy.ndimage import median_filter

def plot_airfoil(airfoil: Airfoil, num: int = 100):
    sur_points = airfoil.get_lin_dist_surface_points(num)
    plt.plot([p[1] for p in sur_points], [p[2] for p in sur_points])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(airfoil.name)
    plt.axis("equal")
    plt.grid(True)
    plt.show()

def plot_wing_planform(wing: WingGeometry):
    y_values = np.linspace(-wing.half_span, wing.half_span, 1000)

    plt.plot(y_values, np.array([wing.leading_edge(y)[0] for y in y_values]), color = "blue")
    plt.plot(y_values, np.array([wing.leading_edge(y) [0] for y in y_values]) + np.array([wing.chord_len(y) for y in y_values]), color = "blue")

    plt.xlabel("Y-Axsis")
    plt.ylabel("X-Axsis")
    plt.title("Wing planform")
    plt.axis("equal")
    plt.grid(True)
    plt.show()

def plot_wing_planform_with_cg(wing: WingGeometry, cg_min: float, cg_max: float, cg_delta: float):
    y_values = np.linspace(-wing.half_span, wing.half_span, 1000)

    plt.plot(y_values, np.array([wing.leading_edge(y)[0] for y in y_values]), color = "blue")
    plt.plot(y_values, np.array([wing.leading_edge(y) [0] for y in y_values]) + np.array([wing.chord_len(y) for y in y_values]), color = "blue")

    plt.plot(y_values, np.ones_like(y_values)*cg_min, "--",color = "red")
    plt.plot(y_values, np.ones_like(y_values)*cg_max, "--",color = "red")
    plt.plot(y_values, np.ones_like(y_values)*(cg_min + cg_delta/2), "--",color = "green")

    plt.xlabel("Y-Axsis")
    plt.ylabel("X-Axsis")
    plt.title("Wing planform")
    plt.axis("equal")
    plt.grid(True)
    plt.show()

def plot_cg_limit_analysis(analysis_data: CGBoundaryAnalysis):

    # Boundary Curves
    plt.plot(list(analysis_data.alpha_values), list(analysis_data.cg_upper_boundary), 'o-', markersize=6, color="red")
    plt.plot(list(analysis_data.alpha_values), list(analysis_data.cg_lower_boundary), 'o-', markersize=6, color="red")

    # Const CG values
    plt.plot(list(analysis_data.alpha_values), np.ones_like(analysis_data.alpha_values)*analysis_data.cg_max, '-', markersize=6, color="green")    
    plt.plot(list(analysis_data.alpha_values), np.ones_like(analysis_data.alpha_values)*analysis_data.cg_min, '-', markersize=6, color="green")

    plt.xlabel("alpha")
    plt.ylabel("x center of gravity")
    plt.title("Center of gravity boundary analysis")
    plt.grid(True)
    plt.show()



