from itertools import repeat
from typing import Dict, List
from GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase

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