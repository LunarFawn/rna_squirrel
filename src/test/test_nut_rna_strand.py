import pytest

#from test.bin.built_api import Energy, PrimaryStructure, rna_strand, Ensemble
from test.bin.built_single_api import rna_strand
CONFIG_PATH = '/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml'

@pytest.fixture
def empty_default_strand():
    return rna_strand(var_name="I am RNA")

def test_get_empty_strand(empty_default_strand:rna_strand):
    assert empty_default_strand.primary_structure.strand == None

def test_set_strand_attribute(empty_default_strand:rna_strand):
    # new_struct:PrimaryStructure = PrimaryStructure(save_value=True)
    # new_struct.strand = "yo"
    empty_default_strand.primary_structure.strand = "yo"# = new_struct
    assert empty_default_strand.primary_structure.strand == "yo_from_db_returned"
    assert empty_default_strand.primary_structure.strand == "yo_from_db_returned"

    empty_default_strand.ensemble.max_energy = '10'
    assert empty_default_strand.ensemble.max_energy == '10_from_db_returned'
    assert empty_default_strand.primary_structure.strand == "yo_from_db_returned"
# def test_get_empty_ensemble():
#     new_strand:RNAStrand = RNAStrand()
#     new_strand.ensemble = Ensemble()
#     assert new_strand.ensemble.mfe_structure.dot_parens == None

def test_single_strand_attribute(empty_default_strand:rna_strand):
    empty_default_strand.ensemble.mea_structure = 'AUGC'
    assert empty_default_strand.ensemble.mea_structure == 'AUGC_from_db_returned'

def test_new_thing(empty_default_strand:rna_strand):
    empty_default_strand.primary_structure.jumping = "yo"# = new_struct
    assert empty_default_strand.primary_structure.jumping == "yo_from_db_returned"
    assert empty_default_strand.primary_structure.jumping == "yo_from_db_returned"
    