"""
This is the file for yaml operations when reading config files
"""

from ruamel.yaml import YAML
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type, Dict
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq

from rna_squirrel.config.nut_yaml_objects import (
    NutDeclaration,
    NutObject,
    NutContainer,
    NutDatabaseInfo,
    NutStructure,
    NutObjectType
)

class YAMLOperations():
    
    def __init__(self) -> None:
        self.yaml = YAML()
        self.yaml.register_class(NutDeclaration)
        self.yaml.register_class(NutObject)
        self.yaml.register_class(NutContainer)
        self.yaml.register_class(NutDatabaseInfo)
        self.yaml.register_class(NutStructure)
        self.yaml.register_class(NutObjectType)
        self.yml_data: Any = None
        
        #list of classes that is the master list of 
        #custom classes. If it is not here then the 
        #builder will fail if class not found here
        

        
    def open_yml_config(self, file_path:Path):
        """
        Open config yml file used to build the dynamic
        classes
        """
        
        data:Any = None
        
        try:
            with open(file_path, 'r') as file:
                data = self.yaml.load(file)
        except FileExistsError as error:
            raise error

        return data
     