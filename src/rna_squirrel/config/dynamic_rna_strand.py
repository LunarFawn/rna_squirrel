"""
Class for defining a rna strand dynamically
"""

from attrs import define, field, Factory
from enum import Enum
from typing import TypeVar, List, Dict, Any, Protocol, Type
import pickle

from rna_squirrel.config.nut_yaml_objects import AtrClass

from rna_squirrel.config.nut_filter_definitions import NutFilterDefinitions, ValueFlow

nut_filter:NutFilterDefinitions = NutFilterDefinitions()

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
    def __init__(self,parent:Any,source_name:str,atr_class:AtrClass,atr_type:Any,attr_name:str, save_value:bool = False, ) -> None:
        super().__init__(atr_class=atr_class,
                         atr_type=atr_type,
                         attribute=attr_name)
        self.do_save:bool = save_value
        self.parent_table:Any = None
        self.current_table:Any = None
        self._attrib_dict:Dict[str,Any] = {}
        self.parent:Any = parent
        self.source_name: str = source_name
        
    def new_attr(self, atr: GenericAttribute) -> None:
        # for attribute in atr.attributes:
        if atr.atr_class == AtrClass.PARENT:
            # self._attrib_dict[atr.attribute] = CustomAttribute(parent=getattr(self.parent, atr.attribute),
            #                                                    source_name=atr.attribute, 
            #                                                    save_value=True)
            self.__setattr__(atr.attribute, CustomAttribute(parent=getattr(self.parent, self.source_name),
                                                               source_name=atr.attribute,
                                                               save_value=True,
                                                               atr_class=atr.atr_class,
                                                               atr_type=atr.atr_type,
                                                               attr_name=atr.attribute))
            test = 1
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
            __value = nut_filter.filter(flow_direction=ValueFlow.OUTBOUND,
                              value=__value,
                              parent=self,
                              attr_name=__name)
            # if type(__value) == str:
            #     __value = f'{__value}_from_db'
        super().__setattr__(__name, __value)
    
    def __getattribute__(self, __name: str) -> Any:
        #this is where to put the code to pull from db
        #use parent table location to get current table
        #to get the attribute value
        name_end:str = __name[-3:]
        if name_end == '_db' or name_end == '_DB':
            #value = self.__dict__[__name]
            value = super().__getattribute__(__name)
            # if type(value) == str:
            #     value = f'{value}_returned'
            #     return value
            value = nut_filter.filter(flow_direction=ValueFlow.INBOUND,
                              value=value,
                              parent=self,
                              attr_name=__name)
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
    var_name:str = field()
    atr_class:AtrClass = AtrClass.NUT
    def __attrs_post_init__(self):
       for thing in self.enum_list:
            self.__setattr__(thing.value, CustomAttribute(parent=self,
                                                               source_name=thing.value,
                                                               save_value=True,
                                                               atr_type=Any,
                                                               atr_class=AtrClass.PARENT,
                                                               attr_name=thing.value))
