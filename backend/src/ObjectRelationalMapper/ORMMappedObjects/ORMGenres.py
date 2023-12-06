from typing import Dict, List
from Game.GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase


@dataclass
class ORMGenres(ORMAbstractBase):
    steam_id: int
    genre: str

    @staticmethod
    def get_table_name() -> str:
        return "Genres"

    @staticmethod
    def get_insertion_data(game_model: Game) -> tuple:
        genres = game_model.app_detail.genres
        genre_data = tuple((game_model.steam_id, genre) for genre in genres)
        return genre_data

    @staticmethod
    def needs_multiple_statements() -> bool:
        return True

    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id": "Games"}

    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return ["steam_id", "genre"]
