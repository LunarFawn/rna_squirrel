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

from pathlib import Path

from queue import PriorityQueue
import builtins

from typing import List, Dict, Any

@pytest.fixture
def yaml_ops():
    yaml: YAMLOperations = YAMLOperations()
    yaml.open_yml_config(file_path=CONFIG_PATH)
    return yaml

@pytest.fixture
def yaml_nut(yaml_ops:YAMLOperations):
    return yaml_ops.nut

@pytest.fixture
def yaml_def(yaml_ops:YAMLOperations):
    return yaml_ops.definitions


LINUX_PATH = Path(f'/home/rnauser/repo/rna_squirrel/src/test/bin/new_yaml_version_v3.yaml')
WINDOWS_PATH = Path(r"C:\Users\pearljen\Documents\me\repo\rna_squirrel\src\test\bin\new_yaml_version_v3.yaml")
CONFIG_PATH = LINUX_PATH

def test_open_yaml(yaml_ops:YAMLOperations):
    # yaml: YAMLOperations = YAMLOperations()
    # data = yaml.open_yml_config(file_path=WINDOWS_PATH)
    assert isinstance(yaml_ops.nut, NutStructure) == True
    assert isinstance(yaml_ops.definitions, NutContainerDefinitions) == True
    
def test_load_yaml_nut_class(yaml_nut:NutStructure):
    assert isinstance(yaml_nut, NutStructure) == True
    attributes:List[str] = list(vars(yaml_nut).keys())
    assert len(attributes) == 5
    assert ('db_info' in attributes) == True
    assert ('nut_container_declarations' in attributes) == True
    assert ('nut_main_struct' in attributes) == True
    assert ('nut_containers' in attributes) == True


def test_load_NutDatabaseInfo_class(yaml_nut:NutStructure):
    db_info:NutDatabaseInfo = yaml_nut.db_info
    assert isinstance(db_info, NutDatabaseInfo) == True
    attributes:List[str] = list(vars(db_info).keys())
    assert len(attributes) == 1
    assert ('db_name' in attributes) == True
    
def test_populate_db_info(yaml_nut:NutStructure):
    db_info:NutDatabaseInfo = yaml_nut.db_info
    assert db_info.db_name == "test_db"

def test_load_nut_container_declarations_class(yaml_nut:NutStructure):
    nut_declarations:List[NutDeclaration] = yaml_nut.nut_container_declarations 
    assert type(nut_declarations) == list
    for declaration in nut_declarations:
        assert isinstance(declaration, NutDeclaration)
        attributes:List[str] = list(vars(declaration).keys())
        assert len(attributes) == 1
        assert ('name' in attributes) == True

def test_populate_nut_container_declarations(yaml_nut:NutStructure):
    nut_declarations:List[NutDeclaration] = yaml_nut.nut_container_declarations 
    assert nut_declarations[0].name == "PrimaryStructure"
    assert nut_declarations[1].name == "Energy"
    assert nut_declarations[2].name == "SecondaryStructure"
    assert nut_declarations[3].name == "Ensemble"
    
def test_load_nut_main_struct_class(yaml_nut:NutStructure):
    main_struct: NutContainer = yaml_nut.nut_main_struct
    assert isinstance(main_struct, NutContainer) == True
    attributes:List[str] = list(vars(main_struct).keys())
    assert len(attributes) == 3
    assert ('name' in attributes) == True
    assert ('db_name' in attributes) == True
    assert ('object_list' in attributes) == True  
    
    assert type(main_struct.object_list) == list
    for item in main_struct.object_list:
        assert isinstance(item, NutObject) == True
        assert isinstance(item.object_type, NutObjectType) == True
        attributes:List[str] = list(vars(item).keys())
        assert len(attributes) == 4
        assert ('name' in attributes) == True
        assert ('db_name' in attributes) == True
        assert ('object_info' in attributes) == True
        assert ('object_type' in attributes) == True
 
