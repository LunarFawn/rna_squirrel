"""
File for generating the api file
"""

from typing import List
from pathlib import Path
import argparse
import os
from string import ascii_letters
from pathvalidate import sanitize_filepath

from data_squirrel.config.nut_yaml_operations import (
    YAMLOperations
)

from data_squirrel.config.nut_python_build import PythonBuild

from data_squirrel.config.nut_yaml_objects import (
    NutContainer
)

yaml_ops: YAMLOperations = YAMLOperations()
python_build :PythonBuild = PythonBuild()

def build_shared_python_nut(nut_struct_name:str, yaml_config_path:Path, dst_save_filename:Path):
    """
    Build a data_squirrel python package file from nut yaml definitions
    """
    yaml_ops.open_yml_config(file_path=yaml_config_path)
    full_list:List[str] = []
    header_list:List[str] = python_build.generate_one_file_api_header()
    external_links_list:List[str] = python_build.generate_external_imports(external_attrs=yaml_ops.nut.external_imports)
    enum_lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    basecode_lines:List[str] = python_build.generate_config_baseclass(class_name=yaml_ops.nut.nut_main_struct.name,
                                                    container_definitions=yaml_ops.definitions,
                                                    nut_structure=yaml_ops.nut)
    full_list:List[str] = header_list + external_links_list + enum_lines + basecode_lines
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

def script_run():
    """
    Build the Shared Python Framework Container API via command line arguments
    """
    parser = argparse.ArgumentParser()
    print("Hi")

    parser.add_argument("-n","--nut-struct", type=str, required=True)
    parser.add_argument("-c","--config-file", type=str, required=True)
    parser.add_argument("-s","--save-filename", type=str, required=True, help="This is just the name and not the full path. Do not add .py to it either. The file will be saved to the current working directory.")
        
    args = parser.parse_args()
    nut_struct_name:str = args.nut_struct
    nut_container_config_path:Path = Path(args.config_file)
    save_path:Path = Path(sanitize_filepath(f'{os.getcwd()}/{args.save_filename}.py'))
    
    print(nut_struct_name)
    print(nut_container_config_path)
    print(save_path)
    
    # if os.path.isdir(save_path) == False:
    #     raise FileExistsError(f'Path {save_path} is not a valid directory path')

    if os.path.isfile(nut_container_config_path) == False:
        raise FileExistsError(f'File path {nut_container_config_path} is not a valid file path')
    
    if set(nut_struct_name).difference(ascii_letters) or nut_struct_name.count(' ') > 0:
        raise ValueError("Nut struct name is invalid and is contains characters other than asci or has spaces in it")
    
    build_shared_python_nut(nut_struct_name=nut_struct_name,
                            yaml_config_path=nut_container_config_path,
                            dst_save_filename=save_path)