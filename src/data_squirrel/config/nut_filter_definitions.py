"""
File to hold teh default classes for manipulating
data that goes throught the setter and getter
of the dynamic backend
"""
from typing import Any, Dict, List

from enum import Enum
import heapq
from pathlib import Path
from dataclasses import dataclass, field

from data_squirrel.config.nut_yaml_objects import (
    AtrClass,
    ValuePacket,
    GenericAttribute, 
    String,
    Integer,
    FloatingPoint,
    NutObjectType,
    Dictionary,
    ListOfThings
)
from data_squirrel.config.nut_data_manager import YamlDataOperations

class ValueFlow(Enum):
    OUTBOUND="OUTBOUND"
    INBOUND="INBOUND"
    BOTH="BOTH"

@dataclass
class AddressInfo():
    name:str
    address_list: List[str]
    working_folder:Path 
    address_string:str = field(init=False)
    address_file_path: Path = field(init=False)
    
    def __post_init__(self) -> None:
        self.address_string = f'{"_".join(self.address_list)}.yaml'
        self.address_file_path = self.working_folder.joinpath(self.address_list[-1],self.address_string)
        
        
class NutFilterDefinitions():

    def __init__(self, working_dir:Path) -> None:
        self.working_dir:Path = working_dir
        self.yaml_operations:YamlDataOperations = YamlDataOperations()
    
    def filter(self, parent:Any, attr_name:str, value:Any, flow_direction:ValueFlow):
        new_value:Any = value
        
        routing:NutAdressing = NutAdressing()
        jump_list: List[str] = routing.get_attr_address(parent_attr=parent,
                                 name=attr_name)
        address_info:AddressInfo = AddressInfo(address_list=jump_list,
                                               working_folder=self.working_dir,
                                               name=attr_name)
        #heapq.heapify(jump_list)
        
        if flow_direction == ValueFlow.OUTBOUND:
            new_value = self.filter_out_flow(value=new_value,
                                             address=address_info,
                                             ops=self.yaml_operations)
        elif flow_direction == ValueFlow.INBOUND:
            new_value = self.filter_in_flow(value=new_value,
                                            address=address_info,
                                            ops=self.yaml_operations)
        
        
        return new_value
        
    def filter_both_flow(self, value:Any):
        new_value:Any = value
        return new_value
    
    def filter_out_flow(self, value:Any, address:AddressInfo, ops:YamlDataOperations):
        """
        This is the 
        """

        new_value:Any = value
        if isinstance(value, ValuePacket) == True:
            #this is a value and not a parent custom attribe
            packet:ValuePacket = value
            new_value = packet.value
            is_valid:bool = False
            preped_data: Any = None
            if packet.value_type == str:
                preped_data = String(value=packet.value)
                is_valid = True
                #now save it to the yaml at the file target
            if packet.value_type == int:
                preped_data = Integer(value=packet.value)
                is_valid = True
            if packet.value_type == float:
                preped_data = FloatingPoint(value=packet.value)
                is_valid = True
            
            """
            new 1-16-24 work
            check if python dict type and then test key and value pair to see what it is for proper routing
            I either need to allow any type like python does or trongly type the dicts moving away from python a bit
            but I think strongly typed python sounds not bad....
            """
            if packet.value_type == dict:
                #test the types of the key and value
                #first check that it is a dict
                raw_dict:Dict[Any,Any] = packet.value
                
                dict_keys:List[Any] = list(raw_dict.keys())
                dict_values:List[Any] = list(raw_dict.values())
                
                #should really do a for keys and then build a string dict
                #that can be easily sent to yaml as well as be 
                #checked properly
                golden_key = dict_keys[0]
                keys_type:NutObjectType = NutObjectType.VALUE
                if type(golden_key) == str:
                    keys_type:NutObjectType = NutObjectType.STRING
                    #now save it to the yaml at the file target
                elif type(golden_key) == int:
                    keys_type:NutObjectType = NutObjectType.INTEGER
                elif type(golden_key) == float:
                    keys_type:NutObjectType = NutObjectType.FLOATINGPOINT
                elif type(golden_key) == list:
                    keys_type:NutObjectType = NutObjectType.LIST
                else:
                    found_type_key = type(golden_key)
                    raise TypeError(f'{golden_key} is type:{found_type_key} and that is not supported yet')
                
                value_type:NutObjectType = NutObjectType.VALUE
                if type(raw_dict[golden_key]) == str:
                    value_type:NutObjectType = NutObjectType.STRING
                    #now save it to the yaml at the file target
                elif type(raw_dict[golden_key]) == int:
                    value_type:NutObjectType = NutObjectType.INTEGER
                elif type(raw_dict[golden_key]) == float:
                    value_type:NutObjectType = NutObjectType.FLOATINGPOINT
                elif type(raw_dict[golden_key]) == list:
                    value_type:NutObjectType = NutObjectType.LIST
                else:
                    found_type_value = type(raw_dict[golden_key])
                    raise TypeError(f'{raw_dict[golden_key]} is type:{found_type_value} and that is not supported yet')
                
                temp_dict:Dict[str,str] = {}
                for key, value in raw_dict.items():
                    # temp_dict[str(key)] = str(value)   
                    temp_dict[key] = value              
                
                yaml_dict:Dictionary = Dictionary(key_def=keys_type,
                                                  value_def=value_type,
                                                  value=temp_dict)
                
                is_valid = True
                preped_data = yaml_dict
            
            if packet.value_type == list:
                raw_list:List[Any] = packet.value
                golden_item = raw_list[0]
                item_type:NutObjectType = NutObjectType.VALUE
                if type(golden_item) == str:
                    item_type:NutObjectType = NutObjectType.STRING
                    #now save it to the yaml at the file target
                elif type(golden_item) == int:
                    item_type:NutObjectType = NutObjectType.INTEGER
                elif type(golden_item) == float:
                    item_type:NutObjectType = NutObjectType.FLOATINGPOINT
                else:
                    found_type_item = type(golden_item)
                    raise TypeError(f'{golden_item} is type:{found_type_item} and that is not supported yet')
                
                temp_list:List[str] = []
                
                for item in raw_list:
                    temp_list.append(str(item))
                
                yaml_list:ListOfThings = ListOfThings(value_def=item_type,
                                                    value=temp_list)  
                
                is_valid = True
                preped_data = yaml_list
            
            #this is supper old...maybe get ride off
            # if packet.value == None:
            #     preped_data = Empty()
            #     is_valid = True
                                
            if is_valid == True:
                ops.save_data(data=preped_data,
                                working_folder=address.working_folder,
                                nut_name=address.address_list[-1],
                                filename=address.address_file_path)
            else:
                if packet.value != None:
                    raise ValueError("Unsupported value type. Please update and try again maybe?")
            #new_value = f'{new_value}_from_db'
            # new_value = None
        else:
            #it is a parent struct
            pass     
       
        return new_value
    
    def filter_in_flow(self,  value:Any, address:AddressInfo, ops:YamlDataOperations):
        """
        This is the 
        """
        new_value:Any = value
        
        if isinstance(value, ValuePacket) == True:
            # if value.value != None:
            new_data = ops.read_data(working_folder=address.working_folder,
                        nut_name=address.address_list[-1],
                        filename=address.address_file_path)
            if isinstance(new_data, String) == True:
                new_value = new_data.value
            if isinstance(new_data, Integer) == True:
                new_value = new_data.value
            if isinstance(new_data, FloatingPoint) == True:
                new_value = new_data.value     
            if isinstance(new_data, Dictionary) == True:
                key_def:NutObjectType = new_data.key_def
                value_def:NutObjectType = new_data.value_def
                temp_value:Dict[str,str] = new_data.value
                
                temp_dict = {}
                for key, value in temp_value.items():
                    recoverd_key = None
                    recoverd_value = None
                    if key_def == NutObjectType.STRING:
                        recoverd_key = str(key)
                    elif key_def == NutObjectType.INTEGER:
                        recoverd_key = int(key)
                    elif key_def == NutObjectType.FLOATINGPOINT:
                        recoverd_key = float(key)
                    elif key_def == NutObjectType.LIST:
                        recoverd_key = list(key)
                    else:
                        raise TypeError(f'Dict key type for {key} not supported')
                    
                    if value_def == NutObjectType.STRING:
                        recoverd_value = str(value)
                    elif value_def == NutObjectType.INTEGER:
                        recoverd_value = int(value)
                    elif value_def == NutObjectType.FLOATINGPOINT:
                        recoverd_value = float(value)
                    elif value_def == NutObjectType.LIST:
                        recoverd_value = list(value)
                    else:
                        raise TypeError(f'Dict value type for {value} not supported')
                    
                    temp_dict[recoverd_key] = recoverd_value
                
                new_value = temp_dict
            
            if isinstance(new_data, ListOfThings) == True:
                # raw_list:List[Any,Any] = new_data.value
                # golden_item = raw_list[0]
                item_type:NutObjectType = new_data.value_def
                item_list:List[str] = new_data.value
                
                temp_list = []
                for item in item_list:
                    recoverd_value = None
                    if item_type == NutObjectType.STRING:
                        recoverd_value = str(item)
                    elif item_type == NutObjectType.INTEGER:
                        recoverd_value = int(item)
                    elif item_type == NutObjectType.FLOATINGPOINT:
                        recoverd_value = float(item)
                    else:
                        raise TypeError(f'List value type for {value} not supported')
                    temp_list.append(recoverd_value)
                
                new_value = temp_list
            # if isinstance(new_data, Empty) == True:
            #         new_value = None
        return new_value

class NutAdvancedFilterRules():
    """
    Class to hold all the rules for types
    """

    def __init__(self) -> None:
        pass

    def process_dict(self, dict_container:Dict):
        pass

class NutAdressing():
    """
    Class to handle the addressing and routing
    of the attributes and the data
    """
    
    def __init__(self) -> None:
        pass
    
    def get_attr_address(self,name:str, parent_attr:Any):
        """
        get the attribute parent
        """
        order:int = 1
        jump_list:List[tuple] = []
        
        #jump_list.append((order,name)) 
        jump_list.append(name)
        
        while hasattr(parent_attr, 'parent') == True:
            order += 1
            if getattr(parent_attr, 'atr_class') != AtrClass.NUT:
                parent_name = parent_attr.attribute
                #jump_list.append((order, parent_name))
                jump_list.append(parent_name)                 
            parent_attr = getattr(parent_attr, 'parent')
        
        if getattr(parent_attr, 'atr_class') == AtrClass.NUT:
            order += 1
            parent_name = parent_attr.var_name
            #jump_list.append((order, parent_name))
            jump_list.append(parent_name)  
        else:
            raise Exception("Error while getting address")
  
        return jump_list
        
            
        