"""
File to hold teh default classes for manipulating
data that goes throught the setter and getter
of the dynamic backend
"""
from typing import Any, Dict
from enum import Enum

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
        routing.get_attr_address(attribute=parent)
        
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
    
    def get_attr_address(self, attribute:Any):
        """
        get the attribute parent
        """
        pass