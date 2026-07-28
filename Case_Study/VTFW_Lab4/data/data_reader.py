import os
import dill
from typing import List
from data.data_classes import FlyingWing


def read_flying_wing(path: str) -> FlyingWing:
    if "flying_wing" in path:
        with open(path, "rb") as file:
            meta_data = dill.load(file)
            return meta_data

def read_list_of_flying_wings(path: str) -> List[FlyingWing]:
    flying_wings = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file_name in filenames:
            if "flying_wing" in file_name:
                flying_wings.append(read_flying_wing(os.path.join(dirpath, file_name)))

    return flying_wings








