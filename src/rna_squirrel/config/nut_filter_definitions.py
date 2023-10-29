"""
File to hold teh default classes for manipulating
data that goes throught the setter and getter
of the dynamic backend
"""
from typing import Any, Dict, List
from enum import Enum
import heapq

from rna_squirrel.config.nut_yaml_objects import AtrClass

class ValueFlow(Enum):
    OUTBOUND="OUTBOUND"
    INBOUND="INBOUND"
    BOTH="BOTH"
    
class NutFilterDefinitions():

    def __init__(self) -> None:
        pass
    
    def filter(self, parent:Any, attr_name:str, value:Any, flow_direction:ValueFlow):
        new_value:Any = value
        
        routing:NutAdressing = NutAdressing()
        jump_list: List[str] = routing.get_attr_address(parent_attr=parent,
                                 name=attr_name)
        
        heapq.heapify(jump_list)
        
        if flow_direction == ValueFlow.OUTBOUND:
            new_value = self.filter_out_flow(value=new_value,
                                             address=jump_list)
        elif flow_direction == ValueFlow.INBOUND:
            new_value = self.filter_in_flow(value=new_value)
        
        
        return new_value
        
    def filter_both_flow(self, value:Any):
        new_value:Any = value
        return new_value
    
    def filter_out_flow(self, value:Any, address:List[str]):
        """
        This is the 
        """
        for _ in range(len(address)):
            test_value:tuple = heapq.heappop(address)
            order:int = test_value[0]
            jump_name:str = test_value[1]
            print(f'{order} {jump_name}')
        new_value:Any = value
        if type(value) == str:
            new_value = f'{value}_from_db'
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
        
        jump_list.append((order,name)) 
        
        
        while hasattr(parent_attr, 'parent') == True:
            order += 1
            if getattr(parent_attr, 'atr_class') != AtrClass.NUT:
                parent_name = parent_attr.attribute
                jump_list.append((order, parent_name))                
            parent_attr = getattr(parent_attr, 'parent')
        
        if getattr(parent_attr, 'atr_class') == AtrClass.NUT:
            order += 1
            parent_name = parent_attr.var_name
            jump_list.append((order, parent_name))
        else:
            raise Exception("Error while getting address")
  
        return jump_list
        
            
        