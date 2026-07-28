from abc import ABC
from typing import Tuple, List


class Airfoil(ABC):
    """
    Abstract Class for airfoils
    """
    name: str
    def get_lin_dist_surface_points(self, number_points: int) -> List[Tuple]:
        """
        Returns number_points distributed linear across the chord of the foil. 
        """
        return []
        