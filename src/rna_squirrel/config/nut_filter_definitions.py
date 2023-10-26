"""
File to hold teh default classes for manipulating
data that goes throught the setter and getter
of the dynamic backend
"""
from typing import Any
from enum import Enum

class ValueFlow(Enum):
    OUTBOUND="OUTBOUND"
    INBOUND="INBOUND"
    BOTH="BOTH"
    
class NutFilterDefinitions():

    def __init__(self) -> None:
        pass
    
    def filter(self, value:Any, flow_direction:ValueFlow):
        new_value:Any = value
        
        if flow_direction == ValueFlow.OUTBOUND:
            new_value = self.filter_out_flow(value=new_value)
        elif flow_direction == ValueFlow.INBOUND:
            new_value = self.filter_in_flow(value=new_value)
        
        
        return new_value
        
    def filter_both_flow(self, value:Any):
        new_value:Any = value
        return new_value
    
    def filter_out_flow(self,  value:Any):
        """
        This is the 
        """
        new_value:Any = value
        if type(value) == str:
            new_value = f'{value}_from_db'
        return new_value
    
    def filter_in_flow(self,  value:Any):
        """
        This is the 
        """
        new_value:Any = value
        return new_value