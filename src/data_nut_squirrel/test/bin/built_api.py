"""
File that defines the main RNA sequence data
"""


from attrs import define, field
from collections import namedtuple
from typing import List, Dict, Any

from test.bin.built_config import (
	Spaceship,
)

from data_nut_squirrel.config.dynamic_data_nut import (
	Nut,
	Value,
	GenericAttribute,
	AtrClass,
	CustomAttribute
)


class Fines(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def sizes(self)->List[int]:
		return self.parent.sizes_db

	@sizes.setter
	def sizes(self, value:List[int]):
		if isinstance(value, list) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty lists not allowed")

		for item in value:
			if isinstance(item, int) == False:
				raise ValueError("Invalid value assignment")
		self.parent.sizes_db = value


	@property
	def shape(self)->str:
		return self.parent.shape_db

	@shape.setter
	def shape(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.shape_db = value


	@property
	def color(self)->str:
		return self.parent.color_db

	@color.setter
	def color(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.color_db = value


	@property
	def color_lists(self)->Dict[float,list]:
		return self.parent.color_lists_db

	@color_lists.setter
	def color_lists(self, value:Dict[float,list]):
		if isinstance(value, dict) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty dicts not allowed")

		for key,val in value.items():
			if isinstance(key, float) == False:
				raise ValueError("Invalid key assignment to dic")
			if isinstance(val, list) == False:
				raise ValueError("Invalid value assignment to dict")
		self.parent.color_lists_db = value


class Flames(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def size(self)->int:
		return self.parent.size_db

	@size.setter
	def size(self, value:int):
		if isinstance(value, int) == False:
			raise ValueError("Invalid value assignment")
		self.parent.size_db = value


	@property
	def luemens(self)->float:
		return self.parent.luemens_db

	@luemens.setter
	def luemens(self, value:float):
		if isinstance(value, float) == False:
			raise ValueError("Invalid value assignment")
		self.parent.luemens_db = value


class Hatch(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def shape(self)->str:
		return self.parent.shape_db

	@shape.setter
	def shape(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.shape_db = value


	@property
	def window_type(self)->str:
		return self.parent.window_type_db

	@window_type.setter
	def window_type(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.window_type_db = value


	@property
	def window_size_versions(self)->Dict[int,str]:
		return self.parent.window_size_versions_db

	@window_size_versions.setter
	def window_size_versions(self, value:Dict[int,str]):
		if isinstance(value, dict) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty dicts not allowed")

		for key,val in value.items():
			if isinstance(key, int) == False:
				raise ValueError("Invalid key assignment to dic")
			if isinstance(val, str) == False:
				raise ValueError("Invalid value assignment to dict")
		self.parent.window_size_versions_db = value


	@property
	def external_simple_list(self)->List[ExternalClassDemo]:
		self.parent.nut_filter.yaml_operations.yaml.register_class(ExternalClassDemo)
		return self.parent.external_simple_list_db

	@external_simple_list.setter
	def external_simple_list(self, value:List[ExternalClassDemo]):
		if isinstance(value, list) == False:
			raise ValueError("Invalid value assignment")
		if len(value) < 1:
			raise Exception("Empty lists not allowed")

		for item in value:
			if isinstance(item, ExternalClassDemo) == False:
				raise ValueError("Invalid value assignment")
		self.parent.nut_filter.yaml_operations.yaml.register_class(ExternalClassDemo)
		self.parent.external_simple_list_db = value


	@property
	def external_complex_value(self)->ComponentsDemo:
		self.parent.nut_filter.yaml_operations.yaml.register_class(ComponentsDemo)
		self.parent.nut_filter.yaml_operations.yaml.register_class(ExternalClassDemo)
		return self.parent.external_complex_value_db

	@external_complex_value.setter
	def external_complex_value(self, value:ComponentsDemo):
		if isinstance(value, ComponentsDemo) == False:
			raise ValueError("Invalid value assignment")
		self.parent.nut_filter.yaml_operations.yaml.register_class(ComponentsDemo)
		self.parent.nut_filter.yaml_operations.yaml.register_class(ExternalClassDemo)
		self.parent.external_complex_value_db = value


	@property
	def external_simple_value(self)->ExternalClassDemo:
		self.parent.nut_filter.yaml_operations.yaml.register_class(ExternalClassDemo)
		return self.parent.external_simple_value_db

	@external_simple_value.setter
	def external_simple_value(self, value:ExternalClassDemo):
		if isinstance(value, ExternalClassDemo) == False:
			raise ValueError("Invalid value assignment")
		self.parent.nut_filter.yaml_operations.yaml.register_class(ExternalClassDemo)
		self.parent.external_simple_value_db = value


class Engine(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value
		self._flames: Flames = Flames(save_value=True,
			current=None,
			parent=self.parent.flames_db)


	@property
	def flames(self)->Flames:
		return self._flames

	@flames.setter
	def flames(self, value:Flames):
		if isinstance(value, Flames) == False:
			raise ValueError("Invalid value assignment")
		self._flames = value


	@property
	def color(self)->str:
		return self.parent.color_db

	@color.setter
	def color(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.color_db = value


class MidSection(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value
		self._hatch: Hatch = Hatch(save_value=True,
			current=None,
			parent=self.parent.hatch_db)

		self._fines: Fines = Fines(save_value=True,
			current=None,
			parent=self.parent.fines_db)


	@property
	def hatch(self)->Hatch:
		return self._hatch

	@hatch.setter
	def hatch(self, value:Hatch):
		if isinstance(value, Hatch) == False:
			raise ValueError("Invalid value assignment")
		self._hatch = value


	@property
	def fines(self)->Fines:
		return self._fines

	@fines.setter
	def fines(self, value:Fines):
		if isinstance(value, Fines) == False:
			raise ValueError("Invalid value assignment")
		self._fines = value


	@property
	def color(self)->str:
		return self.parent.color_db

	@color.setter
	def color(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.color_db = value


class Top(CustomAttribute):
	def __init__(self, parent: Any, current:Any, save_value:bool) -> None:
		self.parent = parent
		self.current = current
		self.do_save = save_value

	@property
	def color(self)->str:
		return self.parent.color_db

	@color.setter
	def color(self, value:str):
		if isinstance(value, str) == False:
			raise ValueError("Invalid value assignment")
		self.parent.color_db = value


class Spaceship(SpaceshipHelix):

	def __init__(self, working_folder:str, var_name:str, use_db:bool = False) -> None:
		super().__init__(use_db=use_db,
			var_name=var_name,
			working_folder=Path(working_folder))


		self._top: Top = Top(save_value=True,
			current=None,
			parent=self.top_db)

		self._midsection: MidSection = MidSection(save_value=True,
			current=None,
			parent=self.midsection_db)

		self._engine: Engine = Engine(save_value=True,
			current=None,
			parent=self.engine_db)

	@property
	def top(self)->Top:
		return self._top

	@top.setter
	def top(self, struct:Top):
		if isinstance(struct, Top) == False:
			raise ValueError("Invalid value assignment")
		self._top = struct


	@property
	def midsection(self)->MidSection:
		return self._midsection

	@midsection.setter
	def midsection(self, struct:MidSection):
		if isinstance(struct, MidSection) == False:
			raise ValueError("Invalid value assignment")
		self._midsection = struct


	@property
	def engine(self)->Engine:
		return self._engine

	@engine.setter
	def engine(self, struct:Engine):
		if isinstance(struct, Engine) == False:
			raise ValueError("Invalid value assignment")
		self._engine = struct


