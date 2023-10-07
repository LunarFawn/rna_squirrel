"""
File that contains the Enums and
config files for rna squirrel to use nupack.
The idea is that any config can be used
for a generic system for later extensability
"""

from enum import Enum
from typing import TypeVar

OBJECT_TYPE = None



class Strand_Attributes(Enum):
    PrimaryStructure = "PrimaryStructure"
    Ensemble = "Ensemble"