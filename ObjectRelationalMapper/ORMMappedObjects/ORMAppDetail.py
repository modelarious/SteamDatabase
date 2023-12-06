from typing import Dict, List, Tuple
from GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase


@dataclass
class ORMAppDetail(ORMAbstractBase):
    steam_id: int
    detailed_description: str
    about_the_game: str
    short_description: str
    header_image_url: str
    metacritic_score: int
    controller_support: bool
    background_image_url: str

    @staticmethod
    def get_table_name() -> str:
        return "AppDetails"

    @staticmethod
    def get_insertion_data(game_model: Game) -> tuple:
        app_detail = game_model.app_detail
        app_detail_data = (
            game_model.steam_id,
            app_detail.detailed_description,
            app_detail.about_the_game,
            app_detail.short_description,
            app_detail.header_image_url,
            app_detail.metacritic_score,
            app_detail.controller_support,
            app_detail.background_image_url,
        )
        return app_detail_data

    @staticmethod
    def needs_multiple_statements() -> bool:
        return False

    @staticmethod
    def get_primary_key() -> Tuple[str]:
        return "steam_id"

    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id": "Games"}

    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return [
            "detailed_description",
            "about_the_game",
            "short_description",
            "metacritic_score",
            "controller_support",
        ]

    @staticmethod
    def get_nullable_fields() -> List[str]:
        return ["metacritic_score"]
