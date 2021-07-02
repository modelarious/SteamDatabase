from typing import List, Tuple
from GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase

@dataclass
class ORMGame(ORMAbstractBase):
    steam_id: int
    game_name_on_disk: str
    path_on_harddrive: str
    game_name_from_steam: str
    avg_review_score: int

    @staticmethod
    def get_table_name() -> str:
        return 'Games'

    @staticmethod
    def get_insertion_data(game_model: Game) -> tuple:
        return (
            game_model.steam_id, 
            game_model.game_name_on_disk, 
            game_model.path_on_harddrive, 
            game_model.game_name_from_steam, 
            game_model.avg_review_score
        )

    @staticmethod
    def needs_multiple_statements() -> bool:
        return False

    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return ('steam_id')
    
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            'avg_review_score',
        ]