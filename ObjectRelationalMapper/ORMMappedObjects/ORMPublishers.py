from typing import Dict, List
from GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase

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
