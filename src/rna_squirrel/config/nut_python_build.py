"""
File that holds the code to build the python API's
"""


import sys
import os
from typing import List, Any, Dict

from rna_squirrel.config.nut_yaml_objects import (
    NutStructure,
    NutDatabaseInfo,
    NutContainerDefinitions,
    NutDatabaseInfo,
    NutDeclaration,
    NutContainer,
    NutObject,
    NutObjectType
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

    def generate_nut_enums(self, nut_structure:NutStructure):
        enum_lines:List[str] = []
        
        enum_title:str = f'class Nut_Attributes(Enum):'
        enum_lines.append(enum_title)
        #now build the attribute enums
        for item in nut_structure.nut_main_struct.object_list:
            line:str = f'\t{item.object_info} = "{item.db_name}"'
            enum_lines.append(line)
        
        return enum_lines

    def generate_object_enum(self, container:NutContainer, db_posfix:str = "DB"):
        """
        Generate the list of string that make up the attribute enums
        These feed into the dynamic class builder and tells it what to
        name things
        """
        class_lines:List[str] = []
        
        enum_title:str = f'class {container.name}_Attributes(Enum):'
        class_lines.append(enum_title)
        #now build the attribute enums
        for item in container.object_list:
            line:str = ''
            if item.object_type == NutObjectType.CONTAINER:
                line = f'\t{item.object_info} = "{item.db_name}"'
            else:                
                line = f'\t{item.name} = "{item.db_name}"'
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

    def generate_config_baseline_attrib_add(self, container:NutContainer):
        pass
    
    
    
    
    
    

    def generate_api_containers_structure(self, class_name:str, struct_object:NutContainer):
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
            if attribute.object_type == NutObjectType.CONTAINER:
                #its a structure or class whatever im calling it
                #atr_name = attribute.name
                return_type = attribute.object_info
                #db_name = attribute.db_name
            else:
                if attribute.object_type == NutObjectType.DICTIONARY:
                    return_type = f'{NutObjectType.DICTIONARY.value}{attribute.object_info}'
                else:
                    return_type = f'{attribute.object_type.value}'

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