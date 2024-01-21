"""
This is the file for yaml operations when reading config files
"""

from ruamel.yaml import YAML
import copy
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type, Dict
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq

from data_squirrel.config.nut_yaml_objects import (
    NutDeclaration,
    NutObject,
    NutContainer,
    NutDatabaseInfo,
    NutStructure,
    NutObjectType,
    NutContainerDefinitions,
    ExternalAttribute
)

@dataclass
class WalkObjectReturn():
    structure_found_list:List[str]
    struct_priority_queue: List[tuple]
    level:int

class YAMLOperations():
    
    def __init__(self) -> None:
        self._yaml:YAML = YAML()
        self._yaml.register_class(NutDeclaration)
        self._yaml.register_class(NutObject)
        self._yaml.register_class(NutContainer)
        self._yaml.register_class(NutDatabaseInfo)
        self._yaml.register_class(NutStructure)
        self._yaml.register_class(NutObjectType)
        self._yaml.register_class(NutContainerDefinitions)
        self._yaml.register_class(ExternalAttribute)
        self._yaml_data:Any = None
        self._struct_dict:Dict[str, NutContainer] = {}
        
        #use heapq to turn list into a priority queue list
        self._priority_queue:List[tuple] = []
        self._backup_priority_queue:List[tuple] = []
        heapq.heapify(self._priority_queue)
        heapq.heapify(self._backup_priority_queue)
        
        #list of classes that is the master list of 
        #custom classes. If it is not here then the 
        #builder will fail if class not found here
    
    @property 
    def yaml(self)->YAML: 
        return self._yaml

    @property
    def nut(self)->NutStructure:
        return self._yaml_data['NUT']
    
    @property
    def definitions(self)->NutContainerDefinitions:
        return self._yaml_data['DEFINITIONS']

    @property
    def containers_dict(self)->Dict[str, NutContainer]:
        return self._struct_dict
    
    @property
    def yaml_data(self)->Any:
        return self._yaml_data
    
    @property
    def priority_queue(self):
        return self._priority_queue
    
    @priority_queue.setter
    def priority_queue(self, queue:List[tuple]):
        self._priority_queue = queue
        heapq.heapify(self._priority_queue)
    
    @property
    def pop_priority_queue(self):
        return heapq.heappop(self._priority_queue)
    
    @property
    def get_original_priorty_queue_copy(self):
        new_copy = copy.deepcopy(self._backup_priority_queue)
        heapq.heapify(new_copy)
        return new_copy
    
    @property
    def reset_priority_queue(self):
        self.priority_queue = self.get_original_priorty_queue_copy
    
    def open_yml_config(self, file_path:Path):
        """
        Open config yml file used to build the dynamic
        classes
        """
        
        data:Any = None
        
        try:
            with open(file_path, 'r') as file:
                data = self.yaml.load(file)
        except FileExistsError as error:
            raise error
        self._yaml_data = data
        self.build_struct_dict()
        self.build_struct_queue()
        return data
    
    def walk_objects_list(self, object_structs:List[str], level:int,struct_priority_queue: List[tuple] = [], previous_stucts:List[str]=[]):
        """
        Assumed that object_structs is non-empty
        """        
        structure_found_list:List[str] = []
        
        heapq.heapify(struct_priority_queue)
        
        for item in object_structs:
            current_item:NutContainer = self.definitions.definition_dict[item]
            next_object_structs:List[NutObject] = current_item.object_list
            # next_object_structs:List[Any] = self.walk_objects(yaml_data=yaml_data,
            #                                     object_struct=item)            
            for next_item in next_object_structs:
                if next_item.object_type == NutObjectType.CONTAINER:
                    if next_item.object_info not in structure_found_list and next_item.object_info not in previous_stucts:
                        structure_found_list.append(next_item.object_info)                        
                        value = (level*-1, next_item.object_info)
                        heapq.heappush(struct_priority_queue, value)
                        #struct_priority_queue.append(value)
                        #struct_order_queue.put(value)
                    
        walk_object:WalkObjectReturn = WalkObjectReturn(structure_found_list=structure_found_list,
                                                        struct_priority_queue=struct_priority_queue,
                                                        level=level)    
        return walk_object  
    
    def build_struct_dict(self)->Dict[str, NutContainer]:
        """
        Builds out the dictionary that has all the structures
        and their info
        """
        #now that we have list lets populate the global stuff
        #we care about
        struct_dict:Dict[str, NutContainer] = {}
        
        #first do the nut
        struct_dict['NUT'] = self.nut.nut_main_struct
        
        for container in self.definitions.nut_containers_definitions:
            if container.name in self.nut.nut_containers:
                struct_dict[container.name] = container
        
        self._struct_dict = struct_dict
        #return struct_dict
    
    def build_struct_queue(self):
        """
        Build the queue for all the classes
        so that they get built in the API in the 
        right order
        
        Walk the classes in the yaml and then end up with a
        prioritizedqueue of all the classes to make in the api
        """
        
        #need to replace with heapq
        struct_priority_queue: List[tuple] = []
        heapq.heapify(struct_priority_queue)
        
        #start with nut and then go from there only adding structures
        level_tracker:int = 1
        
        nut_list:List[str] = []
        
        nut_ojects = self.nut.nut_main_struct.object_list
        for item in nut_ojects:
            if item.object_type == NutObjectType.CONTAINER:
                queue_item = (level_tracker*-1, item.object_info)
                heapq.heappush(struct_priority_queue, queue_item)
                nut_list.append(item.object_info)
        level_tracker += 1
        hold_tracker:int = level_tracker
        
        
        
        stop = False
        
        walk_object:WalkObjectReturn = self.walk_objects_list(object_structs=nut_list,
                                                              level=level_tracker,
                                                              struct_priority_queue=struct_priority_queue)
        nut_list = nut_list + walk_object.structure_found_list
        
        while walk_object.structure_found_list != []:
            #start over the tracker at the same level
            #each time through
            level_tracker += 1
            walk_object = self.walk_objects_list(object_structs=walk_object.structure_found_list,
                                                level=level_tracker,
                                                previous_stucts=nut_list,
                                                struct_priority_queue=walk_object.struct_priority_queue)
            nut_list = nut_list + walk_object.structure_found_list
        
        heapq.heapify(walk_object.struct_priority_queue)
        
        self._priority_queue =  copy.deepcopy(walk_object.struct_priority_queue)
        self._backup_priority_queue = copy.deepcopy(walk_object.struct_priority_queue)
        
        #now the struct_order_queue should be built and be a priority queue
        #now build all the API classes in order of pop