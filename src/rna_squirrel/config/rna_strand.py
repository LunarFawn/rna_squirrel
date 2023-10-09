"""
File that defines the main RNA sequence data
"""

from attrs import define, field
from collections import namedtuple
from typing import List, Dict, Any


from rna_squirrel.config.nupack_config import (
    NupackStrand,
    Nut_Attributes,
    PrimaryStructure_Attributes,
)
from rna_squirrel.config.dynamic_rna_strand import (
    Nut,
    Value,
    GenericAttribute,
    AtrClass,
    CustomAttribute
)

@define
class Energy():
    kcal: float = 0


class PrimaryStructure(CustomAttribute):

    def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
        #self._strand: str = ''
        self.parent = parent
        self.current = current
        self.do_save = save_value
        
    @property
    def strand(self):
        #return self.Strand_DB
        return self.parent.PrimaryStructure_DB.Strand_DB
    
    @strand.setter
    def strand(self, value:str):
        #self.Strand_DB = value
        self.parent.PrimaryStructure_DB.Strand_DB = value

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
class Ensemble(CustomAttribute):
    min_energy:Energy = Energy()
    max_energy:Energy = Energy()
    # energy_groups:List[EnsembleGroup] = []
    energy_groups:Dict[Energy, EnergyGroup] = {}
    mfe_structure:SecondaryStructure = SecondaryStructure()
    mea_structure:SecondaryStructure = SecondaryStructure()
    

#@define
class RNAStrand(Nut):
    
    def __init__(self, use_db:bool = False) -> None:
        super().__init__(enum_list=Nut_Attributes,
                         use_db=True,
                         db=None)
        self._primary_structure: PrimaryStructure = PrimaryStructure(save_value=True,
                                                                     current=None,
                                                                     parent=self)
        self.ensemble:Ensemble# = Ensemble()
        # self.strand:NupackStrand = NupackStrand(enum_list=Strand_Attributes,
        #                                         use_db=use_db)
        
        
        #build the Primary Structure first
        self.PrimaryStructure_DB.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
                                        attributes=PrimaryStructure_Attributes,
                                        atr_type=str,
                                        atr_default_value='yes?'))

        self._primary_structure.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
                                        attributes=PrimaryStructure_Attributes,
                                        atr_type=str,
                                        atr_default_value='empty'))
        
    @property
    def primary_structure(self)->PrimaryStructure:
        #return PrimaryStructure(strand=self.PrimaryStructure_DB.Strand_DB)
        return self._primary_structure
        
    @primary_structure.setter
    def primary_structure(self, struct:PrimaryStructure):
        #self.PrimaryStructure_DB.Strand_DB = struct.strand
        self._primary_structure = struct
    
    @property
    def ensemble(self):
        # return self.strand.attributes[Strand_Attributes.Ensemble]
        return self.Ensemble_DB
        
    @ensemble.setter
    def ensemble(self, ensemble:Ensemble):
        # self.strand.set_attributes(atr=Strand_Attributes.Ensemble,
        #                            value=ensemble)
        self.Ensemble_DB = ensemble