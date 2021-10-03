
from ObjectRelationalMapper.Helpers.GameFromORMFactory import GameFromORMFactory
from ObjectRelationalMapper.Helpers.PostgresSelectedValues import PostgresSelectedValues
from ObjectRelationalMapper.StatementCreation.StatementCreationFacadePostgres import StatementCreationFacadePostgres
from ObjectRelationalMapper.ORMMappedObjects.ORMScreenshotURLs import ORMScreenshotURLS
from ObjectRelationalMapper.ORMMappedObjects.ORMGenres import ORMGenres
from ObjectRelationalMapper.ORMMappedObjects.ORMDevelopers import ORMDevelopers
from ObjectRelationalMapper.ORMMappedObjects.ORMPublishers import ORMPublishers
from ObjectRelationalMapper.ORMMappedObjects.ORMAppDetail import ORMAppDetail
from ObjectRelationalMapper.ORMMappedObjects.ORMUserDefinedGenres import ORMUserDefinedGenres
from ObjectRelationalMapper.ORMMappedObjects.ORMGame import ORMGame
from typing import Any, Callable, List
from GameModel import Game

class ORMMapper:
	def __init__(self, statement_creation_facade: StatementCreationFacadePostgres, game_from_orm_factory: GameFromORMFactory):
		self.statement_creation = statement_creation_facade
		self.game_from_orm_factory = game_from_orm_factory
		self.ORMClasses = [
			ORMGame,
			ORMUserDefinedGenres,
			ORMAppDetail,
			ORMPublishers,
			ORMDevelopers,
			ORMGenres,
			ORMScreenshotURLS
		]

	def create_tables(self, database_interaction_func: Callable[[str], Any]):
		for ORMClass in self.ORMClasses:
			table_create_statement = self.statement_creation.get_create_table_statement(ORMClass)
			database_interaction_func(table_create_statement)
	
	def insert_game(self, database_interaction_func: Callable[[str, tuple], Any], database_interaction_func_multiple_statements: Callable[[str, tuple], Any], game: Game):
		for ORMClass in self.ORMClasses:
			sql = self.statement_creation.get_insert_data_statement(ORMClass)
			insertion_data = ORMClass.get_insertion_data(game)
			non_commit_insertion_func = database_interaction_func
			if ORMClass.needs_multiple_statements():
				non_commit_insertion_func = database_interaction_func_multiple_statements
			non_commit_insertion_func(sql, insertion_data)

	def get_all_games(self, database_interaction_func: Callable[[str, tuple], Any]) -> List[Game]:
		storage = PostgresSelectedValues() # XXX factory could be passed in through DI
		for ORMClass in self.ORMClasses:
			sql = self.statement_creation.get_select_statement(ORMClass)
			selected_data_from_db = database_interaction_func(sql)
			mapped_data = [ORMClass(*row) for row in selected_data_from_db]
			storage.gather_and_store(ORMClass, mapped_data)
		
		if not storage.games_were_returned():
			return []

		return self.game_from_orm_factory.create_games(storage)
