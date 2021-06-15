from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Dict, List, Tuple

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
# AppDetail:
#     steam_id: int
#     detailed_description: str
#     about_the_game: str
#     short_description: str
#     header_image_url: str
#     metacritic_score: int, Null
#     controller_support: bool
#     background_image_url: str

# CREATE TABLE IF NOT EXISTS Developers (
#   steam_id int NOT NULL,
#   developer VARCHAR ( 1000 ) NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id)
# );
# # many
# developers:
#     steam_id: int
#     developer: str

# CREATE TABLE IF NOT EXISTS Publishers (
#   steam_id int NOT NULL,
#   publisher VARCHAR ( 1000 ) NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id)
# );
# # many
# publishers:
#     steam_id: int
#     publisher: str

# CREATE TABLE IF NOT EXISTS Genres (
#   steam_id int NOT NULL,
#   genre VARCHAR ( 1000 ) NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id)
# );
# # many
# genres:
#     steam_id: int
#     genre: str

# CREATE TABLE IF NOT EXISTS ScreenshotURLs (
#   steam_id int NOT NULL,
#   thumbnail_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   fullsize_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id)
# );
# # many
# screenshot_urls:
#     steam_id: int
#     thumbnail_url: str
#     fullsize_url: str




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
# CREATE TABLE IF NOT EXISTS ScreenshotURLs (
#   steam_id int NOT NULL,
#   thumbnail_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   fullsize_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id)
# );
# CREATE TABLE IF NOT EXISTS Games (
#   steam_id int NOT NULL,
#   name_on_harddrive VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   path_on_harddrive VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   name_on_steam VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   avg_review_score DOUBLE PRECISION NOT NULL,
#   PRIMARY KEY (steam_id)
# );
class ORMAbstractBase(ABC):
    @staticmethod
    @abstractmethod
    def get_table_name() -> str:
        return ""

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
            'steam_id',
            'controller_support'
        ]

# XXX Weakness of this approach: have the types defined in two places. AppDetail and here
# Could just replace all this with Django 
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

# XXX Weakness of this approach: have the types defined in two places. AppDetail and here
# Could just replace all this with Django 
@dataclass
class ORMGame(ORMAbstractBase):
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
        return 'Games'

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
python_to_postrgres_type_map = {
    str: "VARCHAR ( 1000 )",
    int: "int",
    bool: "boolean"
}

class TableCreatorBase(ABC):
    @abstractmethod
    def create(orm_object: ORMAbstractBase) -> str:
        pass

# no user input here - no need to worry about injection attacks
class TableCreatorPostrgres(TableCreatorBase):
    def create(self, orm_object: ORMAbstractBase) -> str:
        orm_column_title_name_to_type_map = {}
        for f in fields(orm_object):
            orm_column_title_name_to_type_map[f.name] = f.type
        return self._get_create_table_statement(orm_column_title_name_to_type_map, orm_object)

    def _get_create_table_statement(self, orm_column_title_name_to_type_map: Dict[str, type], ORMObject: ORMAbstractBase):
        statement = f"CREATE TABLE IF NOT EXISTS {ORMObject.get_table_name()} (\n"

        #columns
        for column_title, python_type in orm_column_title_name_to_type_map.items():
            postgres_type = python_to_postrgres_type_map[python_type]
            unique_value = " UNIQUE" if column_title not in ORMObject.get_non_unique_mappings() else ""
            null_value = " NOT NULL" if column_title not in ORMObject.get_nullable_fields() else ""
            statement += f"\t{column_title} {postgres_type}{unique_value}{null_value},\n"

        # foreign key
        for column_title, foreign_table in ORMObject.get_foreign_key_mappings().items():
            statement += f"\tFOREIGN KEY ({column_title}) REFERENCES {foreign_table}({column_title}),\n"
        
        # primary key
        primary_key = ORMObject.get_primary_key()
        if primary_key:
            statement += f"\tPRIMARY KEY ({primary_key})\n"
        
        statement += ");\n"
        return statement

class ORMMapper:
    def __init__(self, table_creator: TableCreatorBase):
        self.table_creator = table_creator
    
    def create_table_statement(self, orm_object: ORMAbstractBase) -> str:
        return self.table_creator.create(orm_object)

        
    

table_creator = TableCreatorPostrgres()
x = ORMMapper(table_creator)
print(x.create_table_statement(ORMAppDetail))
print(x.create_table_statement(ORMScreenshotURLS))
# create:
#     names of collumns
#     types of columns
#     table name