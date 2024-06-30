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
    BasicDataOperations
    )

class PickelDataOperations(BasicDataOperations):
    
    def __init__(self) -> None:
        pass
    
    def save_data(self, data:Any, working_folder:Path, nut_name:str, filename:Path):
        nut_folder_path:Path = working_folder.joinpath(nut_name)
        if os.path.isdir(nut_folder_path) == False:
            raise FileExistsError(f'Variable {nut_name} save path {nut_folder_path} does not exist. Maybe initialize it first?')
        found_data:Any = None
        pickle_filename:Path = nut_folder_path.joinpath(filename)
        try:
            with pickle_filename.open('wb') as file: 
                pickle.dump(data, file)
        except:
            raise Exception(f'Error while writing out {nut_name} to {pickle_filename.as_posix()}')
    
    def read_data(self, working_folder:Path, nut_name:str, filename:Path):
        pass