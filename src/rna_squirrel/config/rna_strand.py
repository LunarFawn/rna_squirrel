"""
File that defines the main RNA sequence data
"""

from attrs import define, field
from typing import List


from rna_squirrel.config.nupack_config import NupackStrand, Strand_Attributes

@define
class Energy():
    kcal: float = 0

@define
class PrimaryStructure():
    strand: str = ''

@define
class SecondaryStructure():
    dot_parens: str = ''
    free_energy: Energy = Energy()
    stack_energy: Energy = Energy()

@define
class EnergyGroup():
    min_energy:Energy = Energy()
    max_energy:Energy = Energy()
    structure_list: List[SecondaryStructure] = []
    mfe_structure:SecondaryStructure = SecondaryStructure()
    mea_structure:SecondaryStructure = SecondaryStructure()
  

@define
class Ensemble():
    min_energy:Energy = Energy()
    max_energy:Energy = Energy()
    mfe_structure:SecondaryStructure = SecondaryStructure()
    mea_structure:SecondaryStructure = SecondaryStructure()
    

#@define
class RNAStrand():
    
    def __init__(self) -> None:
        self.primary_structure: PrimaryStructure
        self.ensemble:Ensemble# = Ensemble()
        
        self.strand:NupackStrand = NupackStrand(enum_list=Strand_Attributes)
    
    @property
    def primary_structure(self):
        return self.strand.attributes[Strand_Attributes.PrimaryStructure]
        
    @primary_structure.setter
    def primary_structure(self, struct):
        self.strand.attributes[Strand_Attributes.PrimaryStructure] = struct
    
    @property
    def ensemble(self):
        return self.strand.attributes[Strand_Attributes.Ensemble]
        
    @ensemble.setter
    def ensemble(self, ensemble:Ensemble):
        self.strand.set_attributes(Strand_Attributes.Ensemble, ensemble)