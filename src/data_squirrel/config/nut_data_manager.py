"""
File for managing how data is saved and accessed
"""

from ruamel.yaml import YAML
from pathlib import Path
from typing import Any
import os
import copy
import time

from data_squirrel.config.nut_yaml_objects import (
    String, 
    Integer, 
    FloatingPoint, 
    Dictionary, 
    Empty, 
    NutObjectType,
    ListOfThings,
    Class
)

def init_variable_folder(working_folder:Path, nut_name:str):
    nut_folder_path:Path = working_folder.joinpath(nut_name)
    if os.path.isdir(nut_folder_path) == False:
        try:
            os.mkdir(nut_folder_path)
        except Exception as error:
            raise Exception(f'Unable to create folder {nut_folder_path} Error:{error}')

class YamlDataOperations():
    """
    Class for handeling using yaml files
    for rough quick file access
    """
    
    def __init__(self) -> None:
        self._yaml:YAML = YAML()
        self._yaml.register_class(String)
        self._yaml.register_class(Integer)
        self._yaml.register_class(FloatingPoint)
        self._yaml.register_class(NutObjectType)
        self._yaml.register_class(Dictionary)
        self._yaml.register_class(ListOfThings)
        self._yaml.register_class(Class)
        # self._yaml.register_class(Empty)
        self._dump_yaml:YAML = YAML()
        self._dump_yaml.register_class(String)
        self._dump_yaml.register_class(Integer)
        self._dump_yaml.register_class(FloatingPoint)
        self._dump_yaml.register_class(NutObjectType)
        self._dump_yaml.register_class(Dictionary)
        self._dump_yaml.register_class(ListOfThings)
        self._dump_yaml.register_class(Class)
        
        
    @property
    def yaml(self)->YAML:
        return self._yaml
        
    def save_data(self, data:Any, working_folder:Path, nut_name:str, filename:Path):
        nut_folder_path:Path = working_folder.joinpath(nut_name)
        if os.path.isdir(nut_folder_path) == False:
            raise FileExistsError(f'Variable {nut_name} save path {nut_folder_path} does not exist. Maybe initialize it first?')
        found_data:Any = None
        try:
            self.yaml.dump(data=data,
                       stream=filename)
            time.sleep(1)
            #now do the check             
        except:
            raise Exception('Failed to write data')
        
        try:
            found_data = self._dump_yaml.load(filename)  
            print(found_data)  
            if found_data == data:
                #its good
                self._dump_yaml = YAML()
        except:
            raise Exception('Data save check failed. Found data that differed than original in yaml')       
        
    def read_data(self, working_folder:Path, nut_name:str, filename:Path):
        nut_folder_path:Path = working_folder.joinpath(nut_name)
        if os.path.isdir(nut_folder_path) == False:
            raise FileExistsError(f'Variable {nut_name} save path {nut_folder_path} does not exist. Maybe initialize it first?')
        try:
            return self.yaml.load(filename)
        except:
            raise Exception('Failed to read data')
        