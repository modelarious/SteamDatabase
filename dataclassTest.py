from GameModel import Game
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Callable, Dict, List, Tuple, get_type_hints

class ORMAbstractBase(ABC):
    @staticmethod
    @abstractmethod
    def get_table_name() -> str:
        return ""

    @staticmethod
    @abstractmethod
    def get_insertion_data() -> tuple:
        return ()

    # return a tuple of names of columns that are part of primary key 
    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return ()
    
    # in the form of "column_name": "ForeignTable" which becomes 
    # FOREIGN KEY (column_name) REFERENCES ForeignTable(column_name)
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {}

    # names of columns that contain values that won't be unique
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return []
    
    # names of columns that may be null
    @staticmethod
    def get_nullable_fields() -> List[str]:
        return []

@dataclass
class ORMUserDefinedGenres(ORMAbstractBase):
    steam_id: int
    genre_name: str
    rank: int

    @staticmethod
    def get_table_name() -> str:
        return 'UserDefinedGenres'
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'steam_id',
            'genre_name',
            'rank'
        ]

@dataclass
class ORMPublishers(ORMAbstractBase):
    steam_id: int
    publisher: str

    @staticmethod
    def get_table_name() -> str:
        return 'Publishers'
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'steam_id',
            'publisher'
        ]

@dataclass
class ORMDevelopers(ORMAbstractBase):
    steam_id: int
    developer: str

    @staticmethod
    def get_table_name() -> str:
        return 'Developers'
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'steam_id',
            'developer'
        ]

@dataclass
class ORMGenres(ORMAbstractBase):
    steam_id: int
    genre: str

    @staticmethod
    def get_table_name() -> str:
        return 'Genres'
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'steam_id',
            'genre'
        ]

@dataclass
class ORMScreenshotURLS(ORMAbstractBase):
    steam_id: int
    thumbnail_url: str
    fullsize_url: str

    @staticmethod
    def get_table_name() -> str:
        return 'ScreenshotURLs'
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'steam_id'
        ]

@dataclass
class ORMAppDetail(ORMAbstractBase):
    steam_id: int
    detailed_description: str
    about_the_game: str
    short_description: str
    header_image_url: str
    metacritic_score: int
    controller_support: bool
    background_image_url: str

    @staticmethod
    def get_table_name() -> str:
        return 'AppDetails'

    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return ('steam_id')
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'metacritic_score',
            'controller_support'
        ]
    
    @staticmethod
    def get_nullable_fields() -> List[str]:
        return [
            'metacritic_score'
        ]

@dataclass
class ORMGame(ORMAbstractBase):
    steam_id: int
    name_on_harddrive: str
    path_on_harddrive: str
    name_on_steam: str
    avg_review_score: int

    @staticmethod
    def get_table_name() -> str:
        return 'Games'

    @staticmethod
    def get_insertion_data(game_model: Game) -> tuple:
        return (
            game_model.steam_id, 
            game_model.name_on_harddrive, 
            game_model.path_on_harddrive, 
            game_model.name_on_steam, 
            game_model.avg_review_score
        )

    @staticmethod
    def needs_multiple_statements() -> bool:
        return False

    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return ('steam_id')
    

python_to_postrgres_type_map = {
    str: "VARCHAR ( 1000 )",
    int: "int",
    bool: "boolean"
}

class StatementCreator(ABC):
    @abstractmethod
    def create(ORMObjectClass: ORMAbstractBase) -> str:
        pass

