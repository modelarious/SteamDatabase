from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple
from GameModel import Game

@dataclass
class ORMAbstractBase(ABC):
    steam_id: int

    @staticmethod
    @abstractmethod
    def get_table_name() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_insertion_data(game_model: Game) -> tuple:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def needs_multiple_statements() -> bool:
        raise NotImplementedError

    # return a tuple of names of columns that are part of primary key 
    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return ()
    
    # in the form of "column_name": "ForeignTable" which becomes 
    # FOREIGN KEY (column_name) REFERENCES ForeignTable(column_name)
    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {}

    # names of columns that contain values that won't be unique
    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return []
    
    # names of columns that may be null
    @staticmethod
    def get_nullable_fields() -> List[str]:
        return []
