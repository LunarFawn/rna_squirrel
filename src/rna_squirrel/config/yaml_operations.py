"""
This is the file for yaml operations when reading config files
"""

from ruamel.yaml import YAML
import sys
from pathlib import Path
from typing import Any, List, ClassVar, Type, Dict
#from attrs import define, field
from enum import Enum
from dataclasses import dataclass, field
from queue import PriorityQueue
import heapq


from rna_squirrel.config.dynamic_rna_strand import AtrClass

class ObjectStatus(Enum):
    """
    The enum for type of object
    """
    CLASS = 'CLASS'
    VALUE = 'VALUE'

@dataclass
class CLASS:
    status:ObjectStatus = ObjectStatus.CLASS

@dataclass
class VALUE:
    status:ObjectStatus = ObjectStatus.VALUE

@dataclass
class Integer:
    name:str
    python_type:Any = field(init=False)
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)
    
    def __post_init__(self) -> None:
        self.python_type = 'int'
        self.status = ObjectStatus.VALUE
        self.db_name = f'{self.name}_db'
        
@dataclass
class FloatingPoint:
    name:str
    python_type:Any = field(init=False)
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)
    
    def __post_init__(self) -> None:
        self.python_type = 'float'
        self.status = ObjectStatus.VALUE
        self.db_name = f'{self.name}_db'
        
@dataclass
class String:
    name:str
    python_type:Any = field(init=False)
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)
    
    def __post_init__(self) -> None:
        self.python_type = 'str'
        self.status = ObjectStatus.VALUE
        self.db_name = f'{self.name}_db'

        
@dataclass
class Dictionary:
    name:str
    key: Any
    value: Any
    python_type:Any = field(init=False)
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)

    def __post_init__(self) -> None:
        self.python_type = "Dict"
        self.status = ObjectStatus.VALUE
        self.db_name = f'{self.name}_db'
        
@dataclass
class ClassType:
    name:str
    class_type:str
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)
    
    def __post_init__(self) -> None:
        self.status = ObjectStatus.CLASS
        self.db_name = f'{self.name}_db'

@dataclass
class ValueType:
    name:str
    python_type:str 
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)
    
    def __post_init__(self) -> None:
        self.status = ObjectStatus.VALUE
        self.db_name = f'{self.name}_db'
    
@dataclass
class CustomList:
    name: str
    list_type: str
    status:ObjectStatus = field(init=False)
    db_name:str = field(init=False)
    
    def __post_init__(self) -> None:
        self.status = ObjectStatus.CLASS
        self.db_name = f'{self.name}_db'
    
@dataclass
class ClassDeclaration:
    name:str

class NutObjectType(Enum):
    INT="INT"
    FLOAT="FLOAT"
    STRING="STRING"
    BOOL="BOOL"

    @classmethod
    def from_yaml(cls, loader, node):
        test = cls(node.value)
        return test

@dataclass
class Objects():
    """
    class for the fields to define
    the attributes of an object.
    Classes and attributes both have specs
    """
    #yaml_tage: ClassVar = '!Spec'
    
    #status:str #ObjectStatus
    #status_enum:ObjectStatus = field(init=False)   
    name: str
    object_list: Any 
    db_name:str = field(init=False)
      
    def __post_init__(self) -> None:
        self.db_name = f'{self.name}_db'

@dataclass
class NUT():
    name:str
    objects: Objects

@dataclass
class ValueSpec:
    """
    Class for getting the configuration
    of the attributes that are values 
    so that the code can build the type
    """
    type_name: str
    
@dataclass
class WalkObjectReturn():
    structure_found_list:List[str]
    struct_order_queue:PriorityQueue
    level:int

@dataclass
class ParentSpecs():
    pass

