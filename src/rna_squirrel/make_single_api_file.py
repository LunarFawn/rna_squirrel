"""
File for generating the api file
"""

from typing import List
from pathlib import Path
import os

from rna_squirrel.config.nut_yaml_operations import (
    YAMLOperations,
    WalkObjectReturn
)
from rna_squirrel.config.nut_python_build import PythonBuild

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

class GenerateSingleApifile():
    """
    Class for handleing the generation of the
    single api file
    """
    
    def __init__(self) -> None:
        self.yaml_ops: YAMLOperations = YAMLOperations()
        self.python_build :PythonBuild = PythonBuild()
    
    def run(self, nut_struct_name:str, yaml_config_path:Path, dst_save_filename:Path):
        self.yaml_ops.open_yml_config(file_path=yaml_config_path)
        full_list:List[str] = []
        header_list:List[str] = self.python_build.generate_one_file_api_header()
        enum_lines: List[str] = self.python_build.generate_nut_enums(nut_structure=self.yaml_ops.nut)
        basecode_lines:List[str] = self.python_build.generate_config_baseclass(class_name=nut_struct_name,
                                                        container_definitions=self.yaml_ops.definitions,
                                                        nut_structure=self.yaml_ops.nut)
        full_list:List[str] = header_list + enum_lines + basecode_lines
        found_structs_list:List[str] = []
        self.yaml_ops.reset_priority_queue
        while len(self.yaml_ops.priority_queue) > 0:
            current_entry:tuple = self.yaml_ops.pop_priority_queue
            struct_name:str = current_entry[1]
            if struct_name not in found_structs_list:
                found_structs_list.append(struct_name)
                struct_container: NutContainer =self.yaml_ops.definitions.definition_dict[struct_name]
                current_list:List[str] = self.python_build.generate_api_containers_structure(class_name=struct_name,
                                                                                        struct_object=struct_container)
                full_list = full_list + current_list
        
        #now make main call
        main_call_list:List[str] = self.python_build.generate_api_main_call(config_class_name=nut_struct_name,
                                                                    nut_container=self.yaml_ops.nut.nut_main_struct)
        full_list = full_list + main_call_list
        #dst:Path = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_single_api.py')
        #dst:Path = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\built_single_api.py")
        with open(dst_save_filename, 'w') as file:
            file.writelines(full_list)
