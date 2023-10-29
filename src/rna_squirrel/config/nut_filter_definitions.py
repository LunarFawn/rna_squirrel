"""
File to hold teh default classes for manipulating
data that goes throught the setter and getter
of the dynamic backend
"""
from typing import Any, Dict, List
from enum import Enum
import heapq
from pathlib import Path
from dataclasses import dataclass, field

from rna_squirrel.config.nut_yaml_objects import AtrClass, ValuePacket, GenericAttribute

class ValueFlow(Enum):
    OUTBOUND="OUTBOUND"
    INBOUND="INBOUND"
    BOTH="BOTH"

@dataclass
class AddressInfo():
    address_list: List[str]
    working_folder:Path 
    address_string:str = field(init=False)
    address_file_path: Path = field(init=False)
    
    def __post_init__(self) -> None:
        self.address_string = f'{"_".join(self.address_list)}.yaml'
        self.address_file_path = self.working_folder.joinpath(self.address_string)
        
        
class NutFilterDefinitions():

    def __init__(self, working_dir:Path) -> None:
        self.working_dir:Path = working_dir
    
    def filter(self, parent:Any, attr_name:str, value:Any, flow_direction:ValueFlow):
        new_value:Any = value
        
        routing:NutAdressing = NutAdressing()
        jump_list: List[str] = routing.get_attr_address(parent_attr=parent,
                                 name=attr_name)
        address_info:AddressInfo = AddressInfo(address_list=jump_list,
                                               working_folder=self.working_dir)
        #heapq.heapify(jump_list)
        
        if flow_direction == ValueFlow.OUTBOUND:
            new_value = self.filter_out_flow(value=new_value,
                                             address=address_info)
        elif flow_direction == ValueFlow.INBOUND:
            new_value = self.filter_in_flow(value=new_value)
        
        
        return new_value
        
    def filter_both_flow(self, value:Any):
        new_value:Any = value
        return new_value
    
    def filter_out_flow(self, value:Any, address:AddressInfo):
        """
        This is the 
        """

        new_value:Any = value
        if isinstance(value, ValuePacket) == True:
            #this is a value and not a parent custom attribe
            packet:ValuePacket = value
            new_value = packet.value
            if type(packet.value) == str:
                
                #now save it to the yaml at the file target
                
                new_value = f'{new_value}_from_db'
        else:
            #it is a parent struct
            pass     
       
        return new_value
    
    def filter_in_flow(self,  value:Any):
        """
        This is the 
        """
        new_value:Any = value
        
        if type(value) == str:
                new_value = f'{value}_returned'
            
        return new_value

class NutAdvancedFilterRules():
    """
    Class to hold all the rules for types
    """

    def __init__(self) -> None:
        pass

    def process_dict(self, dict_container:Dict):
        pass

class NutAdressing():
    """
    Class to handle the addressing and routing
    of the attributes and the data
    """
    
    def __init__(self) -> None:
        pass
    
    def get_attr_address(self,name:str, parent_attr:Any):
        """
        get the attribute parent
        """
        order:int = 1
        jump_list:List[tuple] = []
        
        #jump_list.append((order,name)) 
        jump_list.append(name)
        
        while hasattr(parent_attr, 'parent') == True:
            order += 1
            if getattr(parent_attr, 'atr_class') != AtrClass.NUT:
                parent_name = parent_attr.attribute
                #jump_list.append((order, parent_name))
                jump_list.append(parent_name)                 
            parent_attr = getattr(parent_attr, 'parent')
        
        if getattr(parent_attr, 'atr_class') == AtrClass.NUT:
            order += 1
            parent_name = parent_attr.var_name
            #jump_list.append((order, parent_name))
            jump_list.append(parent_name)  
        else:
            raise Exception("Error while getting address")
  
        return jump_list
        
            
        