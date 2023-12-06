from typing import Dict, List
from Game.GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase


@dataclass
class ORMDevelopers(ORMAbstractBase):
    steam_id: int
    developer: str

    @staticmethod
    def get_table_name() -> str:
        return "Developers"

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
        return {"steam_id": "Games"}

    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return ["steam_id", "developer"]
