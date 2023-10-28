"""
File that defines the main RNA sequence data
"""


from enum import Enum
from attrs import define, field
from collections import namedtuple
from typing import List, Dict, Any,TypeVar, Type

from rna_squirrel.config.dynamic_rna_strand import (
	Nut,
	Value,
	GenericAttribute,
	AtrClass,
	CustomAttribute
)


class Nut_Attributes(Enum):
	PrimaryStructure = "primary_structure_db"
	Ensemble = "ensemble_db"


class NupackStrand(Nut):

	def __init__(self,var_name:str, use_db:bool = False) -> None:
		super().__init__(enum_list=Nut_Attributes,
			use_db=True,
			db=None,
   			var_name=var_name)


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

		self.ensemble_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="what_structure_db",
			atr_type=None))

		self.ensemble_db.what_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="strand_db",
			atr_type=str))

		self.ensemble_db.what_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="jumping_db",
			atr_type=str))

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
		self.parent.strand_db = value


	@property
	def jumping(self)->str:
		return self.parent.jumping_db

	@jumping.setter
	def jumping(self, value:str):
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
		self.parent.dot_parens_db = value


	@property
	def free_energy(self)->Energy:
		return self.parent.free_energy_db

	@free_energy.setter
	def free_energy(self, value:Energy):
		self.parent.free_energy_db = value


	@property
	def stack_energy(self)->Energy:
		return self.parent.stack_energy_db

	@stack_energy.setter
	def stack_energy(self, value:Energy):
		self.parent.stack_energy_db = value


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
		return self.parent.min_energy_db

	@min_energy.setter
	def min_energy(self, value:Energy):
		self.parent.min_energy_db = value


	@property
	def max_energy(self)->Energy:
		return self.parent.max_energy_db

	@max_energy.setter
	def max_energy(self, value:Energy):
		self.parent.max_energy_db = value


	@property
	def mfe_structure(self)->SecondaryStructure:
		return self.parent.mfe_structure_db

	@mfe_structure.setter
	def mfe_structure(self, value:SecondaryStructure):
		self.parent.mfe_structure_db = value


	@property
	def mea_structure(self)->SecondaryStructure:
		return self.parent.mea_structure_db

	@mea_structure.setter
	def mea_structure(self, value:SecondaryStructure):
		self.parent.mea_structure_db = value


	@property
	def what_structure(self)->PrimaryStructure:
		return self.parent.what_structure_db

	@what_structure.setter
	def what_structure(self, value:PrimaryStructure):
		self.parent.what_structure_db = value


class rna_strand(NupackStrand):

	def __init__(self,var_name:str, use_db:bool = False) -> None:
		super().__init__(use_db=use_db,
                   var_name=var_name)


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
		self._primary_structure = struct


	@property
	def ensemble(self)->Ensemble:
		return self._ensemble

	@ensemble.setter
	def ensemble(self, struct:Ensemble):
		self._ensemble = struct


