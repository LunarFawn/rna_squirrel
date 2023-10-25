"""
Config file built from yaml
"""


from enum import Enum
from typing import TypeVar, Type, List, Dict
from attrs import define, field
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

	def __init__(self, use_db:bool = False) -> None:
		super().__init__(enum_list=Nut_Attributes,
			use_db=True,
			db=None)


		self.primary_structure_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="strand_db",
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

