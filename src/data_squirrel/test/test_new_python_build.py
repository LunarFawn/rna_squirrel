import pytest

import pytest
import inspect
import heapq

from data_squirrel.config.nut_yaml_operations import (
    YAMLOperations,
    WalkObjectReturn
)


from data_squirrel.config.nut_yaml_objects import (
    NutStructure,
    NutDatabaseInfo,
    NutContainerDefinitions,
    NutDatabaseInfo,
    NutDeclaration,
    NutContainer,
    NutObject,
    NutObjectType
)

from data_squirrel.config.nut_python_build import PythonBuild

from pathlib import Path

from queue import PriorityQueue
import builtins
import os
import sys
from typing import List, Dict, Any

from data_squirrel.make_single_api_file import build_shared_python_nut

LINUX_PATH = Path(f'/home/rnauser/repo/rna_squirrel/src/test/bin/new_yaml_version_v3.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\new_yaml_version_v3.yaml")
CONFIG_PATH = LINUX_PATH

@pytest.fixture
def yaml_ops():
    yaml: YAMLOperations = YAMLOperations()
    yaml.open_yml_config(file_path=CONFIG_PATH)
    return yaml

@pytest.fixture
def python_build():
    return PythonBuild()

def test_generate_header_strings(python_build:PythonBuild):
    file_header:List[str] = python_build.generate_config_header()
    assert file_header[1]  == 'Config file built from yaml\n'

def test_generate_exteral_imports(python_build:PythonBuild, yaml_ops:YAMLOperations):
    lines: List[str] = python_build.generate_external_imports(external_attrs=yaml_ops.nut.external_imports)
    assert lines[0]  == 'from serena.utilities.ensemble_structures import Sara2SecondaryStructure\n'

def test_build_nut_enum(python_build:PythonBuild, yaml_ops:YAMLOperations):
    lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    assert lines[1] == '\tPrimaryStructure = "primary_structure_db"\n'
    
def test_build_object_enum(python_build:PythonBuild, yaml_ops:YAMLOperations):

    class_name:str = "PrimaryStructure"
    parent_lines:List[str] = []
    child_lines:List[str] = []
    parent_lines, child_lines = python_build.generate_object_enum(container=yaml_ops.definitions.definition_dict[class_name])
    assert len(parent_lines) == 1
    assert len(child_lines) == 3
    assert child_lines[1] == '\tstrand = "strand_db"\n'
    
def test_config_definition_generation(python_build:PythonBuild,yaml_ops:YAMLOperations):
    lines:str = python_build.generate_config_baseclass(class_name="NupackStrand",
                                                       container_definitions=yaml_ops.definitions,
                                                       nut_structure=yaml_ops.nut)
    assert lines[0] == 'class NupackStrand(Nut):\n'

def test_build_config_file(python_build:PythonBuild,yaml_ops:YAMLOperations):
    file_header:List[str] = python_build.generate_config_header()
    enum_lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    basecode_lines:str = python_build.generate_config_baseclass(class_name="NupackStrand",
                                                       container_definitions=yaml_ops.definitions,
                                                       nut_structure=yaml_ops.nut)
    full_list:List[str] = file_header + enum_lines + basecode_lines
    dst:Path = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_config.py')
    with open(dst, 'w') as file:
        file.writelines(full_list)
    assert os.path.isfile(dst) == True

def test_generate_api_header(python_build:PythonBuild, yaml_ops:YAMLOperations):
    nut_struct_name:str = "NupackStrand"
    path_to_config:str = 'rna_squirrel.config.nupack_config'
    header:List[str] = python_build.generate_api_header(config_file_path=path_to_config,
                                                        nut_struct_name=nut_struct_name)
    assert header[1] == 'File that defines the main RNA sequence data\n'
    assert header[9] == 'from rna_squirrel.config.nupack_config import (\n'
    assert header[10] == '\tNupackStrand,\n'

def test_generate_api_containers_structure(python_build:PythonBuild, yaml_ops:YAMLOperations):

    class_name:str = 'SecondaryStructure'
    class_object:NutContainer = yaml_ops._struct_dict[class_name]
    class_lines:List[str] = python_build.generate_api_containers_structure(class_name=class_name,
                                                                   struct_object=class_object)
    assert class_lines[0] == 'class SecondaryStructure(CustomAttribute):\n'

def test_generate_api_main_call(python_build:PythonBuild, yaml_ops:YAMLOperations):
    config_class:str = 'NupackStrand'
    main_call:List[str] = python_build.generate_api_main_call(config_class_name=config_class,
                                                              nut_container=yaml_ops.nut.nut_main_struct)
    assert main_call[2] == '\tdef __init__(self, working_folder:str, var_name:str, use_db:bool = False) -> None:\n'
    assert main_call[28] == '\t\tself._primary_structure = struct\n'

def test_build_api_file(python_build:PythonBuild, yaml_ops:YAMLOperations):
    full_list:List[str] = []
    nut_struct_name:str = "NupackStrand"
    path_to_config:str = 'test.bin.built_config'
    header_list:List[str]= python_build.generate_api_header(config_file_path=path_to_config,
                                                            nut_struct_name=nut_struct_name)
    full_list = full_list + header_list
    found_structs_list:List[str] = []
    yaml_ops.reset_priority_queue
    while len(yaml_ops.priority_queue) > 0:
        current_entry:tuple = yaml_ops.pop_priority_queue
        struct_name:str = current_entry[1]
        if struct_name not in found_structs_list:
            found_structs_list.append(struct_name)
            struct_container: NutContainer = yaml_ops.definitions.definition_dict[struct_name]
            current_list:List[str] = python_build.generate_api_containers_structure(class_name=struct_name,
                                                                                    struct_object=struct_container)
            full_list = full_list + current_list
    
    #now make main call
    main_call_list:List[str] = python_build.generate_api_main_call(config_class_name=nut_struct_name,
                                                                   nut_container=yaml_ops.nut.nut_main_struct)
    
    full_list = full_list + main_call_list
    dst:Path = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_api.py')
    with open(dst, 'w') as file:
        file.writelines(full_list)
    assert os.path.isfile(dst) == True

def test_build_one_file_api(python_build:PythonBuild, yaml_ops:YAMLOperations):
    full_list:List[str] = []
    nut_struct_name:str = "NupackStrand"
    header_list:List[str] = python_build.generate_one_file_api_header()
    external_links_list:List[str] = python_build.generate_external_imports(external_attrs=yaml_ops.nut.external_imports)
    enum_lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    basecode_lines:List[str] = python_build.generate_config_baseclass(class_name=nut_struct_name,
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
            struct_container: NutContainer = yaml_ops.definitions.definition_dict[struct_name]
            current_list:List[str] = python_build.generate_api_containers_structure(class_name=struct_name,
                                                                                    struct_object=struct_container)
            full_list = full_list + current_list
    
    #now make main call
    main_call_list:List[str] = python_build.generate_api_main_call(config_class_name=nut_struct_name,
                                                                   nut_container=yaml_ops.nut.nut_main_struct)
    full_list = full_list + main_call_list
    dst:Path = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_single_api.py')
    #dst:Path = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\built_single_api.py")
    with open(dst, 'w') as file:
        file.writelines(full_list)
    assert os.path.isfile(dst) == True
    
def test_main_call_run():
    build_shared_python_nut(nut_struct_name="RNAStruct",
                      yaml_config_path=CONFIG_PATH,
                      dst_save_filename=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_single_api_2.py'))
    assert os.path.isfile(Path('/home/rnauser/repo/rna_squirrel/src/test/bin/built_single_api_2.py')) == True