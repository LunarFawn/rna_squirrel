"""
This is the file for yaml operations when reading config files
"""

from ruamel.yaml import YAML
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field


from rna_squirrel.config.dynamic_rna_strand import AtrClass


@dataclass
class Integer:
    name:str
    python_type:Any = int
    string_castable:bool = True

@dataclass
class FloatingPoint:
    name:str
    python_type:Any = float
    string_castable:bool = True

@dataclass
class String:
    name:str
    python_type:Any = str
    string_castable:bool = True

@dataclass
class Dictionary:
    name:str
    key: str
    value: str

@dataclass
class CustomList:
    name: str
    list_type: str
        

@dataclass
class ClassType:
    name:str
    class_type:str

@dataclass
class ClassDeclaration:
    name:str

class ObjectStatus(Enum):
    """
    The enum for type of object
    """
    CLASS = 'CLASS'
    VALUE = 'VALUE'

@dataclass
class ObjectSpec:
    """
    class for the fields to define
    the attributes of an object.
    Classes and attributes both have specs
    """
    #yaml_tage: ClassVar = '!Spec'
    name:str
    
    status:str #ObjectStatus
    status_enum:ObjectStatus = field(init=False)   
    
    object_type: str # Any
          
    def __post_init__(self) -> None:
        self.status_enum = ObjectStatus(self.status)

@dataclass
class ValueSpec:
    """
    Class for getting the configuration
    of the attributes that are values 
    so that the code can build the type
    """
    type_name: str
    


@dataclass
class ParentSpecs():
    pass

class YAMLOperations():
    
    def __init__(self) -> None:
        self.yaml = YAML()
        self.yaml.register_class(ObjectSpec)
        self.yaml.register_class(String)
        self.yaml.register_class(ClassAttribute)
        self.yaml.register_class(ClassDeclaration)
        self.yml_data: Any = None
        self.classes_list: List = []
        self.nut_attributes: List[ObjectSpec] = []
        
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
            
    def parse_system_settings(self, data:Any):
        """
        Parse the raw data from the yml file
        to populate the main system catagories
        required for generation and population
        of python files
        """
        
        #first get the list of classes
        classes = data['OBJECT_CLASSES']
        
    def get_object_list(self, data:Any):
        pass
    
    def read_object_attributes(self):
        pass
