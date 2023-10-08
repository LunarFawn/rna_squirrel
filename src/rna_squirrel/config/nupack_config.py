"""
File that contains the Enums and
config files for rna squirrel to use nupack.
The idea is that any config can be used
for a generic system for later extensability
"""

from enum import Enum
from typing import TypeVar, Type, List
from attrs import define, field
from rna_squirrel.config.dynamic_rna_strand import (
    Nut,
    Value,
    GenericAttribute,
    AtrClass,
    CustomAttribute
)

OBJECT_TYPE = None

"""
Pickle and unpickle
"""

class Nut_Attributes(Enum):
    """
    This is a common attribute that
    needs to be published for the dynamic
    strand to build the correct object
    """
    PrimaryStructure = "PrimaryStructure"
    Ensemble = "Ensemble"

class PrimaryStructure_Attributes(Enum):
    Strand = "Strand"
    
# class PrimaryStructure_Stats(GenericAttribute):
#     atr_class:AtrClass = AtrClass.PARENT
#     atr_type:Type = None
#     attributes:Enum = PrimaryStructure_Attributes
    
#     def __init__(self) -> None:
#         super().__init__(atr_class=self.atr_class,
#                          atr_type=self.atr_type)

class NupackStrand(Nut):
    enum_list = Nut_Attributes