# CREATE TABLE IF NOT EXISTS AppDetail (
#   steam_id int UNIQUE NOT NULL,
#   detailed_description VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   about_the_game VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   short_description VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   header_image_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   metacritic_score int NOT NULL,
#   controller_support boolean NOT NULL,
#   background_image_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id),
#   PRIMARY KEY (steam_id)
# );
# no user input here - no need to worry about injection attacks
class TableCreatorPostgres(StatementCreator):
    def create(self, ORMObjectClass: ORMAbstractBase) -> str:
        orm_column_title_name_to_type_map = {}
        for f in fields(ORMObjectClass): # XXX get_type_hints
            orm_column_title_name_to_type_map[f.name] = f.type
        return self._get_create_table_statement(orm_column_title_name_to_type_map, ORMObjectClass)

    def _get_create_table_statement(self, orm_column_title_name_to_type_map: Dict[str, type], ORMObjectClass: ORMAbstractBase):
        statement = f"CREATE TABLE IF NOT EXISTS {ORMObjectClass.get_table_name()} (\n"

        #columns
        for column_title, python_type in orm_column_title_name_to_type_map.items():
            postgres_type = python_to_postrgres_type_map[python_type]
            unique_value = " UNIQUE" if column_title not in ORMObjectClass.get_non_unique_mappings() else ""
            null_value = " NOT NULL" if column_title not in ORMObjectClass.get_nullable_fields() else ""
            statement += f"\t{column_title} {postgres_type}{unique_value}{null_value},\n"

        # foreign key
        for column_title, foreign_table in ORMObjectClass.get_foreign_key_mappings().items():
            statement += f"\tFOREIGN KEY ({column_title}) REFERENCES {foreign_table}({column_title}),\n"
        
        # primary key
        primary_key = ORMObjectClass.get_primary_key()
        if primary_key:
            statement += f"\tPRIMARY KEY ({primary_key})\n"
        
        # correct the case where we have a dangling comma.
        # this would happen if we had a foreign key and no primary key
        if statement[-2] == ",":
            # remove dangling comma
            statement = statement[:-2] + statement[-1:]
        
        statement += ");\n"
        return statement

class TableInserterPostgres(StatementCreator):
    def create(self, ORMObjectClass: ORMAbstractBase):
        data_fields = fields(ORMObjectClass)
        data_field_names = [data_field.name for data_field in data_fields]
        placeholders = ["%s"] * len(data_fields)
        sep = ',\n\t'
        statement = f"INSERT INTO {ORMObjectClass.get_table_name()} (\n\t{sep.join(data_field_names)}\n)\nVALUES ({','.join(placeholders)});"
        return statement

class TableSelectPostgres(StatementCreator):
    def create(self, ORMObjectClass: ORMAbstractBase):
        return f"SELECT *\nFROM {ORMObjectClass.get_table_name()};"

@dataclass
# class ORMMapperPostgres:
class StatementCreationFacadePostgres:
    table_creator: TableCreatorPostgres
    table_inserter: TableInserterPostgres
    table_select: TableSelectPostgres
    
    def create_table_statement(self, ORMObjectClass: ORMAbstractBase) -> str:
        return self.table_creator.create(ORMObjectClass)
    
    def get_insert_data_statement(self, ORMObjectClass: ORMAbstractBase):
        return self.table_inserter.create(ORMObjectClass)
    
    def get_select_statement(self, ORMObjectClass: ORMAbstractBase):
        return self.table_select.create(ORMObjectClass)

class StatementCreationFacadePostgresFactory:
    def create(self) -> StatementCreationFacadePostgres:
        table_creator = TableCreatorPostgres()
        table_inserter = TableInserterPostgres()
        table_select = TableSelectPostgres()
        orm_mapper = StatementCreationFacadePostgres(table_creator, table_inserter, table_select)
        return orm_mapper

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

    def create_tables(self, database_interaction_func: Callable):
        for ORMClass in self.ORMClasses:
            table_create_statement = self.statement_creation.create_table_statement(ORMClass)
            database_interaction_func(table_create_statement)
    
    def insert_game(self, database_interaction_func: Callable):
        for ORMClass in self.ORMClasses:
            insert_statement = self.statement_creation.get_insert_data_statement(ORMClass)
            database_interaction_func(insert_statement, ORMClass.)

f = StatementCreationFacadePostgresFactory()
o = ORMMapper(f.create())
o.create_tables(print)
# statement_creation_facade_postrgres_factory = StatementCreationFacadePostgresFactory()
# statement_creation_facade = statement_creation_facade_postrgres_factory.create()

print(get_type_hints(ORMDevelopers))