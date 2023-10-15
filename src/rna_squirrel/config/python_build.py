"""
File for classes and code that deal with
building the python API and config files
after yaml operations reads the files
"""

import sys
import os
from typing import List
from queue import PriorityQueue


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
    
    def generate_object_enum(self, class_name:str, atr_list:List[str], db_posfix:str = "DB"):
        """
        Generate the list of string that make up the attribute enums
        These feed into the dynamic class builder and tells it what to
        name things
        """
        class_lines:List[str] = []
        
        enum_title:str = f'class {class_name}_Attributes(Enum):'
        class_lines.append(enum_title)
        #now build the attribute enums
        for atr in atr_list:
          line:str = f'\t{atr} = "{atr}_{db_posfix}"'
          class_lines.append(line)
        
        return class_lines  

    
    def generate_config_baseclass(self, class_name:str):
        """
        Generate the list of strings that make up the
        config baseclass. This class can be considered the
        definition class and how it is build out will affect
        how the dynamic variables are addressed in the backend
        """
        
        #first generate teh header 
        class_lines:List[str] = []
        class_lines.append(f'class {class_name}(Nut):')
        class_lines.append('\n')
        class_lines.append('\tdef __init__(self, use_db:bool = False) -> None:')
        class_lines.append('\t\tsuper().__init__(enum_list=Nut_Attributes,')
        class_lines.append('\t\t\tuse_db=True,')
        class_lines.append('\t\t\tdb=None)')    
        class_lines.append('\n')             
                         
        #now build out the objects and the attributes

    def generate_config_baseclass_declaration(self):
        pass    