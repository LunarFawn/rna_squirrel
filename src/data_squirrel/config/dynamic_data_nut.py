"""
Class for defining a rna strand dynamically
"""

from attrs import define, field, Factory
from enum import Enum
from typing import TypeVar, List, Dict, Any, Protocol, Type
from pathlib import Path
import pickle

from data_squirrel.config.nut_yaml_objects import AtrClass, GenericAttribute, ValuePacket

from data_squirrel.config.nut_filter_definitions import NutFilterDefinitions, ValueFlow

from data_squirrel.config.nut_data_manager import init_variable_folder

#nut_filter:NutFilterDefinitions = NutFilterDefinitions(working_dir=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))

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


class CustomAttribute(GenericAttribute):
    """
    I think that each CustomAttribute needs
    to spin up its own new table but needs to be 
    traceable
    """
    # def __init__(self, save_value: bool = False) -> None:
    #     super().__init__(save_value)
    def __init__(self,parent:Any,source_name:str,atr_class:AtrClass,atr_type:Any,attr_name:str,nut_filter:NutFilterDefinitions, save_value:bool = False, ) -> None:
        super().__init__(atr_class=atr_class,
                         atr_type=atr_type,
                         attribute=attr_name)
        self.do_save:bool = save_value
        self.parent_table:Any = None
        self.current_table:Any = None
        
        #this is for the  new attriburtes dict 
        self._parent_list:List[str] = []
        self._child_list:List[str] = []
        self._child_type_dict:Dict[str,Any] = {}        
        self._child_address_dict:Dict = {}
        self._child_values_dict:Dict[str,Any] = {}
        
        
        self._attrib_dict:Dict[str,Any] = {}
        self._parent:Any = parent
        self.source_name: str = source_name
        self._nut_filter:NutFilterDefinitions = nut_filter
    
    @property
    def nut_filter(self)->NutFilterDefinitions:
        return self._nut_filter
    
    @property
    def child_list(self):
        return self._child_list
    
    @property
    def child_types(self):
        return self._child_type_dict
    
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, thing:Any):
        self._parent = thing
       
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
                                                               attr_name=atr.attribute,
                                                               nut_filter=self.nut_filter))
            self._parent_list.append(atr.attribute)
            test = 1        
        elif atr.atr_class == AtrClass.CHILD:
            self._child_list.append(atr.attribute)
            self._attrib_dict[atr.attribute] = None

            self.__setattr__(atr.attribute, None)
        return self
    
    def __iter__(self):
        list_of_items:List[str] = self.parent._child_list
        return_dict = {}
        
        for item in list_of_items:
            attribute = self.parent.__getattribute__(item)
            return_dict[item] = attribute
        
        # for key in self.parent.__dict__:
        #     attribute:CustomAttribute = self.parent.__dict__[key]
        #     if isinstance(attribute, CustomAttribute) == True:
        #         if attribute.atr_class == AtrClass.CHILD:
        #             return_dict[attribute.attribute] = getattr(self, attribute.attribute)
        
        return return_dict
    
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
            
            if isinstance(__value, CustomAttribute) != True:
                #cant use hasattr becuase that will trigger get attribute and 
                #need to work on packet routing better before that
                if __name in list(self.__dict__.keys()):
                    this_attr = self.__dict__[__name]
                    if isinstance(this_attr, CustomAttribute) == True:
                        raise ValueError("Unable to assign value to parent container backend")
                self._child_type_dict[__name] = type(__value)        
                __value:ValuePacket = ValuePacket(name=__name,
                                        value=__value,
                                        parent=self,
                                        this_type=type(__value))
            # else:
            #     test_value:CustomAttribute = __value
            #     if test_value.atr_class == AtrClass.PARENT:
            #         

            __value = self.nut_filter.filter(flow_direction=ValueFlow.OUTBOUND,
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
            if isinstance(value, CustomAttribute) == False:
                value:ValuePacket = ValuePacket(name=None,
                                        value=None,
                                        parent=None,
                                        this_type=None)
            # if type(value) == str:
            #     value = f'{value}_returned'
            #     return value
            value = self.nut_filter.filter(flow_direction=ValueFlow.INBOUND,
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
    working_folder:Path = field()
    atr_class:AtrClass = AtrClass.NUT
    nut_filter:NutFilterDefinitions = field(init=False)#NutFilterDefinitions(working_dir=Path('/home/rnauser/repo/rna_squirrel/src/test/bin/data'))
    
    def __attrs_post_init__(self):
        self.nut_filter = NutFilterDefinitions(working_dir=self.working_folder)
        init_variable_folder(working_folder=self.working_folder,
                                nut_name=self.var_name)        
        for thing in self.enum_list:
                self.__setattr__(thing.value, CustomAttribute(parent=self,
                                                            source_name=thing.value,
                                                            save_value=True,
                                                            atr_type=Any,
                                                            atr_class=AtrClass.PARENT,
                                                            attr_name=thing.value,
                                                            nut_filter=self.nut_filter))
