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
        header.append("from typing import TypeVar, Type, List")
        header.append("from attrs import define, field")
        header.append("from rna_squirrel.config.dynamic_rna_strand import (")
        header.append("\tNut,")
        header.append("\tValue,")
        header.append("\tGenericAttribute,")
        header.append("\tAtrClass,")
        header.append("\tCustomAttribute")
        header.append(")")
        
        return header
    



