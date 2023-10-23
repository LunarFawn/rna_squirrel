import pytest

import pytest
import inspect
import heapq

from rna_squirrel.config.nut_yaml_operations import (
    YAMLOperations,
    WalkObjectReturn
)


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

from rna_squirrel.config.nut_python_build import PythonBuild

from pathlib import Path

from queue import PriorityQueue
import builtins
import os
import sys
from typing import List, Dict, Any

LINUX_PATH = Path(f'/home/rnauser/repo/rna_squirrel/src/test/bin/new_yaml_version_v1.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\new_yaml_version_v1.yaml")
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

def test_build_nut_enum(python_build:PythonBuild, yaml_ops:YAMLOperations):
    lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    assert lines[1] == '\tPrimaryStructure = "primary_structure_db"\n'
    
def test_build_object_enum(python_build:PythonBuild, yaml_ops:YAMLOperations):

    class_name:str = "PrimaryStructure"
    parent_lines:List[str] = []
    child_lines:List[str] = []
    parent_lines, child_lines = python_build.generate_object_enum(container=yaml_ops.definitions.definition_dict[class_name])
    assert len(parent_lines) == 1
    assert len(child_lines) == 2
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
    assert main_call[2] == '\tdef __init__(self, use_db:bool = False) -> None:\n'
    assert main_call[24] == '\tdef ensemble(self)->Ensemble:\n'

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

    