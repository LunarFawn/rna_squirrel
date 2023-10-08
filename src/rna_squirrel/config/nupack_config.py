"""
File that contains the Enums and
config files for rna squirrel to use nupack.
The idea is that any config can be used
for a generic system for later extensability
"""

from enum import Enum
from typing import TypeVar
from attrs import define, field
from rna_squirrel.config.dynamic_rna_strand import Strand, Value

OBJECT_TYPE = None

"""
Pickle and unpickle
"""

class Strand_Attributes(Enum):
    """
    This is a common attribute that
    needs to be published for the dynamic
    strand to build the correct object
    """
    PrimaryStructure = "PrimaryStructure"
    Ensemble = "Ensemble"



@define
class NupackStrand(Strand):
    pass

