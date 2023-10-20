from ruamel.yaml import YAML
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type, Dict
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq


from rna_squirrel.config.dynamic_rna_strand import AtrClass

class NutObjectStatus(Enum):
    """
    The enum for type of object
    """
    CLASS = 'CLASS'
    VALUE = 'VALUE'

class NutObjectType(Enum):
    INTEGER="INTEGER"
    FLOATINGPOINT="FLOATINGPOINT"
    STRING="STRING"
    BOOLEAN="BOOLEAN"

        
@dataclass
class NutObject():
    """
    class for the fields to define
    the attributes of an object.
    Classes and attributes both have specs
    """
    #yaml_tage: ClassVar = '!Spec'
    
    #status:str #ObjectStatus
    #status_enum:ObjectStatus = field(init=False)   
    name: str
    db_name:str = field(init=False)
    
    object_type: NutObjectType
    object_status: NutObjectStatus
    
      
    def __post_init__(self) -> None:
        self.db_name = f'{self.name}_db'

@dataclass
class NutContainer:
    """
    Container for classes
    """
    name:str
    db_name:str = field(init=False)
    
    object_list: List[NutObject]
    
    def __post_init__(self) -> None:
        self.db_name = f'{self.name}_db'
        
@dataclass
class NutStructure():
    """
    Represents the composition of the nut
    """
    name:str
    db_name:str = field(init=False)
    
    nut_main_struct:NutContainer    
    nut_containers_dict:Dict[str,NutContainer]
    
    def __post_init__(self) -> None:
        self.db_name = f'{self.name}_db'

@dataclass
class ClassDeclaration:
    name:str
    

@dataclass
class WalkObjectReturn():
    structure_found_list:List[str]
    struct_order_queue:PriorityQueue
    level:int

