"""
File for defining the operations required to save and retrieve
data nut squirrel objects using pickeling
"""

import pickle
from ruamel.yaml import YAML
from pathlib import Path
from typing import Any, List
import os
import copy
import time
from datetime import datetime
import hashlib

from data_squirrel.config.nut_data_manager import (
    BasicDataOperations,
    DataPathDetails
    )

class PickelDataOperations(BasicDataOperations):
    
    def __init__(self) -> None:
        pass
    
    def save_data(self, data:Any, working_folder:Path, nut_name:str, filename:Path):
        data_path:DataPathDetails = self.generate_data_path_details(working_folder=working_folder,
                                                                    nut_name=nut_name,
                                                                    filename=filename)

        if os.path.isdir(data_path.working_folder) == False:
            raise FileExistsError(f'Variable {nut_name} save path {data_path.working_folder} does not exist. Maybe initialize it first?')
        found_data:Any = None
        # pickle_filename:Path = nut_folder_path.joinpath(filename)
        try:
            with data_path.target_path.open('wb') as file: 
                pickle.dump(data, file)
        except:
            raise Exception(f'Error while writing out {nut_name} to {data_path.target_path.as_posix()}')
    
    def read_data(self, working_folder:Path, nut_name:str, filename:Path):
        pass