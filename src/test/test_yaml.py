import pytest
from pathlib import Path
from rna_squirrel.config.yaml_operations import (    
    String,
    ClassDeclaration,
    ClassType,
    Objects
)


import builtins

from typing import List, Dict

@pytest.fixture
def yaml_data():
    yaml: YAMLOperations = YAMLOperations()
    return yaml.open_yml_config(file_path=CONFIG_PATH)

@pytest.fixture
def yml_ops():
   return  YAMLOperations()

from rna_squirrel.config.yaml_operations import YAMLOperations
CONFIG_PATH = Path('/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\test_class.yaml")

def test_open_yaml(yaml_data):
    # yaml: YAMLOperations = YAMLOperations()
    # data = yaml.open_yml_config(file_path=WINDOWS_PATH)
    assert yaml_data["CUSTOM_TYPES"][0]['name'] == 'PrimaryStructure'
    
def test_load_object_spec(yaml_data):
    test_object =  yaml_data["PrimaryStructure"].object_list[0]
    test_object2 =  yaml_data["NUT"].object_list[0]
    assert  isinstance(test_object, String) == True
    assert  isinstance(test_object2, ClassType) == True
    
def test_load_object_type(yaml_data):
    test_object:String =  yaml_data["PrimaryStructure"]["objects"][0]
    #test_type = getattr(builtins, test_object.python_type)  
    
    assert isinstance(test_object.python_type, type(str)) == True

def test_declarations(yaml_data):
    test_data: ClassDeclaration = yaml_data["DECLARATIONS"][0]
    assert isinstance(test_data, ClassDeclaration) == True
    assert test_data.name == "PrimaryStructure"
    
def test_get_class_declaration(yml_ops:YAMLOperations):
    data = yml_ops.open_yml_config(CONFIG_PATH)
    class_list:List[ClassDeclaration] = yml_ops.get_declarations(yaml_data=data)
    assert isinstance(class_list, List) ==  True
    assert len(class_list) == 4
    assert isinstance(class_list[0], ClassDeclaration) == True
    assert class_list[0].name == "PrimaryStructure"
    assert class_list[1].name == "Energy"
    assert class_list[2].name == "SecondaryStructure"
    assert class_list[3].name == "Ensemble"

def test_get_objects(yml_ops:YAMLOperations):
    data = yml_ops.open_yml_config(CONFIG_PATH)
    classes, values = yml_ops.get_object_list(yaml_data=data,
                                              class_name="SecondaryStructure")
    assert len(classes) == 2
    assert len(values) == 1

def test_build_struct_dict(yml_ops:YAMLOperations):
    data = yml_ops.open_yml_config(CONFIG_PATH)
    declared_classes = yml_ops.get_declarations(yaml_data=data)
    stuct_dict:Dict[str, Objects] = yml_ops.build_struct_dict(yaml_data=data,
                                           declarations=declared_classes)
    assert isinstance(stuct_dict["PrimaryStructure"].object_list[0] , String) == True 