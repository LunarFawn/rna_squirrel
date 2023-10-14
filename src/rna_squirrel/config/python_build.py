"""
File for classes and code that deal with
building the python API and config files
after yaml operations reads the files
"""

import sys
import os
from typing import List


class PythonBuild():
    """
    Main class for handeling creating python files
    and all python files are generated via this class
    """
    
    def __init__(self) -> None:
        self
    
    def generate_config_header(self)->List[str]:
        """
        Generates a list of strings that represent
        the lines of the include header of the python
        config file
        """
        header:List[str] = []
        
        header.append("from enum import Enum")
        
        
        
        return header
    



