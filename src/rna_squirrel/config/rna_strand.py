"""
File that defines the main RNA sequence data
"""

from attrs import define, field
from typing import List
from collections import namedtuple

@define
class Energy():
    kcal: float = 0

@define
class PrimaryStructure():
    strand: str = ''

@define
class SecondaryStructure():
    dot_parens: str
    free_energy: Energy = Energy()
    stack_energy: Energy = Energy()

@define
class EnergyGroup():
    min_energy:Energy = Energy()
    max_energy:Energy = Energy()
    structure_list: List[SecondaryStructure] = []
    mfe_structure:SecondaryStructure = SecondaryStructure()
    mea_structure:SecondaryStructure = SecondaryStructure()
    
    def add_structure(self, structure:SecondaryStructure):
        """
        add a secondary structure to the energy group
        """
        self.structure_list.append(structure)
        
class EnsembleGroup(namedtuple):
    start_energy: float
    group:EnergyGroup

@define
class Ensemble():
    min_energy:Energy = Energy()
    max_energy:Energy = Energy()
    energy_groups:List[EnsembleGroup] = []
    mfe_structure:SecondaryStructure = SecondaryStructure()
    mea_structure:SecondaryStructure = SecondaryStructure()
    
    def add_group(self, start_energy:float, group:EnergyGroup):
        """
        Add a energy group with its label to the ensemble 
        """
        new_group: EnsembleGroup = EnsembleGroup(start_energy, group)
        self.energy_groups.append(new_group)
        

@define
class RNAStrand():
    primary_structure: PrimaryStructure
    ensemble: Ensemble = Ensemble()
