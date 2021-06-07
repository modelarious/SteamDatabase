
from itertools import repeat

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
            insertTags = "INSERT INTO UserDefinedGenres (steam_id, genre_name, rank) VALUES (%s, %s, %s);"
            steamIDIter = repeat(gameModel.steam_id)
            rank = range(1, (len(gameModel.user_defined_tags) + 1))
            
            tagData = tuple(zip(steamIDIter, gameModel.user_defined_tags, rank))
            cur.executemany(insertTags, tagData)
            
            conn.commit()
        conn.close()