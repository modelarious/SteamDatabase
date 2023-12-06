from typing import Dict, List
from Game.GameModel import Game
from dataclasses import dataclass
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase


@dataclass
class ORMScreenshotURLS(ORMAbstractBase):
    steam_id: int
    thumbnail_url: str
    fullsize_url: str

    @staticmethod
    def get_table_name() -> str:
        return "ScreenshotURLs"

    @staticmethod
    def get_insertion_data(game_model: Game) -> tuple:
        screenshot_urls = game_model.app_detail.screenshot_urls
        screenshot_url_data = tuple(
            (
                game_model.steam_id,
                screenshot_url.thumbnail_url,
                screenshot_url.fullsize_url,
            )
            for screenshot_url in screenshot_urls
        )
        return screenshot_url_data

    @staticmethod
    def needs_multiple_statements() -> bool:
        return True

    @staticmethod
    def get_foreign_key_mappings() -> Dict[str, str]:
        return {"steam_id": "Games"}

    @staticmethod
    def get_non_unique_mappings() -> List[str]:
        return ["steam_id"]
