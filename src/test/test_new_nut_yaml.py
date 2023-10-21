import pytest
import inspect

from rna_squirrel.config.nut_yaml_operations import YAMLOperations
from rna_squirrel.config.nut_yaml_objects import (
    NutStructure,
    NutDatabaseInfo,
    NutContainerDefinitions,
    NutDatabaseInfo,
    NutDeclaration
)

from pathlib import Path

from queue import PriorityQueue
import builtins

from typing import List, Dict, Any

@pytest.fixture
def yaml_data():
    yaml: YAMLOperations = YAMLOperations()
    return yaml.open_yml_config(file_path=CONFIG_PATH)

@pytest.fixture
def yaml_nut(yaml_data):
    return yaml_data['NUT']

@pytest.fixture
def yaml_def(yaml_data):
    return yaml_data['DEFINITIONS']


LINUX_PATH = Path(f'/home/rnauser/repo/rna_squirrel/src/test/bin/new_yaml_version_v1.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\new_yaml_version_v1.yaml")
CONFIG_PATH = LINUX_PATH

def test_open_yaml(yaml_data):
    # yaml: YAMLOperations = YAMLOperations()
    # data = yaml.open_yml_config(file_path=WINDOWS_PATH)
    assert isinstance(yaml_data['NUT'], NutStructure) == True
    assert isinstance(yaml_data['DEFINITIONS'], NutContainerDefinitions) == True
    
def test_load_yaml_nut(yaml_nut):
    assert isinstance(yaml_nut, NutStructure) == True

def test_load_yaml_definitions(yaml_def):
    assert isinstance(yaml_def, NutContainerDefinitions) == True

def test_db_info(yaml_nut:NutStructure):
    db_info:NutDatabaseInfo = yaml_nut.db_info
    assert isinstance(db_info, NutDatabaseInfo) == True
    #now verify count and content of db_info
    attributes:List[str] = list(vars(db_info).keys())
    assert len(attributes) == 1
    assert ('db_name' in attributes) == True
    assert db_info.db_name == "test_db"

def test_nut_container_declarations(yaml_nut:NutStructure):
    nut_declarations:List[NutDeclaration] = yaml_nut.nut_container_declarations 
    assert type(nut_declarations) == list
    for declaration in nut_declarations:
        assert isinstance(declaration, NutDeclaration)
        attributes:List[str] = list(vars(declaration).keys())
        assert len(attributes) == 1
        assert ('name' in attributes) == True
    assert nut_declarations[0].name == "PrimaryStructure"
    assert nut_declarations[1].name == "Energy"
    assert nut_declarations[2].name == "SecondaryStructure"
    assert nut_declarations[3].name == "Ensemble"
    