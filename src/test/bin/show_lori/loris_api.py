"""
File that defines the main RNA sequence data
"""


from enum import Enum
from attrs import define, field
from collections import namedtuple
from typing import List, Dict, Any,TypeVar, Type
from pathlib import Path

from rna_squirrel.config.dynamic_rna_strand import (
	Nut,
	Value,
	GenericAttribute,
	AtrClass,
	CustomAttribute
)


class Nut_Attributes(Enum):
	Science = "favorites_db"
	Hotness = "sexy_db"


class LoriStructure(Nut):

	def __init__(self, working_folder:Path, var_name:str, use_db:bool = False) -> None:
		super().__init__(enum_list=Nut_Attributes,
			use_db=True,
			db=None,
			var_name=var_name,
			working_folder=working_folder)


		self.favorites_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="favorite_show_db",
			atr_type=None))

		self.favorites_db.favorite_show_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="show_name_db",
			atr_type=str))

		self.favorites_db.favorite_show_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="era_db",
			atr_type=str))

		self.favorites_db.new_attr(GenericAttribute(atr_class=AtrClass.PARENT,
			attribute="education_db",
			atr_type=None))

		self.favorites_db.education_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="favorite_subject_db",
			atr_type=str))

		self.favorites_db.education_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="method_db",
			atr_type=str))

		self.sexy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="boobs_names_db",
			atr_type=str))

		self.sexy_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD,
			attribute="is_nice_tits_db",
			atr_type=bool))

class Learning(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def favorite_subject(self)->str:
		return self.parent.favorite_subject_db

	@favorite_subject.setter
	def favorite_subject(self, value:str):
		self.parent.favorite_subject_db = value


	@property
	def method(self)->str:
		return self.parent.method_db

	@method.setter
	def method(self, value:str):
		self.parent.method_db = value


class StarTrek(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def show_name(self)->str:
		return self.parent.show_name_db

	@show_name.setter
	def show_name(self, value:str):
		self.parent.show_name_db = value


	@property
	def era(self)->str:
		return self.parent.era_db

	@era.setter
	def era(self, value:str):
		self.parent.era_db = value


class Hotness(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def boobs_names(self)->str:
		return self.parent.boobs_names_db

	@boobs_names.setter
	def boobs_names(self, value:str):
		self.parent.boobs_names_db = value


	@property
	def is_nice_tits(self)->bool:
		return self.parent.is_nice_tits_db

	@is_nice_tits.setter
	def is_nice_tits(self, value:bool):
		self.parent.is_nice_tits_db = value


class Science(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value
		self._favorite_show: StarTrek = StarTrek(save_value=True,
			current=None,
			parent=self.parent.favorite_show_db)

		self._education: Learning = Learning(save_value=True,
			current=None,
			parent=self.parent.education_db)


	@property
	def favorite_show(self)->StarTrek:
		return self._favorite_show

	@favorite_show.setter
	def favorite_show(self, value:StarTrek):
		self._favorite_show = value


	@property
	def education(self)->Learning:
		return self._education

	@education.setter
	def education(self, value:Learning):
		self._education = value


class Lori(LoriStructure):

	def __init__(self, working_folder:str, var_name:str, use_db:bool = False) -> None:
		super().__init__(use_db=use_db,
			var_name=var_name,
			working_folder=Path(working_folder))


		self._favorites: Science = Science(save_value=True,
			current=None,
			parent=self.favorites_db)

		self._sexy: Hotness = Hotness(save_value=True,
			current=None,
			parent=self.sexy_db)

	@property
	def favorites(self)->Science:
		return self._favorites

	@favorites.setter
	def favorites(self, struct:Science):
		self._favorites = struct


	@property
	def sexy(self)->Hotness:
		return self._sexy

	@sexy.setter
	def sexy(self, struct:Hotness):
		self._sexy = struct


