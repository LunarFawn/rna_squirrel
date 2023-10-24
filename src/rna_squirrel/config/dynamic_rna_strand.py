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
    #atr_default_value:Any = None
    #attributes:Enum = field()
    attribute:str = field()
    
class CustomAttribute(GenericAttribute):
    """
    I think that each CustomAttribute needs
    to spin up its own new table but needs to be 
    traceable
    """
    # def __init__(self, save_value: bool = False) -> None:
    #     super().__init__(save_value)
    def __init__(self, save_value:bool = False) -> None:
        super().__init__(atr_class=AtrClass.PARENT,
                         atr_type=None,
                         attribute='')
        self.do_save:bool = save_value
        self.parent_table:Any = None
        self.current_table:Any = None
        self._attrib_dict:Dict[str,Any] = {}
    def new_attr(self, atr: GenericAttribute) -> None:
        # for attribute in atr.attributes:
        if atr.atr_class == AtrClass.PARENT:
            self._attrib_dict[atr.attribute] = CustomAttribute(save_value=True)
            self.__setattr__(atr.attribute, CustomAttribute(save_value=True))
        elif atr.atr_class == AtrClass.CHILD:
            self._attrib_dict[atr.attribute] = None
            self.__setattr__(atr.attribute, None)
    
    def get_custom_attr(self, name:str):
        return self._attrib_dict[name]
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        #this is where to put the code to save to db
        #use parent table location to place current
        #table data
        
        #if setattr value is None then do not update 
        #the db
        name_end:str = __name[-3:]
        if name_end == '_db' or name_end == '_DB':
            if type(__value) == str:
                __value = f'{__value}_from_db'
        super().__setattr__(__name, __value)
    
    def __getattribute__(self, __name: str) -> Any:
        #this is where to put the code to pull from db
        #use parent table location to get current table
        #to get the attribute value
        name_end:str = __name[-3:]
        if name_end == '_db' or name_end == '_DB':
            #value = self.__dict__[__name]
            value = super().__getattribute__(__name)
            if type(value) == str:
                value = f'{value}_returned'
                return value
            return value
        else:
            return super().__getattribute__(__name)
    
        
    def new_table(self):
        pass
    #strand = "taco"

@define(kw_only=True)
class Nut():
    enum_list: T = field()
    use_db:bool = field()
    db:Any = field()
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
    
