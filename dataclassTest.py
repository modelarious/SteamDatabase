from itertools import repeat
from ExternalDataFetchers.AppDetail import AppDetail, ScreenshotURL
from GameModel import Game
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Any, Callable, Dict, List, Tuple, get_type_hints

class ORMAbstractBase(ABC):
    @staticmethod
    @abstractmethod
    def get_table_name() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_insertion_data(game_model: Game) -> tuple:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def needs_multiple_statements() -> bool:
        raise NotImplementedError

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
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'avg_review_score',
        ]

@dataclass
class ORMUserDefinedGenres(ORMAbstractBase):
    steam_id: int
    genre_name: str
    rank: int

    @staticmethod
    def get_table_name() -> str:
        return 'UserDefinedGenres'

    @staticmethod
    def get_insertion_data(game_model: Game) -> tuple:
        steam_id_iter = repeat(game_model.steam_id)
        rank = range(1, (len(game_model.user_defined_genres) + 1))
        genre_data = tuple(zip(steam_id_iter, game_model.user_defined_genres, rank))
        return genre_data
    
    @staticmethod
    def needs_multiple_statements() -> bool:
        return True

    @staticmethod
    def needs_multiple_statements() -> bool:
        return True
    
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
    def get_insertion_data(game_model: Game) -> tuple:
        publishers = game_model.app_detail.publishers
        publisher_data = tuple(
            (game_model.steam_id, publisher) for publisher in publishers
        )
        return publisher_data

    @staticmethod
    def needs_multiple_statements() -> bool:
        return True
    
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
    def get_insertion_data(game_model: Game) -> tuple:
        developers = game_model.app_detail.developers
        developer_data = tuple(
            (game_model.steam_id, developer) for developer in developers
        )
        return developer_data

    @staticmethod
    def needs_multiple_statements() -> bool:
        return True

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
    def get_insertion_data(game_model: Game) -> tuple:
        genres = game_model.app_detail.genres
        genre_data = tuple(
            (game_model.steam_id, genre) for genre in genres
        )
        return genre_data

    @staticmethod
    def needs_multiple_statements() -> bool:
        return True
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'steam_id',
            'genre'
        ]

# @dataclass
# class ORMScreenshotURLS(ORMAbstractBase):
#     steam_id: int
#     thumbnail_url: str
#     fullsize_url: str

#     @staticmethod
#     def get_table_name() -> str:
#         return 'ScreenshotURLs'
    
#     # XXX this isn't going to work, you need to unpack the screenshot url stuff
#     @staticmethod
#     def get_insertion_data(game_model: Game) -> tuple:
#         screenshot_urls = game_model.app_detail.screenshot_urls
#         screenshot_url_data = tuple(
#             (game_model.steam_id, thumbnail_url, fullsize_url) for thumbnail_url, fullsize_url in screenshot_urls
#         )
#         return screenshot_url_data

    # @staticmethod
    # def needs_multiple_statements() -> bool:
    #     return True
    
#     @staticmethod
#     def get_foreign_key_mappings() -> Dict[str, str]:
#         return {"steam_id" : "Games"}
    
#     @staticmethod
#     def get_non_unique_mappings() -> List[str]:
#         return [
#             'steam_id'
#         ]

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
    def get_insertion_data(game_model: Game) -> tuple:
        app_detail = game_model.app_detail
        app_detail_data = (
            game_model.steam_id,
            app_detail.detailed_description,
            app_detail.about_the_game,
            app_detail.short_description,
            app_detail.header_image_url,
            app_detail.metacritic_score,
            app_detail.controller_support,
            app_detail.background_image_url,
        )
        return app_detail_data
    
    @staticmethod
    def needs_multiple_statements() -> bool:
        return False

    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return ('steam_id')
    
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id" : "Games"}
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'detailed_description',
            'about_the_game',
            'short_description',
            'metacritic_score',
            'controller_support'
        ]
    
    @staticmethod
    def get_nullable_fields() -> List[str]:
        return [
            'metacritic_score'
        ]

