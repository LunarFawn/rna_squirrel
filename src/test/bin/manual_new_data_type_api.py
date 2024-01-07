from enum import Enum
from attrs import define, field
from collections import namedtuple
from typing import List, Dict, Any,TypeVar, Type
from pathlib import Path

from data_squirrel.config.new_data_type_nut import (
	Nut,
	Value,
	GenericAttribute,
	AtrClass,
	CustomAttribute
)

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

class RNAStruct(Nut):

	def __init__(self, working_folder:str, var_name:str, use_db:bool = False) -> None:
		super().__init__(use_db=use_db,
			var_name=var_name,
			working_folder=Path(working_folder))




		self.primary_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="strand_db",
			atr_type=str))

		self._primary_structure: PrimaryStructure = PrimaryStructure(save_value=True,
			current=None,
			parent=self.primary_structure_db)




		self._ensemble: Ensemble = Ensemble(save_value=True,
			current=None,
			parent=self.ensemble_db)

	@property
	def primary_structure(self)->PrimaryStructure:
		return self._primary_structure

	@primary_structure.setter
	def primary_structure(self, struct:PrimaryStructure):
		if isinstance(struct, PrimaryStructure) == False:
			raise ValueError("Invalid value assignment")
		self._primary_structure = struct


	# @property
	# def ensemble(self)->Ensemble:
	# 	return self._ensemble

	# @ensemble.setter
	# def ensemble(self, struct:Ensemble):
	# 	if isinstance(struct, Ensemble) == False:
	# 		raise ValueError("Invalid value assignment")
	# 	self._ensemble = struct


