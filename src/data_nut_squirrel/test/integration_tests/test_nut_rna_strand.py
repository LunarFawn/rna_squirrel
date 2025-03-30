import importlib.resources
import pytest
from pathlib import Path
from typing import List
import pkgutil
import os
import sys
import importlib
#from test.bin.built_api import Energy, PrimaryStructure, rna_strand, Ensemble

from data_nut_squirrel.test.bin.built_single_api_2 import (
    Spaceship,
    SpaceshipHelix,
    MidSection,
    Top,
    Fines,
    Engine,
    Flames
)

from data_nut_squirrel.test.bin.data.demo_external_class import (ExternalClassDemo,
                                                             ComponentsDemo)


# parent_path = importlib.resources.files("data_squirrel.test.bin")
# CONFIG_PATH =  parent_path.joinpath('test_class.yaml') # /home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml'
DATA_PATH = importlib.resources.files("data_nut_squirrel.test.bin.data")

@pytest.fixture
def empty_default_ship():
    
    # my_path = pkgutil.extend_path(sys.path,"hu")
    # CONFIG_PATH = my_path
    return Spaceship(var_name="spaceship_001",
                      working_folder=DATA_PATH)

# @pytest.fixture
# def empty_what_strand():
#     return WhatIsThis(var_name="what_1",
#                       working_folder=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))

#test

def test_get_empty_ship(empty_default_ship:Spaceship):
    with pytest.raises(Exception):     
        assert empty_default_ship.top == None

def test_set_ship_attribute(empty_default_ship:Spaceship):
    # new_struct:PrimaryStructure = PrimaryStructure(save_value=True)
    # new_struct.strand = "yo"
    empty_default_ship.top.color = "yo"
    assert empty_default_ship.top.color == "yo"
    assert empty_default_ship.top.color == "yo"

    empty_default_ship.engine.flames.size = 10
    assert empty_default_ship.engine.flames.size == 10
    empty_default_ship.engine.flames.luemens = 11.0
    assert empty_default_ship.engine.flames.luemens == 11.0
    
    with pytest.raises(ValueError):     
        empty_default_ship.engine.flames.size= "10"
        empty_default_ship.engine.flames.luemens = "11"
        #this is an integer and it is declared to be a float
        empty_default_ship.engine.flames.size = 10.0
        empty_default_ship.engine.flames.luemens = 11
    
# def test_get_empty_ensemble():
#     new_strand:RNAStrand = RNAStrand()
#     new_strand.ensemble = Ensemble()
#     assert new_strand.ensemble.mfe_structure.dot_parens == None

def test_single_ship_attribute(empty_default_ship:Spaceship):
    empty_default_ship.midsection.hatch.shape = 'AUGC'
    assert empty_default_ship.midsection.hatch.shape == 'AUGC'

# def test_new_thing(empty_default_ship:Spaceship):
#     empty_default_ship.primary_structure.jumping = "yo"# = new_struct
#     assert empty_default_ship.primary_structure.jumping == "yo"
#     assert empty_default_ship.primary_structure.jumping == "yo"
#     empty_default_ship.primary_structure.strand = "first time"
#     assert empty_default_ship.primary_structure.strand == "first time"
    
#     strand_two:Spaceship = Spaceship(var_name="its_fun",
#                           working_folder='/home/rnauser/repo/rna_squirrel/src/test/bin/data')
#     strand_two.primary_structure.strand = "AABAC"
#     assert strand_two.primary_structure.strand == "AABAC"
#     with pytest.raises(ValueError):     
#         empty_default_ship.primary_structure = "break"

def test_lists(empty_default_ship:Spaceship):
    new_list = []
    new_list.append(1) 
    new_list.append(2) 
    new_list.append(3) 
    empty_default_ship.midsection.fines.sizes = new_list
    assert empty_default_ship.midsection.fines.sizes == [1, 2, 3] 
    

def test_dicts(empty_default_ship:Spaceship):
    new_dict = {}
    new_dict[1] = "four"
    new_dict[2] = "three"
    empty_default_ship.midsection.hatch.window_size_versions = new_dict
    assert empty_default_ship.midsection.hatch.window_size_versions == {1:"four", 2:"three"}
    
def test_complex_dicts(empty_default_ship:Spaceship):
    new_dict = {}
    new_dict[1.3] = ["1",'2', '3']
    new_dict[1.5] = ['4','5','6']
    empty_default_ship.midsection.fines.color_lists = new_dict
    assert empty_default_ship.midsection.fines.color_lists == {1.3:["1",'2', '3'], 1.5:['4','5','6']}
    

def test_complex_lists(empty_default_ship:Spaceship):
    #first create the value you want
    test_struct:ExternalClassDemo = ExternalClassDemo(what_is_it="stuff",
                                                      how_many_are_there=2,
                                                      is_it_true=True)
    
    empty_default_ship.midsection.hatch.external_simple_list = [test_struct]
    
    # this = dict(empty_default_ship.primary_structure)
    # assert this == {}
    returned_list:List[ExternalClassDemo] = empty_default_ship.midsection.hatch.external_simple_list
    for item in returned_list:
        assert isinstance(item, ExternalClassDemo) == True
        assert item.what_is_it == "stuff"
        assert item.how_many_are_there == 2        
        assert item.is_it_true == True
    
def test_class_as_value(empty_default_ship:Spaceship):
    test_struct:ExternalClassDemo = ExternalClassDemo(what_is_it="stuff2",
                                                      how_many_are_there=5,
                                                      is_it_true=True)
    
    empty_default_ship.midsection.hatch.external_simple_value = test_struct
    
    assert isinstance(empty_default_ship.midsection.hatch.external_simple_value, ExternalClassDemo) == True
    assert empty_default_ship.midsection.hatch.external_simple_value.what_is_it == "stuff2"
    assert empty_default_ship.midsection.hatch.external_simple_value.how_many_are_there == 5        
    assert empty_default_ship.midsection.hatch.external_simple_value.is_it_true == True

def test_class_as_value_complex(empty_default_ship:Spaceship):
    test_struct:ExternalClassDemo = ExternalClassDemo(what_is_it="stuf3",
                                                      how_many_are_there=3,
                                                      is_it_true=False)
    test_complex:ComponentsDemo = ComponentsDemo(demo_thing=test_struct)
                                                                                                                                            
    empty_default_ship.midsection.hatch.external_complex_value = test_complex
    
    assert isinstance(empty_default_ship.midsection.hatch.external_complex_value, ComponentsDemo) == True
    assert isinstance(empty_default_ship.midsection.hatch.external_complex_value.demo_thing, ExternalClassDemo) == True
    assert empty_default_ship.midsection.hatch.external_complex_value.demo_thing.what_is_it == 'stuf3'
    assert empty_default_ship.midsection.hatch.external_complex_value.demo_thing.how_many_are_there == 3
    assert empty_default_ship.midsection.hatch.external_complex_value.demo_thing.is_it_true == False

    
    