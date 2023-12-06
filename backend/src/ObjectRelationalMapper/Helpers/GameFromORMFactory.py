from ObjectRelationalMapper.ORMMappedObjects.ORMAppDetail import ORMAppDetail
from ObjectRelationalMapper.ORMMappedObjects.ORMGame import ORMGame
from ObjectRelationalMapper.ORMMappedObjects.ORMUserDefinedGenres import (
    ORMUserDefinedGenres,
)
from ObjectRelationalMapper.ORMMappedObjects.ORMScreenshotURLs import ORMScreenshotURLS
from ObjectRelationalMapper.ORMMappedObjects.ORMDevelopers import ORMDevelopers
from ObjectRelationalMapper.ORMMappedObjects.ORMPublishers import ORMPublishers
from ObjectRelationalMapper.ORMMappedObjects.ORMGenres import ORMGenres

from ObjectRelationalMapper.Helpers.PostgresSelectedValues import PostgresSelectedValues

from Game.GameModel import Game

# XXX this import should be a model import, not from some external data fetcher!
from ExternalDataFetchers.AppDetail import ScreenshotURL, AppDetail


class GameFromORMFactory:
    def _create_game(
        self, steam_id: int, query_storage: PostgresSelectedValues
    ) -> Game:
        game_data = query_storage.get_associated_data(ORMGame, steam_id)
        user_defined_genre_data = query_storage.get_associated_data(
            ORMUserDefinedGenres, steam_id
        )
        user_defined_genres = [
            user_defined_genre_orm.genre_name
            for user_defined_genre_orm in user_defined_genre_data
        ]

        app_detail_data = query_storage.get_associated_data(ORMAppDetail, steam_id)
        screenshot_data = query_storage.get_associated_data(ORMScreenshotURLS, steam_id)
        developer_data = query_storage.get_associated_data(ORMDevelopers, steam_id)
        publisher_data = query_storage.get_associated_data(ORMPublishers, steam_id)
        genre_data = query_storage.get_associated_data(
            ORMGenres, steam_id, default_value=[]
        )
        publishers = [orm_publisher.publisher for orm_publisher in publisher_data]
        developers = [orm_developer.developer for orm_developer in developer_data]
        genres = [orm_genre.genre for orm_genre in genre_data]
        screenshots = [
            ScreenshotURL(orm_screenshot.thumbnail_url, orm_screenshot.fullsize_url)
            for orm_screenshot in screenshot_data
        ]

        app_detail = AppDetail(
            detailed_description=app_detail_data.detailed_description,
            about_the_game=app_detail_data.about_the_game,
            short_description=app_detail_data.short_description,
            header_image_url=app_detail_data.header_image_url,
            publishers=publishers,
            developers=developers,
            metacritic_score=app_detail_data.metacritic_score,
            controller_support=app_detail_data.controller_support,
            genres=genres,
            screenshot_urls=screenshots,
            background_image_url=app_detail_data.background_image_url,
        )

        game_model = Game(
            steam_id=steam_id,
            game_name_on_disk=game_data.game_name_on_disk,
            path_on_harddrive=game_data.path_on_harddrive,
            game_name_from_steam=game_data.game_name_from_steam,
            avg_review_score=game_data.avg_review_score,
            user_defined_genres=user_defined_genres,
            app_detail=app_detail,
        )
        return game_model

    def create_games(self, query_storage: PostgresSelectedValues):
        all_games = []
        for steam_id in query_storage.get_steam_ids():
            game = self._create_game(steam_id, query_storage)
            all_games.append(game)
        return all_games
