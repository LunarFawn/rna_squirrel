"""

This has the classes for external class import testing

"""

from dataclasses import dataclass



@dataclass
class ExternalClassDemo():
    what_is_it:str
    how_many_are_there:int
    is_it_true: bool

@dataclass
class ComponentsDemo():
    demo_thing: ExternalClassDemo