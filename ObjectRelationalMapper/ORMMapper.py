
from re import S
from GameModel import Game
from typing import Any, Callable, Dict, List, Tuple, Type
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

    # this is the worst function in the entire project - if you want to improve anything you should try here 
    def get_all_games(self, database_interaction_func: Callable[[str, tuple], Any]):
        all_games = []

        returned_data = {}
        for ORMClass in self.ORMClasses:
            sql = self.statement_creation.get_select_statement(ORMClass)
            selected_data_from_db = database_interaction_func(sql)
            class_name = self._get_class_name(ORMClass)
            print(f"{class_name} : {selected_data_from_db}")
            if class_name not in returned_data:
                returned_data[class_name] = {}

            # XXX Ugh, you need special handling for ranked arrays too - this is a disaster!
            # XXX I was tired when I wrote this and just wanted it to work
            if ORMClass.needs_multiple_statements():
                if ORMClass == ORMUserDefinedGenres:
                    # returned_data[class_name] = ranked_array(selected_data_from_db)
                    # sort by rank so that you always encounter ranked items in correct order
                    for row in sorted(selected_data_from_db, key=lambda r: r[2]):
                        steam_id = row[0]
                        genre = row[1]
                        rank = row[2]
                        if steam_id not in returned_data[class_name]:
                            returned_data[class_name][steam_id] = []
                        returned_data[class_name][steam_id].append(genre)

                else:
                    for row in selected_data_from_db:
                        steam_id = row[0]
                        array_entry = row[1:]
                        if steam_id not in returned_data[class_name]:
                            returned_data[class_name][steam_id] = []
                        returned_data[class_name][steam_id].append(array_entry)
            else: 
                for row in selected_data_from_db:
                    steam_id = row[0]
                    rest = row[1:]
                    returned_data[class_name][steam_id] = rest
            
        
        # if no games were returned from query, then return blank array
        game_class_name = self._get_class_name(ORMGame)
        if game_class_name not in returned_data:
            return all_games
        
        # XXX the right way to do this would be to make something that requests data that matches the field name_on_harddrive.
        # it would then go through the ORMClasses to find one with a matching field name, and pull the data out of the corresponding
        # place in returned_data.  For example, it would work out that name_on_harddrive is the second member variable of ORMGame after
        # the obligatory steam_id. Since we are 0-indexing, this means name_on_harddrive would be at index 1 in the return from the
        # database.  Since we are using the steam_id as the key, this means that name_on_harddrive is actually at index 0 in the
        # associated data in returned_data.  
        # It would thus look up 
        # returned_data[ORMGame.__name__][steam_id][0] 
        # and return that value
        # This could be sped up by using memoization of where to find each field instead of looking through all the ORMClasses every time.
        # Note you could also use something like @redis_simple_cache to do memoiziation
        for steam_id in returned_data[game_class_name].keys():
            try:

                game_data = returned_data[game_class_name][steam_id]
                user_defined_genres = returned_data[self._get_class_name(ORMUserDefinedGenres)][steam_id]
                game_model = Game(
                    steam_id,
                    name_on_harddrive=game_data[0],
                    path_on_harddrive=game_data[1],
                    name_on_steam=game_data[2],
                    avg_review_score=game_data[3],
                    user_defined_genres=user_defined_genres,
                    app_detail=[]
                )
                print(game_model)
            except Exception as e:
                print("yup, as expected", e)

    def _get_class_name(self, Class: Type) -> str:
        return Class.__name__



# XXX the logic here is pretty much the same logic used in the other functions, you could likely consolidate it

# sort by rank so that you always encounter ranked items in correct order
def ranked_array(selected_data_from_db: List[Tuple]) -> Dict[str, List[str]]:
    gathered_values = {}
    # sort by rank - XXX NOTE this is not generic - and if you plan to make it generic you should make a standard
    # such as "rank is always the second column" to follow the "steam_id is always the first column" rule
    for row in sorted(selected_data_from_db, key=lambda r: r[2]):
        steam_id = row[0]
        value = row[1]
        # rank = row[2]
        if steam_id not in gathered_values:
            gathered_values[steam_id] = []
        gathered_values[steam_id].append(value)
    return gathered_values

def unranked_array(selected_data_from_db: List[Tuple]) -> Dict[str, List[str]]:
    gathered_values = {}
    for row in selected_data_from_db:
        steam_id = row[0]
        array_entry = row[1:]
        if steam_id not in gathered_values:
            gathered_values[steam_id] = []
        gathered_values[steam_id].append(array_entry)
    return gathered_values

def unique_values(selected_data_from_db: List[Tuple]) -> Dict[str, List[str]]:
    gathered_values = {}
    for row in selected_data_from_db:
        steam_id = row[0]
        rest = row[1:]
        gathered_values[steam_id] = rest
    return gathered_values
    