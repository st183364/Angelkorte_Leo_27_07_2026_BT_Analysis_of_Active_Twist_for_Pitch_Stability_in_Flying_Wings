import aerosandbox as asb
import aerosandbox.numpy as np
from tqdm import tqdm
import pandas as pd


from geometry.wing_geometry import WingGeometry
from data.data_classes import SolverOutputData
from utils.aerosandbox_interface import convert_wing_2aerosandbox_wing, convert_wing_2aerosandbox_wing_tw_2ax


def abs_vortex_lattice_method(wing: WingGeometry, velocity: float, alpha: float, beta: float, number_sections: int, chordwise_panel_number: int, spanwise_panel_number: int):

    airplane = asb.Airplane(name="plane", wings=[convert_wing_2aerosandbox_wing_tw_2ax(wing, number_sections)])
    #airplane.draw()
    op_point = asb.OperatingPoint(velocity= velocity, alpha= alpha, beta= beta)
    vlm = asb.VortexLatticeMethod(airplane=airplane, op_point=op_point, chordwise_resolution= chordwise_panel_number, spanwise_resolution= spanwise_panel_number)
    vml_results = vlm.run()
    output_data = {}
    output_data.update(vml_results)

    return SolverOutputData(output_data)













