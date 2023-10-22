import pytest

from rna_squirrel.config.rna_strand import Energy, PrimaryStructure, RNAStrand, Ensemble
CONFIG_PATH = '/home/rnauser/repo/rna_squirrel/src/test/bin/test_class.yaml'

@pytest.fixture
def empty_default_strand():
    return RNAStrand()

def test_get_empty_strand(empty_default_strand:RNAStrand):
    assert empty_default_strand.primary_structure.strand == None

def test_set_strand_attribute(empty_default_strand:RNAStrand):
    # new_struct:PrimaryStructure = PrimaryStructure(save_value=True)
    # new_struct.strand = "yo"
    empty_default_strand.primary_structure.strand = "yo"# = new_struct
    assert empty_default_strand.primary_structure.strand == "yo_from_db_returned"

# def test_get_empty_ensemble():
#     new_strand:RNAStrand = RNAStrand()
#     new_strand.ensemble = Ensemble()
#     assert new_strand.ensemble.mfe_structure.dot_parens == None
    