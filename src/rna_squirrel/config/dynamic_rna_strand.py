"""
Class for defining a rna strand dynamically
"""

from attrs import define, field, Factory
from enum import Enum
from typing import TypeVar, List, Dict, Any, Protocol
import pickle


T = TypeVar("T", bound=Enum)

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

class GenericAttribute():
    pass


@define(kw_only=True)
class Strand():
    enum_list: T = field()
    use_db:bool = field()
    # attributes:Dict[T, Any] = field()
    # @attributes.default
    # def _do_the_attributes(self):
    #     new_dict:Dict[T, Any] = {}
    #     for thing in self.enum_list:
    #         new_dict[thing] = None
    #         self.__setattr__(thing.name, None)
    #     return new_dict
  
    def __attrs_post_init__(self):
       for thing in self.enum_list:
            self.__setattr__(thing.name, None)
  
   
    # @property
    # def attributes(self):
    #     if self.use_db is True:
    #         #first pupulate property with
    #         #value from db
    #         pass
       
    #     return self._attributes
    
    # def set_attributes(self, atr:T, value:Any):
    #     self._attributes[atr] = value
    #     if self.use_db is True:
    #         #write value to property in db
    #         pass

    
    # @property
    # def attributes(self):
    #     return self._attributes

    # @attributes.setter
    # def attributes(self,type:T, value):
    #     self._attributes[type] = value
    
    # @attributes.on_setattr
    # def _do_the_next_thing(self, attribute, value):
    #     record_to_db(attribute=attribute, value=value)
    
    
   