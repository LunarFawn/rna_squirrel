"""
File that defines the main RNA sequence data
"""

from attrs import define, field
from collections import namedtuple
from typing import List, Dict


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
class EnsembleGroup(EnergyGroup):
    start_energy: float = 0
    

@define
class Ensemble():
    min_energy:Energy = Energy()
    max_energy:Energy = Energy()
    # energy_groups:List[EnsembleGroup] = []
    energy_groups:Dict[Energy, EnergyGroup] = {}
    mfe_structure:SecondaryStructure = SecondaryStructure()
    mea_structure:SecondaryStructure = SecondaryStructure()
    

#@define
class RNAStrand():
    
    def __init__(self, use_db:bool = False) -> None:
        self.primary_structure: PrimaryStructure
        self.ensemble:Ensemble# = Ensemble()
        self.strand:NupackStrand = NupackStrand(enum_list=Strand_Attributes,
                                                use_db=use_db)
    
    @property
    def primary_structure(self):
        #return self.strand.attributes[Strand_Attributes.PrimaryStructure]
        return self.strand.PrimaryStructure
        
    @primary_structure.setter
    def primary_structure(self, struct:PrimaryStructure):
        self.strand.PrimaryStructure = struct
    
    @property
    def ensemble(self):
        # return self.strand.attributes[Strand_Attributes.Ensemble]
        return self.strand.Ensemble
        
    @ensemble.setter
    def ensemble(self, ensemble:Ensemble):
        # self.strand.set_attributes(atr=Strand_Attributes.Ensemble,
        #                            value=ensemble)
        self.strand.Ensemble = ensemble