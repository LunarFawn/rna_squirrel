"""
File that contains the Enums and
config files for rna squirrel to use nupack.
The idea is that any config can be used
for a generic system for later extensability
"""

from enum import Enum
from typing import TypeVar, Type, List
from attrs import define, field
from data_squirrel.config.dynamic_data_nut import (
    Nut,
    Value,
    GenericAttribute,
    AtrClass,
    CustomAttribute
)

OBJECT_TYPE = None

class Nut_Attributes(Enum):
    """
    This is a common attribute that
    needs to be published for the dynamic
    strand to build the correct object
    """
    PrimaryStructure = "primaryStructure_db"
    Ensemble = "ensemble_DB"

class PrimaryStructure_Attributes(Enum):
    Strand = "strand_DB"
    
# class PrimaryStructure_Stats(GenericAttribute):
#     atr_class:AtrClass = AtrClass.PARENT
#     atr_type:Type = None
#     attributes:Enum = PrimaryStructure_Attributes
    
#     def __init__(self) -> None:
#         super().__init__(atr_class=self.atr_class,
#                          atr_type=self.atr_type)

class NupackStrand(Nut):

    def __init__(self, use_db:bool = False) -> None:
        super().__init__(enum_list=Nut_Attributes,
                         use_db=True,
                         db=None)
    
        #build the Primary Structure first
        #dont forget that at this point the NUT container exits
        #we just need to add attributes
        #and if it is a class then it will populate new option
        #for us
        self.primaryStructure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
                                        attribute="strand_DB",
                                        atr_type=str))
    

