import pytest
from pathlib import Path
from rna_squirrel.config.python_build import PythonBuild
from typing import List, Dict

from rna_squirrel.config.yaml_operations import (    
    String,
    ClassDeclaration,
    ClassType,
    Objects,
    WalkObjectReturn
)

@pytest.fixture
def yaml_data():
    yaml: YAMLOperations = YAMLOperations()
    return yaml.open_yml_config(file_path=CONFIG_PATH)

@pytest.fixture
def yml_ops():
   return  YAMLOperations()

from rna_squirrel.config.yaml_operations import YAMLOperations

LINUX_PATH = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\test_class.yaml")
CONFIG_PATH = WINDOWS_PATH

@pytest.fixture
def python_build():
    return PythonBuild()

def test_generate_header_strings(python_build:PythonBuild):
    file_header:List[str] = python_build.generate_config_header()
    assert file_header[1]  == "from typing import TypeVar, Type, List"
    
def test_build_object_enum(python_build:PythonBuild):
    attributes:List[str] = ["PrimaryStructure","Ensemble"]
    class_name:str = "Nut"
    lines: List[str] = python_build.generate_object_enum(class_name=class_name,
                                                         atr_list=attributes)
    assert lines[1] == '\tPrimaryStructure = "PrimaryStructure_DB"'
    
def test_config_definition_generation(python_build:PythonBuild):
    lines:str = python_build.generate_config_baseclass(class_name="NupackStrand")
    assert lines[0] == 'class NupackStrand(Nut):'
    
def test_generate_config_baseclass_structure(python_build:PythonBuild, yml_ops:YAMLOperations):
    data = yml_ops.open_yml_config(CONFIG_PATH)
    declared_classes = yml_ops.get_declarations(yaml_data=data)
    struct_dict:Dict[str, Objects] = yml_ops.build_struct_dict(yaml_data=data,
                                                               declarations=declared_classes)
    class_name:str = 'PrimaryStructure'
    class_object:Objects = struct_dict[class_name]
    class_lines:List[str] = python_build.generate_config_baseclass_structure(class_name=class_name,
                                                                   struct_object=class_object)
    assert class_lines[0] == 'class PrimaryStructure(CustomAttribute):'

def test_generate_main_object_call():
    