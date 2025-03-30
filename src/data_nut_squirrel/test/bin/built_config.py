"""
Config file built from yaml
"""


from enum import Enum
from typing import TypeVar, Type, List, Dict
from attrs import define, field
from pathlib import Path
from data_nut_squirrel.config.dynamic_data_nut import (
	Nut,
	Value,
	GenericAttribute,
	AtrClass,
	CustomAttribute
)

class Nut_Attributes(Enum):
	Top = "top_db"
	MidSection = "midsection_db"
	Engine = "engine_db"


class Spaceship(Nut):

	def __init__(self, working_folder:Path, var_name:str, use_db:bool = False) -> None:
		super().__init__(enum_list=Nut_Attributes,
			use_db=True,
			db=None,
			var_name=var_name,
			working_folder=working_folder)


		self.top_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="color_db",
			atr_type=str))

		self.midsection_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="hatch_db",
			atr_type=None))

		self.midsection_db.hatch_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="shape_db",
			atr_type=str))

		self.midsection_db.hatch_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="window_type_db",
			atr_type=str))

		self.midsection_db.hatch_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="window_size_versions_db",
			atr_type=['int', 'str']))

		self.midsection_db.hatch_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="external_simple_list_db",
			atr_type=['ExternalClassDemo', 'CLASS']))

		self.midsection_db.hatch_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="external_complex_value_db",
			atr_type=['ComponentsDemo', 'ExternalClassDemo']))

		self.midsection_db.hatch_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="external_simple_value_db",
			atr_type=['ExternalClassDemo']))

		self.midsection_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="fines_db",
			atr_type=None))

		self.midsection_db.fines_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="sizes_db",
			atr_type=int))

		self.midsection_db.fines_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="shape_db",
			atr_type=str))

		self.midsection_db.fines_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="color_db",
			atr_type=str))

		self.midsection_db.fines_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="color_lists_db",
			atr_type=['float', 'list']))

		self.midsection_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="color_db",
			atr_type=str))

		self.engine_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="flames_db",
			atr_type=None))

		self.engine_db.flames_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="size_db",
			atr_type=int))

		self.engine_db.flames_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="luemens_db",
			atr_type=float))

		self.engine_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="color_db",
			atr_type=str))

