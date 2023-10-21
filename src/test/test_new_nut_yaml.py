import pytest

from rna_squirrel.config.nut_yaml_operations import YAMLOperations
from rna_squirrel.config.nut_yaml_objects import NutStructure, NutDatabaseInfo

from pathlib import Path

from queue import PriorityQueue
import builtins

from typing import List, Dict

@pytest.fixture
def yaml_data():
    yaml: YAMLOperations = YAMLOperations()
    return yaml.open_yml_config(file_path=CONFIG_PATH)

@pytest.fixture
def yml_ops():
   return  YAMLOperations()


LINUX_PATH = Path(f'/home/rnauser/repo/rna_squirrel/src/test/bin/new_yaml_version_v1.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\new_yaml_version_v1.yaml")
CONFIG_PATH = LINUX_PATH

def test_open_yaml(yaml_data):
    # yaml: YAMLOperations = YAMLOperations()
    # data = yaml.open_yml_config(file_path=WINDOWS_PATH)
    assert isinstance(yaml_data, NutStructure) == True
    
def test_load_object_spec(yaml_data):
    pass
    # test_object =  yaml_data["PrimaryStructure"].object_list[0]
    # test_object2 =  yaml_data["NUT"].objects.object_list[0]
    # assert  isinstance(test_object, String) == True
    # assert  isinstance(test_object2, ClassType) == True