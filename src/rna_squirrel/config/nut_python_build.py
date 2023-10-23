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
        header.append('"""\n')
        header.append('Config file built from yaml\n')
        header.append('"""\n')
        header.append("\n")
        header.append("\n")
        header.append("from enum import Enum\n")
        header.append("from typing import TypeVar, Type, List, Dict\n")
        header.append("from attrs import define, field\n")
        header.append("from rna_squirrel.config.dynamic_rna_strand import (\n")
        header.append("\tNut,\n")
        header.append("\tValue,\n")
        header.append("\tGenericAttribute,\n")
        header.append("\tAtrClass,\n")
        header.append("\tCustomAttribute\n")
        header.append(")\n")
        header.append("\n")
        return header

    def generate_nut_enums(self, nut_structure:NutStructure):
        enum_lines:List[str] = []
        
        enum_title:str = f'class Nut_Attributes(Enum):\n'
        enum_lines.append(enum_title)
        #now build the attribute enums
        for item in nut_structure.nut_main_struct.object_list:
            line:str = f'\t{item.object_info} = "{item.db_name}"\n'
            enum_lines.append(line)
        enum_lines.append('\n')
        enum_lines.append('\n')
        
        return enum_lines

    def generate_object_enum(self, container:NutContainer):
        """
        Generate the list of string that make up the attribute enums
        These feed into the dynamic class builder and tells it what to
        name things
        """
        parent_lines:List[str] = []
        child_lines:List[str] = []
        
        parent_title:str = f'class {container.name}_Parent_Attributes(Enum):\n'
        child_title:str = f'class {container.name}_Child_Attributes(Enum):\n'
        parent_lines.append(parent_title)
        child_lines.append(child_title)
        
        #now build the attribute enums
        for item in container.object_list:
            if item.object_type == NutObjectType.CONTAINER:
                line:str = f'\t{item.object_info} = "{item.db_name}"\n'
                parent_lines.append(line)
            else:                
                line:str = f'\t{item.name} = "{item.db_name}"\n'
                child_lines.append(line)

        
        return parent_lines, child_lines   
    
    def generate_config_baseclass(self, class_name:str, nut_structure:NutStructure, container_definitions: NutContainerDefinitions):
        """
        Generate the list of strings that make up the
        config baseclass. This class can be considered the
        definition class and how it is build out will affect
        how the dynamic variables are addressed in the backend
        """
        
        #first generate teh header 
        class_lines:List[str] = []
        class_lines.append(f'class {class_name}(Nut):\n')
        class_lines.append('\n')
        class_lines.append('\tdef __init__(self, use_db:bool = False) -> None:\n')
        class_lines.append('\t\tsuper().__init__(enum_list=Nut_Attributes,\n')
        class_lines.append('\t\t\tuse_db=True,\n')
        class_lines.append('\t\t\tdb=None)\n')    
        class_lines.append('\n')             
        class_lines.append('\n') 
        
        
        #walk the nut structure now
        for nut_object in nut_structure.nut_main_struct.object_list:
            #check if container or value
            if nut_object.object_type == NutObjectType.CONTAINER:
                #walk this container and populate with the assumption that
                #this container has already been initialized
                next_container:NutContainer = container_definitions.definition_dict[nut_object.object_info]
                class_lines = self.generate_recursive_config_baseline_attributes(container_definitions=container_definitions,
                                                                   container=next_container,
                                                                   current_lines=class_lines,
                                                                   parent_container_name=nut_object.db_name)                
                # for item in next_container.object_list:
                #     if item.object_type == NutObjectType.CONTAINER:
                #         class_lines.append(f'\t\tself.{nut_object.db_name}.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,')
                #         class_lines.append(f'\t\t\tattribute={item.db_name}')
                #         class_lines.append(f'\t\t\tatr_type=None))')
                #         class_lines.append('\n') 
                        
                #     else:
                #         class_lines.append(f'\t\tself.{nut_object.db_name}.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,')
                #         class_lines.append(f'\t\t\tattribute={item.db_name}')
                #         class_lines.append(f'\t\t\tatr_type={item.object_type.value}))')
                #         class_lines.append('\n') 
            else:
                pass
        
        return class_lines
    
    def generate_recursive_config_baseline_attributes(self, container_definitions: NutContainerDefinitions, container:NutContainer, current_lines:List[str], parent_container_name:str):
        for item in container.object_list:
            if item.object_type == NutObjectType.CONTAINER:
                current_lines.append(f'\t\tself.{parent_container_name}.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,\n')
                current_lines.append(f'\t\t\tattribute="{item.db_name}",\n')
                current_lines.append(f'\t\t\tatr_type=None))\n')
                current_lines.append('\n') 
                
                next_container:NutContainer = container_definitions.definition_dict[item.object_info]
                parent_container:str =f'{parent_container_name}.{item.db_name}' 
                
                current_lines = self.generate_recursive_config_baseline_attributes(container_definitions=container_definitions,
                                                                   container=next_container,
                                                                   current_lines=current_lines,
                                                                   parent_container_name=parent_container)
                
            else:
                current_lines.append(f'\t\tself.{parent_container_name}.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,\n')
                current_lines.append(f'\t\t\tattribute="{item.db_name}",\n')
                current_lines.append(f'\t\t\tatr_type={item.object_type.value}))\n')
                current_lines.append('\n')
        
        return current_lines
        
    def generate_api_containers_structure(self, class_name:str, struct_object:NutContainer):
        """
        Dynamically build the classes for the python API
        """
        struct_lines:List[str] = []
        
        #first make the header
        struct_lines.append(f'class {class_name}(CustomAttribute):\n')
        
        struct_lines.append('\tdef __init__(self, parent: Any, current:Any, save_value:bool) -> None:\n')
        struct_lines.append('\t\tself.parent = parent\n')
        struct_lines.append('\t\tself.current = current\n')
        struct_lines.append('\t\tself.do_save = save_value\n')
        
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
            struct_lines.append('\t@property\n')
            struct_lines.append(f'\tdef {atr_name}(self)->{return_type}:\n')
            struct_lines.append(f'\t\treturn self.parent.{struct_db_name}.{atr_db_name}\n')
            struct_lines.append('\n')
            
            #now the setter
            struct_lines.append(f'\t@{atr_name}.setter\n')
            struct_lines.append(f'\tdef {atr_name}(self, value:{return_type}):\n')
            struct_lines.append(f'\t\tself.parent.{struct_db_name}.{atr_db_name} = value\n') 
            struct_lines.append('\n')           
            #now an empty line between attributes
 
            
        #now an empty line at the end of the structure to ensure it is seperated form 
        #next structure
        struct_lines.append('\n')    
        
        return struct_lines

    def generate_api_header(self, config_file_path:str, nut_struct_name:str):
        """
        Generate the header for the API
        """
        
        header_lines:List[str] = []
        
        header_lines.append('"""\n')
        header_lines.append('File that defines the main RNA sequence data\n')
        header_lines.append('"""\n')
        header_lines.append('\n')
        header_lines.append('\n')
        header_lines.append('from attrs import define, field\n')
        header_lines.append('from collections import namedtuple\n')
        header_lines.append('from typing import List, Dict, Any\n')
        header_lines.append('\n')
        header_lines.append(f'from {config_file_path} import (\n')
        header_lines.append(f'\t{nut_struct_name},\n')
        header_lines.append(')\n')
        header_lines.append('\n')
        header_lines.append('from rna_squirrel.config.dynamic_rna_strand import (\n')
        header_lines.append('\tNut,\n')
        header_lines.append('\tValue,\n')
        header_lines.append('\tGenericAttribute,\n')
        header_lines.append('\tAtrClass,\n')
        header_lines.append('\tCustomAttribute\n')
        header_lines.append(')\n')
        header_lines.append('\n')
        header_lines.append('\n')
        
        return header_lines
        
        
    def generate_api_main_call(self, config_class_name:str, nut_container:NutContainer):
        """
        Generate the man entry call in the api file
        """
    
        main_call_line:List[str] = []
        main_call_line.append(f'class {nut_container.name}({config_class_name}):\n')
        main_call_line.append('\n')
        main_call_line.append('\tdef __init__(self, use_db:bool = False) -> None:\n')
        main_call_line.append('\t\tsuper().__init__(use_db=use_db)\n')
        main_call_line.append('\n')
        main_call_line.append('\n')
        
        
        for item in nut_container.object_list:
            line:str = ''
            if item.object_type == NutObjectType.CONTAINER:
                line = f'\t\tself._{item.name}: {item.object_info} = {item.object_info}(save_value=True,\n'
                main_call_line.append(line)
                main_call_line.append('\t\t\tcurrent=None,\n')
                main_call_line.append('\t\t\tparent=self)\n') 
                main_call_line.append('\n')
            else:
                pass
                #i think if it is a value then do nothing
                #line = f'\t\tself._{item.name}: {item.object_type.value}\n'
        
        #now build the getter and setters
        
        for item in nut_container.object_list:
            main_call_line.append('\t@property\n')
            line:str = ''
            if item.object_type == NutObjectType.CONTAINER:
                main_call_line.append(f'\tdef {item.name}(self)->{item.object_info}:\n')
                main_call_line.append(f'\t\treturn self._{item.name}\n')
            else:
                main_call_line.append(f'\tdef {item.name}(self)->{item.object_type.value}:\n')
                main_call_line.append(f'\t\treturn self.{item.db_name}\n')
            main_call_line.append('\n')  
        
            main_call_line.append(f'\t@{item.name}.setter\n')
            line:str = ''
            if item.object_type == NutObjectType.CONTAINER:
                main_call_line.append(f'\tdef {item.name}(self, struct:{item.object_info}):\n')
                main_call_line.append(f'\t\tself._{item.name} = struct\n')
            else:
                main_call_line.append(f'\tdef {item.name}(self, value:{item.object_type.value}):\n')
                main_call_line.append(f'\t\tself.{item.db_name} = value\n')
            main_call_line.append('\n')
            main_call_line.append('\n')
            
        return main_call_line
        
            
        


    

    
    
    
