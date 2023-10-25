"""
File to hold teh default classes for manipulating
data that goes throught the setter and getter
of the dynamic backend
"""
from typing import Any
from enum import Enum

class ValueFlow(Enum):
    UPSTREAM="UPSTREAM"
    DOWNSTREAM="DOWNSTREAM"
    BOTH="BOTH"
    
class NutFilterDefinitions():

    def __init__(self) -> None:
        pass
    
    def filter(self, value:Any, flow_direction:ValueFlow):
        
        if type(value) == str:
            pass
        
    def filter_both_flow(self):
        pass
    
    def filter_out_flow(self,  value:Any):
        """
        This is the 
        """
        pass
    
    def filter_in_flow(self,  value:Any):
        """
        This is the 
        """
        pass
    