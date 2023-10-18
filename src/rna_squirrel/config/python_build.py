"""
File for classes and code that deal with
building the python API and config files
after yaml operations reads the files
"""

import sys
import os
from typing import List, Any, Dict
from queue import PriorityQueue
from rna_squirrel.config.yaml_operations import (    
    Objects,
    ClassType
)

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
        
        return class_lines
        #now build out the objects and the attributes
    
    # def generate_class_lines(self):
    #     pass
    
    # def generate_value_lines(self):
    #     pass
    
    def generate_config_baseclass_structure(self, class_name:str, struct_object:Objects):
        """
        Dynamically build the classes for the python API
        """
        struct_lines:List[str] = []
        
        #first make the header
        struct_lines.append(f'class {class_name}(CustomAttribute):')
        
        struct_lines.append('\tdef __init__(self, parent: Any, current:Any, save_value:bool) -> None:')
        struct_lines.append('\t\tself.parent = parent')
        struct_lines.append('\t\tself.current = current')
        struct_lines.append('\t\tself.do_save = save_value')
        
        #now build the python property getter and settes
        #these are the same for value and class with the name 
        #being the only difference
        for attribute in struct_object.object_list:
            atr_name:str = attribute.name
            atr_db_name:str = attribute.db_name
            struct_db_name:str = struct_object.db_name
            
            return_type:Any = None
            if isinstance(attribute, ClassType) is True:
                #its a structure or class whatever im calling it
                #atr_name = attribute.name
                return_type = attribute.class_type
                #db_name = attribute.db_name
            else:
                #its a value
                #atr_name = attribute.name
                return_type = attribute.python_type
                #db_name = attribute.db_name
            struct_lines.append('\n')
            #firest teh getter    
            struct_lines.append('\t@property')
            struct_lines.append(f'\tdef {atr_name}(self)->{return_type}:')
            struct_lines.append(f'\t\treturn self.parent.{struct_db_name}.{atr_db_name}')
            struct_lines.append('\n')
            
            #now the setter
            struct_lines.append(f'\t@{atr_name}.setter')
            struct_lines.append(f'\tdef {atr_name}(self, value:{return_type}):')
            struct_lines.append(f'\t\tself.parent.{struct_db_name}.{atr_db_name} = value')            
            #now an empty line between attributes
 
            
        #now an empty line at the end of the structure to ensure it is seperated form 
        #next structure
        struct_lines.append('\n')    
        
        return struct_lines
        
    def generate_config_file_nut_entry(self, class_name:str, struct_list:Dict[str, Objects],  ):
        """
        Dynamically build the main object that calls the code
        that builds the many structures in the object
        """   
        
        obj_lines:List[str] = []
        
        obj_lines.append(f'class {class_name}(Nut):')
        obj_lines.append('\n')
        obj_lines.append(f'\tdef __init__(self, use_db:bool = False) -> None:')
        obj_lines.append(f'\t\tsuper().__init__(enum_list=Nut_Attributes,')
        obj_lines.append(f'\t\t\tuse_db=True,')
        obj_lines.append(f'\t\t\tdb=None)')
        obj_lines.append('\n')
        
        #now need to build each attribute from a list of objects. The structs
        #defined in the nut are ready to have things assigned to them
        # this does not have to be in order
        
        obj_lines.append()
        obj_lines.append()
        obj_lines.append()
        obj_lines.append()
        
        
        