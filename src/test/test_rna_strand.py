import pytest

from rna_squirrel.config.rna_strand import Energy, PrimaryStructure, RNAStrand, Ensemble


def test_get_empty_strand():
    new_strand:RNAStrand = RNAStrand()
    assert new_strand.primary_structure.strand == "yes?"

def test_set_strand_attribute():
    new_strand:RNAStrand = RNAStrand()
    # new_struct:PrimaryStructure = PrimaryStructure(save_value=True)
    # new_struct.strand = "yo"
    new_strand.primary_structure.strand = "yo"# = new_struct
    assert new_strand.primary_structure.strand == "yo"

def test_get_empty_ensemble():
    new_strand:RNAStrand = RNAStrand()
    new_strand.ensemble = Ensemble()
    assert new_strand.ensemble.mfe_structure.dot_parens == ''
    