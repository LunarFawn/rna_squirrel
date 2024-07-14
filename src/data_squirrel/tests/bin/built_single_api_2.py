"""
File that defines the main RNA sequence data
"""


from enum import Enum
from attrs import define, field
from collections import namedtuple
from typing import List, Dict, Any,TypeVar, Type
from pathlib import Path

from data_squirrel.config.dynamic_data_nut import (
	Nut,
	Value,
	GenericAttribute,
	AtrClass,
	CustomAttribute
)


from serena.utilities.ensemble_structures import Sara2SecondaryStructure
from serena.interfaces.Sara2_API_Python3 import DesignPerformanceData
from serena.interfaces.Sara2_API_Python3 import DesignInformation
from serena.interfaces.Sara2_API_Python3 import WetlabData

class Nut_Attributes(Enum):
	PrimaryStructure = "primary_structure_db"
	Ensemble = "ensemble_db"
	Sara2secStructLists = "primary_structure_lists_db"
	SecondStuff = "secondary_structure_stuff_db"


class RNAStrand(Nut):

	def __init__(self, working_folder:Path, var_name:str, use_db:bool = False) -> None:
		super().__init__(enum_list=Nut_Attributes,
			use_db=True,
			db=None,
			var_name=var_name,
			working_folder=working_folder)


		self.primary_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="strand_db",
			atr_type=str))

		self.primary_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="jumping_db",
			atr_type=str))

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="min_energy_db",
			atr_type=None))

		self.ensemble_db.min_energy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="kcal_db",
			atr_type=float))

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="max_energy_db",
			atr_type=None))

		self.ensemble_db.max_energy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="kcal_db",
			atr_type=float))

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="energy_groups_db",
			atr_type=['float', 'list']))

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="mfe_structure_db",
			atr_type=None))

		self.ensemble_db.mfe_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="dot_parens_db",
			atr_type=str))

		self.ensemble_db.mfe_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="free_energy_db",
			atr_type=None))

		self.ensemble_db.mfe_structure_db.free_energy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="kcal_db",
			atr_type=float))

		self.ensemble_db.mfe_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="stack_energy_db",
			atr_type=None))

		self.ensemble_db.mfe_structure_db.stack_energy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="kcal_db",
			atr_type=float))

		self.ensemble_db.mfe_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="structure_list_db",
			atr_type=int))

		self.ensemble_db.mfe_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="structure_dict_db",
			atr_type=dict))

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="mea_structure_db",
			atr_type=None))

		self.ensemble_db.mea_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="dot_parens_db",
			atr_type=str))

		self.ensemble_db.mea_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="free_energy_db",
			atr_type=None))

		self.ensemble_db.mea_structure_db.free_energy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="kcal_db",
			atr_type=float))

		self.ensemble_db.mea_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="stack_energy_db",
			atr_type=None))

		self.ensemble_db.mea_structure_db.stack_energy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="kcal_db",
			atr_type=float))

		self.ensemble_db.mea_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="structure_list_db",
			atr_type=int))

		self.ensemble_db.mea_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="structure_dict_db",
			atr_type=dict))

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="what_structure_db",
			atr_type=None))

		self.ensemble_db.what_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="strand_db",
			atr_type=str))

		self.ensemble_db.what_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="jumping_db",
			atr_type=str))

		self.primary_structure_lists_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="sara2_struct_list_db",
			atr_type=['Sara2SecondaryStructure', 'DesignPerformanceData', 'CLASS']))

		self.secondary_structure_stuff_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="secondary_structure_db",
			atr_type=['Sara2SecondaryStructure']))

		self.secondary_structure_stuff_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="performance_info_db",
			atr_type=['DesignPerformanceData', 'DesignInformation', 'WetlabData']))

