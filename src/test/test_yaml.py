import pytest
from pathlib import Path
from rna_squirrel.config.yaml_operations import ObjectSpec, ObjectStatus
import builtins

@pytest.fixture
def yaml_data():
    yaml: YAMLOperations = YAMLOperations()
    return yaml.open_yml_config(file_path=WINDOWS_PATH)

from rna_squirrel.config.yaml_operations import YAMLOperations
CONFIG_PATH = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\test_class.yaml")

def test_open_yaml(yaml_data):
    # yaml: YAMLOperations = YAMLOperations()
    # data = yaml.open_yml_config(file_path=WINDOWS_PATH)
    assert yaml_data["OBJECT_CLASSES"][0]['name'] == 'PrimaryStructure'
    
def test_load_object_spec(yaml_data):
    test_object:ObjectSpec =  yaml_data["PrimaryStructure"]["attributes"][0]
    assert test_object.status_enum == ObjectStatus.VALUE

def test_load_object_type(yaml_data):
    test_object:ObjectSpec =  yaml_data["PrimaryStructure"]["attributes"][0]
    test_type = getattr(builtins, test_object.object_type)  
    
    assert isinstance(test_type, type(str)) == True