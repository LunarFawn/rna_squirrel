"""
Class for defining a rna strand dynamically
"""

from attrs import define, field
from typing import TypeVar, List


T = TypeVar("T")

@define
class Value():
    name:str
    value:str

@define
class Object():
    pass

@define
class Group():
    objects:List[T]



@define
class Strand():
    