def test_populate_main_nut_struct(yaml_nut:NutStructure):
    main_struct: NutContainer = yaml_nut.nut_main_struct
    assert main_struct.name == "RNAStrand"
    assert main_struct.db_name == "RNAStrand_db"    
    assert main_struct.object_list[0].name == "primary_structure"
    assert main_struct.object_list[0].db_name == "primary_structure_db"
    assert main_struct.object_list[0].object_type == NutObjectType.CONTAINER
    assert main_struct.object_list[0].object_info == 'PrimaryStructure'
    assert main_struct.object_list[1].name == "ensemble"
    assert main_struct.object_list[1].db_name == "ensemble_db"
    assert main_struct.object_list[1].object_type == NutObjectType.CONTAINER
    assert main_struct.object_list[1].object_info == 'Ensemble'


def test_load_yaml_definitions_class(yaml_def:NutContainerDefinitions):
    assert isinstance(yaml_def, NutContainerDefinitions) == True   
    attributes:List[str] = list(vars(yaml_def).keys())
    assert len(attributes) == 2
    assert ('nut_containers_definitions' in attributes) == True
    assert ('definition_dict' in attributes) == True
    assert type(yaml_def.nut_containers_definitions) == list
    for item in yaml_def.nut_containers_definitions:
        assert isinstance(item, NutContainer) == True
        attributes:List[str] = list(vars(item).keys())
        assert len(attributes) == 3
        assert ('name' in attributes) == True
        assert ('db_name' in attributes) == True
        assert ('object_list' in attributes) == True  
        assert type(item.object_list) == list
        for sub_item in item.object_list:
            assert isinstance(sub_item, NutObject) == True
            assert isinstance(sub_item.object_type, NutObjectType) == True
            sub_attributes:List[str] = list(vars(sub_item).keys())
            assert len(sub_attributes) == 4
            assert ('name' in sub_attributes) == True
            assert ('db_name' in sub_attributes) == True
            assert ('object_info' in sub_attributes) == True
            assert ('object_type' in sub_attributes) == True
    
def test_populate_yaml_definitions(yaml_def:NutContainerDefinitions):
    
    definitions: List[NutContainer] = yaml_def.nut_containers_definitions
    assert definitions[0].name == "PrimaryStructure"
    assert definitions[0].db_name == f'{definitions[0].name}_db'
    assert len(definitions[0].object_list) == 2
    assert definitions[0].object_list[0].name == "strand"
    assert definitions[0].object_list[0].db_name == f'{definitions[0].object_list[0].name}_db'
    assert definitions[0].object_list[0].object_type == NutObjectType.VALUE
    assert definitions[0].object_list[0].object_info == "str"

def test_walk_objects_list(yaml_ops:YAMLOperations):
        
    walk_object:WalkObjectReturn = yaml_ops.walk_objects_list(object_structs=yaml_ops.nut.nut_containers,
                                                            level=1)
    assert walk_object.structure_found_list == ['Energy', 'SecondaryStructure', 'PrimaryStructure']
    assert walk_object.struct_priority_queue == [(-1, 'Energy'), (-1, 'SecondaryStructure'), (-1, 'PrimaryStructure')]

def test_build_structure_dict(yaml_ops:YAMLOperations):   
    #yaml_ops.build_struct_dict()
    assert isinstance(yaml_ops.containers_dict['NUT'], NutContainer) == True
    keys_list:List[str] = list(yaml_ops.containers_dict.keys())
    assert len(keys_list) == len(yaml_ops.nut.nut_containers)+1
    for item in yaml_ops.nut.nut_containers:
        assert (item in keys_list) == True
    
def test_build_struct_queue(yaml_ops:YAMLOperations):
    poped_order:List[tuple] = []
    for _ in range(len(yaml_ops.priority_queue)):
      poped = yaml_ops.pop_priority_queue
      poped_order.append(poped)
    assert poped_order == [(-2, 'Energy'), (-2, 'PrimaryStructure'), (-2, 'SecondaryStructure'), (-1, 'Ensemble'), (-1, 'PrimaryStructure'), (-1, 'Sara2secStructLists')]

def test_copy_priority_queue(yaml_ops:YAMLOperations):
    new_queue: List[tuple] = yaml_ops.get_original_priorty_queue_copy
    assert new_queue == yaml_ops.priority_queue
    yaml_ops.pop_priority_queue
    assert len(new_queue) == 6
    assert len(yaml_ops.priority_queue) == 5