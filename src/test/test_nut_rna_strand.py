import pytest
from pathlib import Path
from typing import List

#from test.bin.built_api import Energy, PrimaryStructure, rna_strand, Ensemble
from test.bin.built_single_api_2 import RNAStruct, PrimaryStructure

import serena.utilities.ensemble_structures

from serena.utilities.ensemble_structures import Sara2SecondaryStructure
from serena.interfaces.Sara2_API_Python3 import DesignPerformanceData, DesignInformation, WetlabData

CONFIG_PATH = '/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml'

@pytest.fixture
def empty_default_strand():
    return RNAStruct(var_name="rna_strand_1",
                      working_folder=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))

# @pytest.fixture
# def empty_what_strand():
#     return WhatIsThis(var_name="what_1",
#                       working_folder=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))


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
    

def test_complex_lists(empty_default_strand:RNAStruct):
    #first create the value you want
    test_struct:serena.utilities.ensemble_structures.Sara2SecondaryStructure = serena.utilities.ensemble_structures.Sara2SecondaryStructure(sequence='AACCUUGG',
                                                                                                                                            structure='...()...',
                                                                                                                                            free_energy=-10,
                                                                                                                                            stack_energy=-20)
    
    empty_default_strand.primary_structure_lists.primary_list = [test_struct]
    
    # this = dict(empty_default_strand.primary_structure)
    # assert this == {}
    returned_list:List[serena.utilities.ensemble_structures.Sara2SecondaryStructure] = empty_default_strand.primary_structure_lists.primary_list
    for item in returned_list:
        assert isinstance(item, serena.utilities.ensemble_structures.Sara2SecondaryStructure) == True
        assert item.sequence == "AACCUUGG"
        assert item.structure == '...()...'        
        assert item.free_energy == -10
        assert item.stack_energy == -20
    
def test_class_as_value(empty_default_strand:RNAStruct):
    test_struct:serena.utilities.ensemble_structures.Sara2SecondaryStructure = serena.utilities.ensemble_structures.Sara2SecondaryStructure(sequence='AACCUUGG',
                                                                                                                                            structure='...()...',
                                                                                                                                            free_energy=-10,
                                                                                                                                            stack_energy=-20)
    empty_default_strand.secondary_structure_stuff.secondary_structure = test_struct
    
    assert isinstance(empty_default_strand.secondary_structure_stuff.secondary_structure, serena.utilities.ensemble_structures.Sara2SecondaryStructure) == True
    assert empty_default_strand.secondary_structure_stuff.secondary_structure.sequence == "AACCUUGG"
    assert empty_default_strand.secondary_structure_stuff.secondary_structure.structure == '...()...'        
    assert empty_default_strand.secondary_structure_stuff.secondary_structure.free_energy == -10
    assert empty_default_strand.secondary_structure_stuff.secondary_structure.stack_energy == -20

def test_class_as_value_complex(empty_default_strand:RNAStruct):
    test_info:DesignInformation = DesignInformation(Sequence='AACCGGUU')
    test_wet:WetlabData = WetlabData(Eterna_Score=99)
    performance:DesignPerformanceData = DesignPerformanceData(DesignInfo=test_info,
                                                              wetlabResults=test_wet)
                                                                                                                                            
    empty_default_strand.secondary_structure_stuff.performance_info = performance
    
    assert isinstance(empty_default_strand.secondary_structure_stuff.performance_info, DesignPerformanceData) == True
    assert isinstance(empty_default_strand.secondary_structure_stuff.performance_info.design_info, DesignInformation) == True
    assert empty_default_strand.secondary_structure_stuff.performance_info.design_info.Sequence == 'AACCGGUU'
    assert isinstance(empty_default_strand.secondary_structure_stuff.performance_info.wetlab_results, WetlabData) == True
    assert empty_default_strand.secondary_structure_stuff.performance_info.wetlab_results.Eterna_Score == 99
    
    