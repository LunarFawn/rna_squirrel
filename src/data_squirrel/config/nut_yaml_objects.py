from ruamel.yaml import YAML
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type, Dict
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq
import attrs

import sys
import ruamel.yaml

class AtrClass(Enum):
    PARENT = "PARENT"
    CHILD = "CHILD"
    NUT="NUT"
    NONE = "NONE"



@dataclass
class NutDeclaration:
    name:str
  

class NutObjectType(Enum):
    INTEGER="int"
    FLOATINGPOINT="float"
    STRING="str"
    BOOLEAN="bool"
    DICTIONARY="Dict"
    CONTAINER="CONTAINER"
    VALUE="VALUE"
    
    @classmethod
    def from_yaml(cls, loader, node):
        return NutObjectType[node.value]

        
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
        new_list: List[NutObject] = []
        for item in self.object_list:
            new_list.append(item)
        self.object_list = new_list
        

@dataclass
class NutContainerDefinitions:
    """
    Holds the definitions for all the containers
    that were declared in the NUT. If it was not
    declared in NutStructure then it will be ignored
    here and by system, but still be loaded (for now)
    """
    nut_containers_definitions:List[NutContainer]
    definition_dict:Dict[str, NutContainer] = field(init=False)
    
    def __post_init__(self) -> None:
        new_list: List[NutContainer] = []
        self.definition_dict = {}
        for item in self.nut_containers_definitions:
            new_list.append(item)
            #also while here build the dict
            self.definition_dict[item.name] = item
        self.nut_containers_definitions = new_list
        
        
    
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
    nut_container_declarations:List[NutDeclaration]
    nut_containers:List[str] = field(init=False)
    
    nut_main_struct:NutContainer    
    #nut_containers_list:List[NutContainer]
    
    def __post_init__(self) -> None:
        new_list: List[NutDeclaration] = []
        self.nut_containers = []
        for item in self.nut_container_declarations:
            new_list.append(item)
            #now build the nut containers name
            self.nut_containers.append(item.name)
        self.nut_container_declarations = new_list


@attrs.define(kw_only=True)
class GenericAttribute():
    atr_class:AtrClass = attrs.field()
    atr_type:Type = None
    #atr_default_value:Any = None
    #attributes:Enum = field()
    attribute:str = attrs.field()


class ValuePacket(GenericAttribute):
      
    def __init__(self, name:str, value:Any, parent:str, type:Any) -> None:
        super().__init__(atr_class=AtrClass.CHILD,
                         atr_type=type,
                         attribute=name)
        self._parent:str = parent
        self._value:Any = value
        self._address_list:List[str] = []  
    
    @property
    def parent(self)->str:
        return self._parent
    
    @property 
    def value(self)->Any:
        return self._value 
    
    @property
    def address_list(self):
        return self._address_list 
    
    address_list:List[str]
    
@dataclass
class Empty():
    value:Any = field(init=False)

@dataclass
class Integer:
    value:int
    
        
@dataclass
class FloatingPoint:
    value:float
        
@dataclass
class String:
    value:str

        
@dataclass
class Dictionary:
    value:Dict[Any,Any]



