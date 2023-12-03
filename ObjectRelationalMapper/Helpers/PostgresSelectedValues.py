
# self._returned_data is indexed by steam_id. it is of one of two formats, an array or a single object:
# {
#   12345: [
#       ORMScreenshotURL(12345, "link/to/lo-res", "link/to/hi-res"),
#       ORMScreenshotURL(12345, "link/to/this-lo-res", "link/to/this-hi-res")
#   ]
#   34567: [
#       ORMScreenshotURL(34567, "link/to/lo-res", "link/to/hi-res"),
#       ORMScreenshotURL(34567, "link/to/this-lo-res", "link/to/this-hi-res")
#   ]
# }

# {
#   12345: ORMGame(...)
#   34567: ORMGame(...)
# }
from typing import Dict, List, Type, Union, Optional, Any
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from ObjectRelationalMapper.ORMMappedObjects.ORMGame import ORMGame

class PostgresSelectedValues:
	def __init__(self):
		self._returned_data = {}

	def gather_and_store(self, ORMClass: Type[ORMAbstractBase], orm_instances: List[ORMAbstractBase]):
		class_name = self._get_class_name(ORMClass)
		self._returned_data[class_name] = self._group_values(ORMClass, orm_instances)

	def get_associated_data(self, ORMClass: Type[ORMAbstractBase], steam_id: int, default_value: Optional[Any] = None) -> Dict[int,Union[ORMAbstractBase, List[ORMAbstractBase]]]:
		try:
			return self._returned_data[self._get_class_name(ORMClass)][steam_id]
		except:
			return default_value

	# if no games were returned from query, then return true
	def games_were_returned(self) -> bool:
		game_class_name = self._get_class_name(ORMGame)
		return game_class_name in self._returned_data
	
	def get_steam_ids(self) -> List[int]:
		if not self.games_were_returned():
			return []
		game_class_name = self._get_class_name(ORMGame)
		return list(self._returned_data[game_class_name].keys())

	def _array_handler(self, orm_instances: List[ORMAbstractBase]) -> Dict[int, List[ORMAbstractBase]]:
		gathered_values = {}
		orm_instances_internal = orm_instances.copy()
		# try sort - it's okay if this fails as it means there was no rank field to deal with for sorting.
		# sort by rank so that you always encounter ranked items in correct order
		try:
			orm_instances_internal = sorted(orm_instances, key=lambda orm_instance: orm_instance.rank)
		except:
			pass

		for orm_instance in orm_instances_internal:
			steam_id = orm_instance.steam_id
			if steam_id not in gathered_values:
				gathered_values[steam_id] = []
			gathered_values[steam_id].append(orm_instance)
		return gathered_values

	def _unique_value_handler(self, orm_instances: List[ORMAbstractBase]) -> Dict[int, ORMAbstractBase]:
		gathered_values = {}
		for orm_instance in orm_instances:
			gathered_values[orm_instance.steam_id] = orm_instance
		return gathered_values

	def _group_values(self, ORMClass: Type[ORMAbstractBase], data_to_group: List[ORMAbstractBase]):
		if ORMClass.needs_multiple_statements():
			return self._array_handler(data_to_group)
		else:
			return self._unique_value_handler(data_to_group)

	def _get_class_name(self, Class: Type) -> str:
		return Class.__name__
