"""
File for generating the api file
"""

from typing import List
from pathlib import Path

from data_squirrel.config.nut_yaml_operations import (
    YAMLOperations
)

from data_squirrel.config.nut_python_build import PythonBuild

from data_squirrel.config.nut_yaml_objects import (
    NutContainer
)

yaml_ops: YAMLOperations = YAMLOperations()
python_build :PythonBuild = PythonBuild()

def run(nut_struct_name:str, yaml_config_path:Path, dst_save_filename:Path):
    """
    Build a data_squirrel python package file from nut yaml definitions
    """
    yaml_ops.open_yml_config(file_path=yaml_config_path)
    full_list:List[str] = []
    header_list:List[str] = python_build.generate_one_file_api_header()
    enum_lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    basecode_lines:List[str] = python_build.generate_config_baseclass(class_name=nut_struct_name,
                                                    container_definitions=yaml_ops.definitions,
                                                    nut_structure=yaml_ops.nut)
    full_list:List[str] = header_list + enum_lines + basecode_lines
    found_structs_list:List[str] = []
    yaml_ops.reset_priority_queue
    while len(yaml_ops.priority_queue) > 0:
        current_entry:tuple = yaml_ops.pop_priority_queue
        struct_name:str = current_entry[1]
        if struct_name not in found_structs_list:
            found_structs_list.append(struct_name)
            struct_container: NutContainer =yaml_ops.definitions.definition_dict[struct_name]
            current_list:List[str] = python_build.generate_api_containers_structure(class_name=struct_name,
                                                                                    struct_object=struct_container)
            full_list = full_list + current_list
    
    #now make main call
    main_call_list:List[str] = python_build.generate_api_main_call(config_class_name=nut_struct_name,
                                                                nut_container=yaml_ops.nut.nut_main_struct)
    full_list = full_list + main_call_list
    #dst:Path = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_single_api.py')
    #dst:Path = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\built_single_api.py")
    try:
        with open(dst_save_filename, 'w') as file:
            file.writelines(full_list)
    except Exception as error:
        raise Exception(f'unable to write to file {dst_save_filename} the file contents {full_list} Error: {error}')
