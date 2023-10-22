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
    assert file_header[1]  == "from typing import TypeVar, Type, List"

def test_build_nut_enum(python_build:PythonBuild, yaml_ops:YAMLOperations):
    lines: List[str] = python_build.generate_nut_enums(nut_structure=yaml_ops.nut)
    assert lines[1] == '\tPrimaryStructure = "primary_structure_db"'
    
def test_build_object_enum(python_build:PythonBuild, yaml_ops:YAMLOperations):

    class_name:str = "PrimaryStructure"
    parent_lines:List[str] = []
    child_lines:List[str] = []
    parent_lines, child_lines = python_build.generate_object_enum(container=yaml_ops.definitions.definition_dict[class_name])
    assert len(parent_lines) == 1
    assert len(child_lines) == 2
    assert child_lines[1] == '\tstrand = "strand_db"'
    
def test_config_definition_generation(python_build:PythonBuild,yaml_ops:YAMLOperations):
    lines:str = python_build.generate_config_baseclass(class_name="NupackStrand",
                                                       container_definitions=yaml_ops.definitions,
                                                       nut_structure=yaml_ops.nut)
    assert lines[0] == 'class NupackStrand(Nut):'

def test_generate_api_containers_structure(python_build:PythonBuild, yaml_ops:YAMLOperations):

    class_name:str = 'PrimaryStructure'
    class_object:NutContainer = yaml_ops._struct_dict[class_name]
    class_lines:List[str] = python_build.generate_api_containers_structure(class_name=class_name,
                                                                   struct_object=class_object)
    assert class_lines[0] == 'class PrimaryStructure(CustomAttribute):'