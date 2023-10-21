from ruamel.yaml import YAML
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type, Dict
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq

import sys
import ruamel.yaml



from rna_squirrel.config.dynamic_rna_strand import AtrClass

@dataclass
class NutDeclaration:
    name:str


class NutObjectType(Enum):
    INTEGER="INTEGER"
    FLOATINGPOINT="FLOATINGPOINT"
    STRING="STRING"
    BOOLEAN="BOOLEAN"
    DICTIONARY="DICTIONARY"
    CONTAINER="CONTAINER"
    
    @classmethod
    def from_yaml(cls, loader, node):
        test = cls(node.value)
        return test

        
@dataclass
class NutObject:
    """
    class for the fields to define
    the attributes of an object.
    Classes and attributes both have specs
    """

    #yaml_tage: ClassVar = '!Spec'
    
    #status:str #ObjectStatus
    #status_enum:ObjectStatus = field(init=False)   
    name: str
    # db_name:str = field(init=False)
    
    object_type: NutObjectType
    object_info: Any
      
    def __post_init__(self) -> None:
        self.db_name = f'{self.name}_db'
    
    # def from_yaml(self, contructor, node):
    #     return self(node.name, node.object_type, node.object_info)


@dataclass
class NutContainer:
    """
    Container for classes
    """
    name:str
    db_name:str = field(init=False)
    
    object_list: List[NutObject]
    #object_dict: Dict[str, NutObject]
    
    def __post_init__(self) -> None:
        self.db_name = f'{self.name}_db'

@dataclass
class NutDatabaseInfo:
    db_name:str
     
@dataclass
class NutStructure:
    """
    Represents the composition of the nut
    """
    db_info:str
    #db_name:str = field(init=False)
    # nut_container_declarations:List[NutDeclaration]
    
    # nut_main_struct:NutContainer    
    # nut_containers_list:List[NutContainer]
    
    # #def __post_init__(self) -> None:
    #    self.db_name = f'{self.name}_db'




