import pytest
from pathlib import Path

#from test.bin.built_api import Energy, PrimaryStructure, rna_strand, Ensemble
from test.bin.built_single_api_2 import RNAStruct
from will_this_work import WhatIsThis
CONFIG_PATH = '/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml'

@pytest.fixture
def empty_default_strand():
    return RNAStruct(var_name="rna_strand_1",
                      working_folder=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))

@pytest.fixture
def empty_what_strand():
    return WhatIsThis(var_name="what_1",
                      working_folder=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))


def test_get_empty_strand(empty_default_strand:RNAStruct):
    with pytest.raises(Exception):     
        assert empty_default_strand.primary_structure.strand == None

def test_set_strand_attribute(empty_default_strand:RNAStruct):
    # new_struct:PrimaryStructure = PrimaryStructure(save_value=True)
    # new_struct.strand = "yo"
    empty_default_strand.primary_structure.strand = "yo"
    assert empty_default_strand.primary_structure.strand == "yo"
    assert empty_default_strand.primary_structure.strand == "yo"

    empty_default_strand.ensemble.max_energy.kcal = 10.0
    assert empty_default_strand.ensemble.max_energy.kcal == 10.0
    
    with pytest.raises(ValueError):     
        empty_default_strand.ensemble.max_energy.kcal = "10"
        
        #this is an integer and it is declared to be a float
        empty_default_strand.ensemble.max_energy.kcal = 10
    
# def test_get_empty_ensemble():
#     new_strand:RNAStrand = RNAStrand()
#     new_strand.ensemble = Ensemble()
#     assert new_strand.ensemble.mfe_structure.dot_parens == None

def test_single_strand_attribute(empty_default_strand:RNAStruct):
    empty_default_strand.ensemble.mea_structure.dot_parens = 'AUGC'
    assert empty_default_strand.ensemble.mea_structure.dot_parens == 'AUGC'

def test_new_thing(empty_default_strand:RNAStruct):
    empty_default_strand.primary_structure.jumping = "yo"# = new_struct
    assert empty_default_strand.primary_structure.jumping == "yo"
    assert empty_default_strand.primary_structure.jumping == "yo"
    empty_default_strand.primary_structure.strand = "first time"
    assert empty_default_strand.primary_structure.strand == "first time"
    
    strand_two:RNAStruct = RNAStruct(var_name="its_fun",
                          working_folder='/home/rnauser/repo/rna_squirrel/src/test/bin/data')
    strand_two.primary_structure.strand = "AABAC"
    assert strand_two.primary_structure.strand == "AABAC"
    with pytest.raises(ValueError):     
        empty_default_strand.primary_structure = "break"

def test_lists(empty_default_strand:RNAStruct):
    new_list = []
    new_list.append(1) 
    new_list.append(2) 
    new_list.append(3) 
    empty_default_strand.ensemble.mfe_structure.structure_list = new_list
    assert empty_default_strand.ensemble.mfe_structure.structure_list == [1, 2, 3] 
    

def test_dicts(empty_default_strand:RNAStruct):
    new_dict = {}
    new_dict[1] = 4
    new_dict[2] = 3 
    empty_default_strand.ensemble.mfe_structure.structure_dict = new_dict
    assert empty_default_strand.ensemble.mfe_structure.structure_dict == {1:4, 2:3}
    
def test_complex_dicts(empty_default_strand:RNAStruct):
    new_dict = {}
    new_dict[1.3] = ["1",'2', '3']
    new_dict[1.5] = ['4','5','6']
    empty_default_strand.ensemble.energy_groups = new_dict
    assert empty_default_strand.ensemble.energy_groups == {1.3:["1",'2', '3'], 1.5:['4','5','6']}
    
def test_complex_what_dicts(empty_what_strand:WhatIsThis):
    new_dict = {}
    new_dict[1.3] = ["1",'2', '3']
    new_dict[1.5] = ['4','5','6']
    empty_what_strand.ensemble.energy_groups = new_dict
    assert empty_what_strand.ensemble.energy_groups == {1.3:["1",'2', '3'], 1.5:['4','5','6']}