class YAMLOperations():
    
    def __init__(self) -> None:
        self.yaml = YAML()
        self.yaml.register_class(Objects)
        self.yaml.register_class(String)
        self.yaml.register_class(ClassType)
        self.yaml.register_class(ClassDeclaration)
        self.yaml.register_class(NUT)
        self.yaml.register_class(NutObjectType)
        self.yml_data: Any = None
        
        #list of classes that is the master list of 
        #custom classes. If it is not here then the 
        #builder will fail if class not found here
        self.classes_list: List[str] = []
        
        self.nut_attributes: List[Objects] = []
        

    def run_python_build(self, yaml_filepath:Path):
        """
        Entry point ot build python api's and
        backend config files
        """
        
        #first need to open the yaml file and grab the
        #data
        data = self.open_yml_config(file_path=yaml_filepath)
        
        #now parse the declarations so we know what classes we 
        #have to work with
        declared_classes = self.get_declarations(yaml_data=data)
        
        #now that we have list lets populate the global stuff
        #we care about
        # for declaration in declared_classes:
        #     self.classes_list.append(declaration.name)
            
        #now get NUT objects and build out from there
        struct_dict:Dict[str, Objects] = self.build_struct_dict(yaml_data=data,
                                                               declarations=declared_classes)
        queue:PriorityQueue = self.build_struct_queue(yaml_data=data,
                                                    struct_dict=struct_dict)
        

    def build_struct_dict(self, yaml_data:Any, declarations:List[ClassDeclaration])->Dict[str, Objects]:
        """
        Builds out the dictionary that has all the structures
        and their info
        """
        #now that we have list lets populate the global stuff
        #we care about
        struct_dict:Dict[str, Objects] = {}
        
        #first do the nut
        struct_dict['NUT'] = yaml_data["NUT"].objects
        for declaration in declarations:
            struct_name:str = declaration.name
            struct_dict[struct_name] = yaml_data[struct_name]
            #self.classes_list.append(declaration.name)
        return struct_dict
        
    def build_struct_queue(self, yaml_data:Any, struct_dict:Dict[str, Objects]):
        """
        Build the queue for all the classes
        so that they get built in the API in the 
        right order
        
        Walk the classes in the yaml and then end up with a
        prioritizedqueue of all the classes to make in the api
        """
        
        #need to replace with heapq
        struct_order_queue:PriorityQueue = PriorityQueue()
        
        #start with nut and then go from there only adding structures
        level_tracker:int = 1
        
        nut_list:List[str] = []
        
        nut_ojects = struct_dict['NUT'].object_list
        for nut_object in nut_ojects:
            if nut_object.status == ObjectStatus.CLASS:
                queue_item = (level_tracker*-1, nut_object.class_type)
                struct_order_queue.put(queue_item) 
                nut_list.append(nut_object.class_type)
        level_tracker += 1
        hold_tracker:int = level_tracker
        
        
        
        stop = False
        
        walk_object:WalkObjectReturn = self.walk_objects_list(yaml_data=yaml_data,
                                                              object_structs=nut_list,
                                                              struct_order_queue=struct_order_queue,
                                                              level=level_tracker)
        nut_list = nut_list + walk_object.structure_found_list
        
        while walk_object.structure_found_list != []:
            #start over the tracker at the same level
            #each time through
            level_tracker += 1
            walk_object = self.walk_objects_list(yaml_data=yaml_data,
                                                object_structs=walk_object.structure_found_list,
                                                struct_order_queue=struct_order_queue,
                                                level=level_tracker,
                                                previous_stucts=nut_list)
            nut_list = nut_list + walk_object.structure_found_list
        
        #now the struct_order_queue should be built and be a priority queue
        #now build all the API classes in order of pop
        return struct_order_queue  
    
    def walk_objects_list(self, yaml_data:Any, object_structs:List[str],struct_order_queue:PriorityQueue, level:int, previous_stucts:List[str]=[]):
        """
        Assumed that object_structs is non-empty
        """
        
        structure_found_list:List[str] = []
        
        for item in object_structs:
            current_item = yaml_data[item]
            next_object_structs:List[Any] = yaml_data[item].object_list
            # next_object_structs:List[Any] = self.walk_objects(yaml_data=yaml_data,
            #                                     object_struct=item)            
            for next_item in next_object_structs:
                if isinstance(next_item, ClassType) is True:
                    if next_item.class_type not in structure_found_list and next_item.class_type not in previous_stucts:
                        structure_found_list.append(next_item.class_type)
                        value = (level*-1, next_item.class_type)
                        struct_order_queue.put(value)
                    
        walk_object:WalkObjectReturn = WalkObjectReturn(structure_found_list=structure_found_list,
                                                        struct_order_queue=struct_order_queue,
                                                        level=level)    
        return walk_object   
    
    # def walk_objects(self,yaml_data:Any, object_struct:str):
    #     is_class:bool = False
        
    #     current_struct:Any = yaml_data[object_struct]
    #     object_list:List[Any] = current_struct.object_list
        
    #     return object_list
        
    
    def build_class(self, yaml_data:Any):
        """
        build class entry to append to the API as well
        """
        pass
        
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

        return data
     
    
    def get_declarations(self, yaml_data:Any)->List[ClassDeclaration]:
        """
        strep through and parse the declarations
        to build out the list of classes
        and what the interpreter is to expect as
        it is pretty dumb right now
        """
        
        declared_classes:List[ClassDeclaration] = []
        
        #generate list of classes first from yaml
        list_of_declarations: List[Any] = yaml_data["DECLARATIONS"]
        for declaration in list_of_declarations:
            declared_classes.append(declaration)
        

        
        return declared_classes
        
    def parse_system_settings(self, data:Any):
        """
        Parse the raw data from the yml file
        to populate the main system catagories
        required for generation and population
        of python files
        """
        
        #first get the list of classes
        classes = data['OBJECT_CLASSES']
        
    def get_object_list(self, yaml_data:Any, class_name:str):
        class_objects:List[ClassType] = []
        value_objects: List[Any] = []
        object_count:int = int(yaml_data[class_name]["object_count"]["count"])
        raw_object_list = yaml_data[class_name]["objects"]
        for object in raw_object_list:
            if isinstance(object, ClassType) is True:
                class_objects.append(object)
            else:
                value_objects.append(object)
        return class_objects, value_objects
    
    def read_object_attributes(self):
        pass
