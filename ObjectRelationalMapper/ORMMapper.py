
from ExternalDataFetchers.AppDetail import AppDetail, ScreenshotURL
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from re import S
from GameModel import Game
from typing import Any, Callable, Dict, List, Tuple, Type, Union
from ObjectRelationalMapper.ORMMappedObjects.ORMScreenshotURLs import ORMScreenshotURLS
from ObjectRelationalMapper.ORMMappedObjects.ORMGenres import ORMGenres
from ObjectRelationalMapper.ORMMappedObjects.ORMDevelopers import ORMDevelopers
from ObjectRelationalMapper.ORMMappedObjects.ORMPublishers import ORMPublishers
from ObjectRelationalMapper.ORMMappedObjects.ORMAppDetail import ORMAppDetail
from ObjectRelationalMapper.ORMMappedObjects.ORMUserDefinedGenres import ORMUserDefinedGenres
from ObjectRelationalMapper.ORMMappedObjects.ORMGame import ORMGame
from ObjectRelationalMapper.StatementCreation.StatementCreationFacadePostgres import StatementCreationFacadePostgres

# This is required because I don't currently have a way to build back the the Game object without
# specifically referencing which ORM parts go where.  I don't like it
class GrossGameRemapper:
    def __init__(self):
        self.game_output = []

    def remap_to_game(self) -> Game:
        pass

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

    def get_all_games(self, database_interaction_func: Callable[[str, tuple], Any]):
        def group_values(ORMClass: Type[ORMAbstractBase], data_to_group: List[ORMAbstractBase]):
            if ORMClass.needs_multiple_statements():
                return array_handler(data_to_group)
            else:
                return unique_value_handler(data_to_group)

        def get_class_name(Class: Type) -> str:
            return Class.__name__

        all_games = []

        returned_data = {}
        for ORMClass in self.ORMClasses:
            sql = self.statement_creation.get_select_statement(ORMClass)
            selected_data_from_db = database_interaction_func(sql)
            mapped_data = [ORMClass(*row) for row in selected_data_from_db]
            class_name = get_class_name(ORMClass)
            returned_data[class_name] = group_values(ORMClass, mapped_data)

        # data returned is indexed by steam_id. it is of one of two formats, an array or a single object:
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

        def get_associated_data(ORMClass: Type[ORMAbstractBase], steam_id: int) -> Dict[int,Union[ORMAbstractBase, List[ORMAbstractBase]]]:
            return returned_data[get_class_name(ORMClass)][steam_id]

        # if no games were returned from query, then return blank array
        game_class_name = get_class_name(ORMGame)
        if game_class_name not in returned_data:
            return all_games

        for steam_id in returned_data[game_class_name].keys():
            try:
                app_detail_data = get_associated_data(ORMAppDetail, steam_id)
                screenshot_data = get_associated_data(ORMScreenshotURLS, steam_id)
                developer_data = get_associated_data(ORMDevelopers, steam_id)
                publisher_data = get_associated_data(ORMPublishers, steam_id)
                genre_data = get_associated_data(ORMGenres, steam_id)

                publishers = [
                    orm_publisher.publisher for orm_publisher in publisher_data
                ]
                developers = [
                    orm_developer.developer for orm_developer in developer_data
                ]
                genres = [
                    orm_genre.genre for orm_genre in genre_data
                ]
                screenshots = [
                    ScreenshotURL(orm_screenshot.thumbnail_url, orm_screenshot.fullsize_url) for orm_screenshot in screenshot_data
                ]

                app_detail = AppDetail(
                    detailed_description=app_detail_data.detailed_description,
                    about_the_game=app_detail_data.about_the_game,
                    short_description=app_detail_data.short_description,
                    header_image_url=app_detail_data.header_image_url,
                    publishers=publishers,
                    developers=developers,
                    metacritic_score=app_detail_data.metacritic_score,
                    controller_support=app_detail_data.controller_support,
                    genres=genres,
                    screenshot_urls=screenshots,
                    background_image_url=app_detail_data.background_image_url
                )

                game_data = get_associated_data(ORMGame, steam_id)
                user_defined_genre_data = get_associated_data(ORMUserDefinedGenres, steam_id)

                user_defined_genres = [user_defined_genre_orm.genre_name for user_defined_genre_orm in user_defined_genre_data]
                game_model = Game(
                    steam_id,
                    name_on_harddrive=game_data.name_on_harddrive,
                    path_on_harddrive=game_data.path_on_harddrive,
                    name_on_steam=game_data.name_on_steam,
                    avg_review_score=game_data.avg_review_score,
                    user_defined_genres=user_defined_genres,
                    app_detail=app_detail
                )
            except Exception as e:
                print("yup, as expected", e)

def array_handler(orm_instances: List[ORMAbstractBase]) -> Dict[str, List[str]]:
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

def unique_value_handler(orm_instances: List[ORMAbstractBase]) -> Dict[str, List[str]]:
    gathered_values = {}
    for orm_instance in orm_instances:
        gathered_values[orm_instance.steam_id] = orm_instance
    return gathered_values
