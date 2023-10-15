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
from queue import PriorityQueue


from rna_squirrel.config.dynamic_rna_strand import AtrClass

class ObjectStatus(Enum):
    """
    The enum for type of object
    """
    CLASS = 'CLASS'
    VALUE = 'VALUE'

@dataclass
class CLASS:
    status:ObjectStatus = ObjectStatus.CLASS

@dataclass
class VALUE:
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class Integer:
    name:str
    python_type:Any = int
    string_castable:bool = True
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class FloatingPoint:
    name:str
    python_type:Any = float
    string_castable:bool = True
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class String():
    name:str
    python_type:Any = str
    string_castable:bool = True
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class Dictionary:
    name:str
    key: str
    value: str
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class ClassType:
    name:str
    class_type:str
    status:ObjectStatus = ObjectStatus.CLASS

@dataclass
class CustomList:
    name: str
    list_type: str
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class ClassDeclaration:
    name:str



@dataclass
class Objects:
    """
    class for the fields to define
    the attributes of an object.
    Classes and attributes both have specs
    """
    #yaml_tage: ClassVar = '!Spec'
    #name:str
    
    #status:str #ObjectStatus
    #status_enum:ObjectStatus = field(init=False)   
    object_list: Any 
          
    #def __post_init__(self) -> None:
    #    self.status_enum = ObjectStatus(self.status)

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
        self.yaml.register_class(Objects)
        self.yaml.register_class(String)
        self.yaml.register_class(ClassType)
        self.yaml.register_class(ClassDeclaration)
        self.yml_data: Any = None
        
        #list of classes that is the master list of 
        #custom classes. If it is not here then the 
        #builder will fail if class not found here
        self.classes_list: List[str] = []
        
        self.nut_attributes: List[Objects] = []
        

    def run_python_build(self, yaml_filepath:Path):
        """
        Entry point ot build python api's and
        backend config files
        """
        
        #first need to open the yaml file and grab the
        #data
        data = self.open_yml_config(file_path=yaml_filepath)
        
        #now parse the declarations so we know what classes we 
        #have to work with
        declared_classes = self.get_declarations(yaml_data=data)
        
        #now that we have list lets populate the global stuff
        #we care about
        for declaration in declared_classes:
            self.classes_list.append(declaration.name)
            
        #now get NUT objects and build out from there

    def build_class_queue(self):
        """
        Build the queue for all the classes
        so that they get built in the API in the 
        right order
        """
        pass
    
    def build_class(self, yaml_data:Any):
        """
        build class entry to append to the API as well
        """
        pass
        
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
     
    
    def get_declarations(self, yaml_data:Any):
        """
        strep through and parse the declarations
        to build out the list of classes
        and what the interpreter is to expect as
        it is pretty dumb right now
        """
        
        declared_classes:List[ClassDeclaration] = []
        
        #generate list of classes first from yaml
        list_of_declarations: List[Any] = yaml_data["DECLARATIONS"]
        for declaration in list_of_declarations:
            declared_classes.append(declaration)
        

        
        return declared_classes
        
    def parse_system_settings(self, data:Any):
        """
        Parse the raw data from the yml file
        to populate the main system catagories
        required for generation and population
        of python files
        """
        
        #first get the list of classes
        classes = data['OBJECT_CLASSES']
        
    def get_object_list(self, yaml_data:Any, class_name:str):
        class_objects:List[ClassType] = []
        value_objects: List[Any] = []
        object_count:int = int(yaml_data[class_name]["object_count"]["count"])
        raw_object_list = yaml_data[class_name]["objects"]
        for object in raw_object_list:
            if isinstance(object, ClassType) is True:
                class_objects.append(object)
            else:
                value_objects.append(object)
        return class_objects, value_objects
    
    def read_object_attributes(self):
        pass
