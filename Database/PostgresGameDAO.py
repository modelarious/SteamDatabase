from itertools import repeat
from typing import List
from GameModel import Game
from abc import ABC, abstractmethod

class ObjectRelationalMapperInterface(ABC):
    @abstractmethod
    def get_sql_statement(self) -> str:
        pass

    # return data that will be inserted by the sql statement
    @abstractmethod
    def get_insertion_data(self, game_model: Game) -> tuple:
        pass
    
    # indicate if we are storing a list of values
    @abstractmethod
    def needs_multiple_statements(self) -> bool:
        pass

    # @abstractmethod
    # def store(self, cur):
    #     pass

    # # for use when selecting all values from database
    # @abstractmethod
    # def retrieve_all(self, cur) -> tuple:
    #     pass

# XXX this has a super bad name, it seems like this is the only ORM you would need
# but in reality you need many more
class GameORM(ObjectRelationalMapperInterface):
    def get_sql_statement(self) -> str:
        return """
            INSERT INTO Games (
                steam_id, 
                name_on_harddrive, 
                path_on_harddrive, 
                name_on_steam, 
                avg_review_score
            ) VALUES (%s, %s, %s, %s, %s);
        """

    def get_insertion_data(self, game_model: Game) -> tuple:
        return (
            game_model.steam_id, 
            game_model.name_on_harddrive, 
            game_model.path_on_harddrive, 
            game_model.name_on_steam, 
            game_model.avg_review_score
        )

    def needs_multiple_statements(self) -> bool:
        return False
    
    # def get_all_values(self) -> tuple:
        

class UserDefinedGenresORM(ObjectRelationalMapperInterface):
    def get_sql_statement(self) -> str:
        return """
            INSERT INTO UserDefinedGenres (
                steam_id, 
                genre_name, 
                rank
            ) VALUES (%s, %s, %s);
        """

    def get_insertion_data(self, game_model: Game) -> tuple:
        steam_id_iter = repeat(game_model.steam_id)
        rank = range(1, (len(game_model.user_defined_genres) + 1))
        genre_data = tuple(zip(steam_id_iter, game_model.user_defined_genres, rank))
        return genre_data

    def needs_multiple_statements(self) -> bool:
        return True

class PostgresGameDAO:
    def __init__(self, connectionFactory):
        self.connectionFactory = connectionFactory

    def commitGame(self, game_model: Game):
        conn = self.connectionFactory.createConnection()
        with conn.cursor() as cur:
            insertions = [
                GameORM(),
                UserDefinedGenresORM()
            ]

            for statement_builder in insertions:
                sql = statement_builder.get_sql_statement()
                insertion_data = statement_builder.get_insertion_data(game_model)
                non_commit_insertion_func = cur.execute
                if statement_builder.needs_multiple_statements():
                    non_commit_insertion_func = cur.executemany
                non_commit_insertion_func(sql, insertion_data)

            # app detail
            # ---------------------------
            insert_app_detail = """
                INSERT INTO AppDetail (
                    steam_id,
                    detailed_description,
                    about_the_game,
                    short_description,
                    header_image_url,
                    metacritic_score,
                    controller_support,
                    background_image_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            # many
            insert_developer = """
                INSERT INTO developers (
                    steam_id,
                    developer
                ) VALUES (%s, %s);
            """
            # many
            insert_publisher = """
                INSERT INTO publishers (
                    steam_id,
                    publisher
                ) VALUES (%s, %s);
            """
            # many
            insert_genre = """
                INSERT INTO genres (
                    steam_id,
                    genre
                ) VALUES (%s, %s);
            """
            # many
            insert_screenshot = """
                INSERT INTO screenshots (
                    steam_id,
                    thumbnail_url,
                    fullsize_url
                ) VALUES (%s, %s, %s);
            """
            
            conn.commit()
        conn.close()
    
    def get_paths_of_all_stored_games(self) -> List[str]:
        conn = self.connectionFactory.createConnection()
        query_returns = []
        with conn.cursor() as cur:
            get_game_titles_query = "SELECT path_on_harddrive from Games"
            cur.execute(get_game_titles_query)
            query_returns = cur.fetchall()
        
        paths = [ret[0] for ret in query_returns]
        return paths
        

# AppDetail:
#     steam_id: int
#     detailed_description: str
#     about_the_game: str
#     short_description: str
#     header_image_url: str
#     metacritic_score: int, Null
#     controller_support: bool
#     background_image_url: str

# # many
# developers:
#     steam_id: int
#     developer: str

# # many
# publishers:
#     steam_id: int
#     publisher: str

# # many
# genres:
#     steam_id: int
#     genre: str

# screenshot_urls:
#     steam_id: int
#     thumbnail_url: str
#     fullsize_url: str