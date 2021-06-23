
from GameModel import Game
from typing import Any, Callable
from ObjectRelationalMapper.ORMMappedObjects.ORMScreenshotURLs import ORMScreenshotURLS
from ObjectRelationalMapper.ORMMappedObjects.ORMGenres import ORMGenres
from ObjectRelationalMapper.ORMMappedObjects.ORMDevelopers import ORMDevelopers
from ObjectRelationalMapper.ORMMappedObjects.ORMPublishers import ORMPublishers
from ObjectRelationalMapper.ORMMappedObjects.ORMAppDetail import ORMAppDetail
from ObjectRelationalMapper.ORMMappedObjects.ORMUserDefinedGenres import ORMUserDefinedGenres
from ObjectRelationalMapper.ORMMappedObjects.ORMGame import ORMGame
from ObjectRelationalMapper.StatementCreation.StatementCreationFacadePostgres import StatementCreationFacadePostgres


class ORMMapper:
    def __init__(self, statement_creation_facade: StatementCreationFacadePostgres):
        self.statement_creation = statement_creation_facade
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
            table_create_statement = self.statement_creation.create_table_statement(ORMClass)
            database_interaction_func(table_create_statement)
    
    def insert_game(self, database_interaction_func: Callable[[str, tuple], Any], database_interaction_func_multiple_statements: Callable[[str, tuple], Any], game: Game):
        for ORMClass in self.ORMClasses:

            sql = self.statement_creation.get_insert_data_statement(ORMClass)
            insertion_data = ORMClass.get_insertion_data(game)
            non_commit_insertion_func = database_interaction_func
            if ORMClass.needs_multiple_statements():
                non_commit_insertion_func = database_interaction_func_multiple_statements
            non_commit_insertion_func(sql, insertion_data)
