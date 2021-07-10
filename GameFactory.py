from ExternalDataFetchers.AppDetail import AppDetailFactory
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from ExternalDataFetchers.UserDefinedGenresFetcher import UserDefinedGenresFetcher
from ExternalDataFetchers.SteamAPIDataFetcher import SteamAPIDataFetcher
from GameModel import Game

class FailedToGetAppDetailsException(Exception):
    pass

class GameFactory:
    def __init__(self, path_on_disk: str):
        self.user_defined_genres_fetcher = UserDefinedGenresFetcher()
        app_detail_factory = AppDetailFactory()
        self.steam_api_data_fetcher = SteamAPIDataFetcher(app_detail_factory)
        self.path_on_disk = path_on_disk

    def create(self, queue_entry: MatchQueueEntry):
        game_name_on_disk = queue_entry.get_game_name_on_disk()
        steam_id_number = queue_entry.get_steam_id_number()

        user_genres = self.user_defined_genres_fetcher.getGenres(steam_id_number)
        review_score = self.steam_api_data_fetcher.getAvgReviewScore(steam_id_number) # XXX PUT REVIEW SCORE IN APP DETAIL
        app_detail = self.steam_api_data_fetcher.get_app_detail(steam_id_number)

        if not app_detail:
            raise FailedToGetAppDetailsException(f'failed get_app_detail for {steam_id_number}, {queue_entry}')
        
        game = Game(
            steam_id=steam_id_number, 
            game_name_on_disk=game_name_on_disk,
            path_on_harddrive=self.path_on_disk, 
            game_name_from_steam=queue_entry.get_game_name_from_steam(), 
            avg_review_score=review_score,
            user_defined_genres=user_genres,
            app_detail=app_detail
        )

        return game
