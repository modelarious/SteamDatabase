from Database.PostgresConnectionFactory import PostgresConnectionFactory
from ObjectRelationalMapper.ORMMapper import ORMMapper
from typing import List
from Game.GameModel import Game


class PostgresGameDAO:
    def __init__(
        self, connection_factory: PostgresConnectionFactory, orm_mapper: ORMMapper
    ):
        self.connection_factory = connection_factory
        self.orm_mapper = orm_mapper

    def create_tables(self):
        conn = self._get_connection()
        with conn.cursor() as cur:
            self.orm_mapper.create_tables(cur.execute)
            conn.commit()
        conn.close()

    def commit_game(self, game_model: Game):
        conn = self._get_connection()
        with conn.cursor() as cur:
            self.orm_mapper.insert_game(cur.execute, cur.executemany, game_model)
            conn.commit()
        conn.close()

    def get_all_games(self) -> List[Game]:
        conn = self._get_connection()
        with conn.cursor() as cur:

            def _select_execute_and_return_value_wrapper(query):
                cur.execute(query)
                return cur.fetchall()

            all_games = self.orm_mapper.get_all_games(
                _select_execute_and_return_value_wrapper
            )
        return all_games

    def get_titles_of_all_stored_games(self) -> List[str]:
        conn = self._get_connection()
        query_returns = []
        with conn.cursor() as cur:
            get_game_titles_query = "SELECT game_name_on_disk from Games"
            cur.execute(get_game_titles_query)
            query_returns = cur.fetchall()

        paths = [ret[0] for ret in query_returns]
        return paths

    def _get_connection(self):
        return self.connection_factory.createConnection()