class Energy(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def kcal(self)->float:
		return self.parent.kcal_db

	@kcal.setter
	def kcal(self, value:float):
		if isinstance(value, float) == False:
			raise ValueError("Invalid value assignment")
		self.parent.kcal_db = value


class PrimaryStructure(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def strand(self)->str:
		return self.parent.strand_db

	@strand.setter
	def strand(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.strand_db = value


	@property
	def jumping(self)->str:
		return self.parent.jumping_db

	@jumping.setter
	def jumping(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.jumping_db = value


class SecondaryStructure(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value
		self._free_energy: Energy = Energy(save_value=True,
			current=None,
			parent=self.parent.free_energy_db)

		self._stack_energy: Energy = Energy(save_value=True,
			current=None,
			parent=self.parent.stack_energy_db)


	@property
	def dot_parens(self)->str:
		return self.parent.dot_parens_db

	@dot_parens.setter
	def dot_parens(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.dot_parens_db = value


	@property
	def free_energy(self)->Energy:
		return self._free_energy

	@free_energy.setter
	def free_energy(self, value:Energy):
		if isinstance(value, Energy) == False:
			raise ValueError("Invalid value assignment")
		self._free_energy = value


	@property
	def stack_energy(self)->Energy:
		return self._stack_energy

	@stack_energy.setter
	def stack_energy(self, value:Energy):
		if isinstance(value, Energy) == False:
			raise ValueError("Invalid value assignment")
		self._stack_energy = value


	@property
	def structure_list(self)->List[int]:
		return self.parent.structure_list_db

	@structure_list.setter
	def structure_list(self, value:List[int]):
		if isinstance(value, list) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty lists not allowed")

		for item in value:
			if isinstance(item, int) == False:
				raise ValueError("Invalid value assignment")
		self.parent.structure_list_db = value


	@property
	def structure_dict(self)->dict:
		return self.parent.structure_dict_db

	@structure_dict.setter
	def structure_dict(self, value:dict):
		if isinstance(value, dict) == False:
			raise ValueError("Invalid value assignment")
		self.parent.structure_dict_db = value


class Ensemble(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value
		self._min_energy: Energy = Energy(save_value=True,
			current=None,
			parent=self.parent.min_energy_db)

		self._max_energy: Energy = Energy(save_value=True,
			current=None,
			parent=self.parent.max_energy_db)

		self._mfe_structure: SecondaryStructure = SecondaryStructure(save_value=True,
			current=None,
			parent=self.parent.mfe_structure_db)

		self._mea_structure: SecondaryStructure = SecondaryStructure(save_value=True,
			current=None,
			parent=self.parent.mea_structure_db)

		self._what_structure: PrimaryStructure = PrimaryStructure(save_value=True,
			current=None,
			parent=self.parent.what_structure_db)


	@property
	def min_energy(self)->Energy:
		return self._min_energy

	@min_energy.setter
	def min_energy(self, value:Energy):
		if isinstance(value, Energy) == False:
			raise ValueError("Invalid value assignment")
		self._min_energy = value


	@property
	def max_energy(self)->Energy:
		return self._max_energy

	@max_energy.setter
	def max_energy(self, value:Energy):
		if isinstance(value, Energy) == False:
			raise ValueError("Invalid value assignment")
		self._max_energy = value


	@property
	def energy_groups(self)->Dict[float,list]:
		return self.parent.energy_groups_db

	@energy_groups.setter
	def energy_groups(self, value:Dict[float,list]):
		if isinstance(value, dict) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty dicts not allowed")

		for key,val in value.items():
			if isinstance(key, float) == False:
				raise ValueError("Invalid key assignment to dic")
			if isinstance(val, list) == False:
				raise ValueError("Invalid value assignment to dict")
		self.parent.energy_groups_db = value


	@property
	def mfe_structure(self)->SecondaryStructure:
		return self._mfe_structure

	@mfe_structure.setter
	def mfe_structure(self, value:SecondaryStructure):
		if isinstance(value, SecondaryStructure) == False:
			raise ValueError("Invalid value assignment")
		self._mfe_structure = value


	@property
	def mea_structure(self)->SecondaryStructure:
		return self._mea_structure

	@mea_structure.setter
	def mea_structure(self, value:SecondaryStructure):
		if isinstance(value, SecondaryStructure) == False:
			raise ValueError("Invalid value assignment")
		self._mea_structure = value


	@property
	def what_structure(self)->PrimaryStructure:
		return self._what_structure

	@what_structure.setter
	def what_structure(self, value:PrimaryStructure):
		if isinstance(value, PrimaryStructure) == False:
			raise ValueError("Invalid value assignment")
		self._what_structure = value


class Sara2secStructLists(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def sara2_struct_list(self)->List[Sara2SecondaryStructure]:
		self.parent.nut_filter.yaml_operations.yaml.register_class(Sara2SecondaryStructure)
		self.parent.nut_filter.yaml_operations.yaml.register_class(DesignPerformanceData)
		return self.parent.sara2_struct_list_db

	@sara2_struct_list.setter
	def sara2_struct_list(self, value:List[Sara2SecondaryStructure]):
		if isinstance(value, list) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty lists not allowed")

		for item in value:
			if isinstance(item, Sara2SecondaryStructure) == False:
				raise ValueError("Invalid value assignment")
		self.parent.nut_filter.yaml_operations.yaml.register_class(Sara2SecondaryStructure)
		self.parent.nut_filter.yaml_operations.yaml.register_class(DesignPerformanceData)
		self.parent.sara2_struct_list_db = value


class SecondStuff(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def secondary_structure(self)->Sara2SecondaryStructure:
		self.parent.nut_filter.yaml_operations.yaml.register_class(Sara2SecondaryStructure)
		return self.parent.secondary_structure_db

	@secondary_structure.setter
	def secondary_structure(self, value:Sara2SecondaryStructure):
		if isinstance(value, Sara2SecondaryStructure) == False:
			raise ValueError("Invalid value assignment")
		self.parent.nut_filter.yaml_operations.yaml.register_class(Sara2SecondaryStructure)
		self.parent.secondary_structure_db = value


	@property
	def performance_info(self)->DesignPerformanceData:
		self.parent.nut_filter.yaml_operations.yaml.register_class(DesignPerformanceData)
		self.parent.nut_filter.yaml_operations.yaml.register_class(DesignInformation)
		self.parent.nut_filter.yaml_operations.yaml.register_class(WetlabData)
		return self.parent.performance_info_db

	@performance_info.setter
	def performance_info(self, value:DesignPerformanceData):
		if isinstance(value, DesignPerformanceData) == False:
			raise ValueError("Invalid value assignment")
		self.parent.nut_filter.yaml_operations.yaml.register_class(DesignPerformanceData)
		self.parent.nut_filter.yaml_operations.yaml.register_class(DesignInformation)
		self.parent.nut_filter.yaml_operations.yaml.register_class(WetlabData)
		self.parent.performance_info_db = value


class RNAStruct(RNAStrand):

	def __init__(self, working_folder:str, var_name:str, use_db:bool = False) -> None:
		super().__init__(use_db=use_db,
			var_name=var_name,
			working_folder=Path(working_folder))


		self._primary_structure: PrimaryStructure = PrimaryStructure(save_value=True,
			current=None,
			parent=self.primary_structure_db)

		self._ensemble: Ensemble = Ensemble(save_value=True,
			current=None,
			parent=self.ensemble_db)

		self._primary_structure_lists: Sara2secStructLists = Sara2secStructLists(save_value=True,
			current=None,
			parent=self.primary_structure_lists_db)

		self._secondary_structure_stuff: SecondStuff = SecondStuff(save_value=True,
			current=None,
			parent=self.secondary_structure_stuff_db)

	@property
	def primary_structure(self)->PrimaryStructure:
		return self._primary_structure

	@primary_structure.setter
	def primary_structure(self, struct:PrimaryStructure):
		if isinstance(struct, PrimaryStructure) == False:
			raise ValueError("Invalid value assignment")
		self._primary_structure = struct


	@property
	def ensemble(self)->Ensemble:
		return self._ensemble

	@ensemble.setter
	def ensemble(self, struct:Ensemble):
		if isinstance(struct, Ensemble) == False:
			raise ValueError("Invalid value assignment")
		self._ensemble = struct


	@property
	def primary_structure_lists(self)->Sara2secStructLists:
		return self._primary_structure_lists

	@primary_structure_lists.setter
	def primary_structure_lists(self, struct:Sara2secStructLists):
		if isinstance(struct, Sara2secStructLists) == False:
			raise ValueError("Invalid value assignment")
		self._primary_structure_lists = struct


	@property
	def secondary_structure_stuff(self)->SecondStuff:
		return self._secondary_structure_stuff

	@secondary_structure_stuff.setter
	def secondary_structure_stuff(self, struct:SecondStuff):
		if isinstance(struct, SecondStuff) == False:
			raise ValueError("Invalid value assignment")
		self._secondary_structure_stuff = struct


