from itertools import repeat
from dataclasses import dataclass
from typing import List


class PostgresGameDAO:
    def __init__(self, connectionFactory):
        self.connectionFactory = connectionFactory

    def commitGame(self, gameModel):
        conn = self.connectionFactory.createConnection()
        with conn.cursor() as cur:
            insertGame = "INSERT INTO Games (steam_id, name_on_harddrive, path_on_harddrive, name_on_steam, avg_review_score) VALUES (%s, %s, %s, %s, %s);"
            gameData = (gameModel.steam_id, gameModel.name_on_harddrive, gameModel.path_on_harddrive, gameModel.name_on_steam, gameModel.avg_review_score)
            cur.execute(insertGame, gameData) # doing it this way prevents sql injection

            # these are similar to genres as defined by users
            insertGenres = "INSERT INTO UserDefinedGenres (steam_id, genre_name, rank) VALUES (%s, %s, %s);"
            steamIDIter = repeat(gameModel.steam_id)
            rank = range(1, (len(gameModel.user_defined_genres) + 1))
            
            genreData = tuple(zip(steamIDIter, gameModel.user_defined_genres, rank))
            cur.executemany(insertGenres, genreData)
            
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
        
