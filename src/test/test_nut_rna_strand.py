import pytest

#from test.bin.built_api import Energy, PrimaryStructure, rna_strand, Ensemble
from test.bin.built_single_api_2 import RNAStrand
CONFIG_PATH = '/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml'

@pytest.fixture
def empty_default_strand():
    return RNAStrand(var_name="rna_strand_1",
                      working_folder='/home/rnauser/repo/rna_squirrel/src/test/bin/data')

def test_get_empty_strand(empty_default_strand:RNAStrand):
    with pytest.raises(Exception):     
        assert empty_default_strand.primary_structure.strand == None

def test_set_strand_attribute(empty_default_strand:RNAStrand):
    # new_struct:PrimaryStructure = PrimaryStructure(save_value=True)
    # new_struct.strand = "yo"
    empty_default_strand.primary_structure.strand = "yo"# = new_struct
    assert empty_default_strand.primary_structure.strand == "yo_returned"
    assert empty_default_strand.primary_structure.strand == "yo_returned"

    empty_default_strand.ensemble.max_energy.kcal = '10'
    assert empty_default_strand.ensemble.max_energy.kcal  == '10_returned'
    assert empty_default_strand.primary_structure.strand == "yo_returned"
# def test_get_empty_ensemble():
#     new_strand:RNAStrand = RNAStrand()
#     new_strand.ensemble = Ensemble()
#     assert new_strand.ensemble.mfe_structure.dot_parens == None

def test_single_strand_attribute(empty_default_strand:RNAStrand):
    empty_default_strand.ensemble.mea_structure.dot_parens = 'AUGC'
    assert empty_default_strand.ensemble.mea_structure.dot_parens == 'AUGC_returned'

def test_new_thing(empty_default_strand:RNAStrand):
    empty_default_strand.primary_structure.jumping = "yo"# = new_struct
    assert empty_default_strand.primary_structure.jumping == "yo_returned"
    assert empty_default_strand.primary_structure.jumping == "yo_returned"
    empty_default_strand.primary_structure.strand = "first time"
    assert empty_default_strand.primary_structure.strand == "first time_returned"
    
    strand_two:RNAStrand = RNAStrand(var_name="its_fun",
                          working_folder='/home/rnauser/repo/rna_squirrel/src/test/bin/data')
    strand_two.primary_structure.strand = "AABAC"
    assert strand_two.primary_structure.strand == "AABAC_returned"