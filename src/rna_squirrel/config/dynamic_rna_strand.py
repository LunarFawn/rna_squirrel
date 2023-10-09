"""
Class for defining a rna strand dynamically
"""

from attrs import define, field, Factory
from enum import Enum
from typing import TypeVar, List, Dict, Any, Protocol, Type
import pickle


T = TypeVar("T", bound=Enum)

class AtrClass(Enum):
    PARENT = "PARENT"
    CHILD = "CHILD"

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

@define(kw_only=True)
class GenericAttribute():
    atr_class:AtrClass = field()
    atr_type:Type = None
    atr_default_value:Any = None
    attributes:Enum = field()

class CustomAttribute():
    # def __init__(self, save_value: bool = False) -> None:
    #     super().__init__(save_value)
    def __init__(self, save_value:bool = False) -> None:
        self.do_save:bool = save_value

    def new_attr(self, atr: GenericAttribute) -> None:
        for attribute in atr.attributes:
            if atr.atr_class == AtrClass.PARENT:
                self.__setattr__(attribute.value, CustomAttribute(save_value=True))
            elif atr.atr_class == AtrClass.CHILD:
                self.__setattr__(attribute.value, atr.atr_default_value)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        #this is where to put the code to save to db
        super().__setattr__(__name, __value)
    
    def __getattribute__(self, __name: str) -> Any:
        #this is where to put the code to pull from db
        return super().__getattribute__(__name)
    #strand = "taco"

@define(kw_only=True)
class Nut():
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
            self.__setattr__(thing.value, CustomAttribute(save_value=True))
  
        
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
    
    
   