python_to_postrgres_type_map = {
    str: "VARCHAR ( 10000 )",
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
        return self._get_create_table_statement(get_type_hints(ORMObjectClass), ORMObjectClass)

    def _get_create_table_statement(self, orm_column_title_name_to_type_map: Dict[str, type], ORMObjectClass: ORMAbstractBase):
        statement = f"CREATE TABLE IF NOT EXISTS {ORMObjectClass.get_table_name()} (\n"
        statement += self._get_columns(orm_column_title_name_to_type_map, ORMObjectClass)
        statement += self._get_foreign_key_mappings(ORMObjectClass)
        statement += self._get_primary_key_mapping(ORMObjectClass)
        
        # correct the case where we have a dangling comma.
        # this would happen if we had a foreign key and no primary key
        if statement[-2] == ",":
            # remove dangling comma
            statement = statement[:-2] + statement[-1:]
        
        statement += ");\n"
        return statement
    
    def _get_columns(self, title_to_type_map: Dict[str, type], ORMObjectClass: ORMAbstractBase) -> str:
        statement_addition = ""
        for column_title, python_type in title_to_type_map.items():
            try:
                postgres_type = python_to_postrgres_type_map[python_type]
            except KeyError as e:
                raise KeyError(f"Had issue with column {column_title} for class {ORMObjectClass}\n {e}")
            unique_value = " UNIQUE" if column_title not in ORMObjectClass.get_non_unique_mappings() else ""
            null_value = " NOT NULL" if column_title not in ORMObjectClass.get_nullable_fields() else ""
            statement_addition += f"\t{column_title} {postgres_type}{unique_value}{null_value},\n"
        return statement_addition

    def _get_foreign_key_mappings(self, ORMObjectClass: ORMAbstractBase) -> str:
        statement_addition = ""
        for column_title, foreign_table in ORMObjectClass.get_foreign_key_mappings().items():
            statement_addition += f"\tFOREIGN KEY ({column_title}) REFERENCES {foreign_table}({column_title}),\n"
        return statement_addition
    
    def _get_primary_key_mapping(self, ORMObjectClass: ORMAbstractBase) -> str:
        primary_key = ORMObjectClass.get_primary_key()
        if primary_key:
            return f"\tPRIMARY KEY ({primary_key})\n"
        return ""

class TableInserterPostgres(StatementCreator):
    def create(self, ORMObjectClass: ORMAbstractBase):
        data_fields = fields(ORMObjectClass)
        data_field_names = [data_field.name for data_field in data_fields]
        placeholders = ["%s"] * len(data_fields)
        seper = ',\n\t'
        statement = f"INSERT INTO {ORMObjectClass.get_table_name()} (\n\t{seper.join(data_field_names)}\n)\nVALUES ({','.join(placeholders)});"
        return statement

class TableSelectPostgres(StatementCreator):
    def create(self, ORMObjectClass: ORMAbstractBase):
        return f"SELECT *\nFROM {ORMObjectClass.get_table_name()};"

@dataclass
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
            # ORMScreenshotURLS
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

g = Game(
    steam_id=25980, 
    name_on_harddrive='Majesty', 
    path_on_harddrive='/Volumes/babyBlue/Games/PC/Majesty', 
    name_on_steam='Majesty 2', 
    avg_review_score=5, 
    user_defined_genres=['Strategy', 'Simulation', 'Fantasy', 'Singleplayer', 'RTS', 'Difficult', 'Base Building', 'City Builder', 'Multiplayer'], 
    app_detail=AppDetail(
        detailed_description='In the world of Majesty, you are the ruler of the kingdom Ardania. At your service are your loyal and somewhat obnoxious subordinates, who have their own minds about how things should be done.<br>\t\t\t\t\tIn fact, Majesty is the only game where your heroes decide on their own what should be done and when, leaving you to try to control them through monetary incentives.<br>\t\t\t\t\tKey Features<br>\t\t\t\t\t<ul class="bb_ul"><li>Real-time strategy game with indirect control - your heroes have a will of their own.<br>\t\t\t\t\t</li><li>Play through a campaign with 16 missions divided into 4 chapters, as well as a few quick missions and a variety of multiplayer maps.<br>\t\t\t\t\t</li><li>Build the fantasy city of your dreams and experience an engaging world, but beware: monsters are waiting to lay siege to your domain.<br>\t\t\t\t\t</li><li>Defend your realm with noble warriors, spell-wielding wizards or wild barbarians. Choose from more than 10 different classes to oversee the protection of your lands.<br>\t\t\t\t\t</li><li>Multiplayer for up to 4 players over LAN<br>\t\t\t\t\t</li><li>The official sequel to the best-selling game Majesty: The Fantasy Kingdom Sim of 2000.<br>\t\t\t\t\t</li></ul>', 
        about_the_game='In the world of Majesty, you are the ruler of the kingdom Ardania. At your service are your loyal and somewhat obnoxious subordinates, who have their own minds about how things should be done.<br>\t\t\t\t\tIn fact, Majesty is the only game where your heroes decide on their own what should be done and when, leaving you to try to control them through monetary incentives.<br>\t\t\t\t\tKey Features<br>\t\t\t\t\t<ul class="bb_ul"><li>Real-time strategy game with indirect control - your heroes have a will of their own.<br>\t\t\t\t\t</li><li>Play through a campaign with 16 missions divided into 4 chapters, as well as a few quick missions and a variety of multiplayer maps.<br>\t\t\t\t\t</li><li>Build the fantasy city of your dreams and experience an engaging world, but beware: monsters are waiting to lay siege to your domain.<br>\t\t\t\t\t</li><li>Defend your realm with noble warriors, spell-wielding wizards or wild barbarians. Choose from more than 10 different classes to oversee the protection of your lands.<br>\t\t\t\t\t</li><li>Multiplayer for up to 4 players over LAN<br>\t\t\t\t\t</li><li>The official sequel to the best-selling game Majesty: The Fantasy Kingdom Sim of 2000.<br>\t\t\t\t\t</li></ul>', 
        short_description='In the world of Majesty, you are the ruler of the kingdom Ardania. At your service are your loyal and somewhat obnoxious subordinates, who have their own minds about how things should be done. In fact, Majesty is the only game where your heroes decide on their own what should be done and when, leaving you to try to control them through...', 
        header_image_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/header.jpg?t=1589874163', 
        developers=['1C:InoCo'], 
        publishers=['Paradox Interactive'], 
        metacritic_score=72, 
        controller_support=False, 
        genres=['Simulation', 'Strategy'], 
        screenshot_urls=[
            ScreenshotURL(
                thumbnail_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_ce55a06230779d50fa943342eaf3c2efe0b5ba9d.600x338.jpg?t=1589874163', 
                fullsize_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_ce55a06230779d50fa943342eaf3c2efe0b5ba9d.1920x1080.jpg?t=1589874163'
            ), 
            ScreenshotURL(
                thumbnail_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_3e00a49d83e3a025e9a0f076ff611a24468c60a9.600x338.jpg?t=1589874163', 
                fullsize_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_3e00a49d83e3a025e9a0f076ff611a24468c60a9.1920x1080.jpg?t=1589874163'
            ), 
            ScreenshotURL(
                thumbnail_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_4f1caccfbec2ac8514bf95f608c7f77819235484.600x338.jpg?t=1589874163', 
                fullsize_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_4f1caccfbec2ac8514bf95f608c7f77819235484.1920x1080.jpg?t=1589874163'
            ), 
            ScreenshotURL(
                thumbnail_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_719ab90c7101005c546147f89bbfd3a3f96013c9.600x338.jpg?t=1589874163', 
                fullsize_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_719ab90c7101005c546147f89bbfd3a3f96013c9.1920x1080.jpg?t=1589874163'
            ), 
            ScreenshotURL(
                thumbnail_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_60d582eec84883ad325533ffd0d6e57478aa1d9c.600x338.jpg?t=1589874163', 
                fullsize_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/ss_60d582eec84883ad325533ffd0d6e57478aa1d9c.1920x1080.jpg?t=1589874163'
            )
        ], 
        background_image_url='https://cdn.akamai.steamstatic.com/steam/apps/25980/page_bg_generated_v6b.jpg?t=1589874163'
    )
)

f = StatementCreationFacadePostgresFactory()
o = ORMMapper(f.create())
o.create_tables(print)
# o.insert_game(print, print, g)