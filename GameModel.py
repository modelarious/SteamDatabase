from ExternalDataFetchers.AppDetail import AppDetail

class Game:
    def __init__(self, steam_id, name_on_harddrive, path_on_harddrive, name_on_steam, avg_review_score, user_defined_genres, app_detail : AppDetail):
        self.steam_id = steam_id
        self.name_on_harddrive = name_on_harddrive
        self.path_on_harddrive = path_on_harddrive
        self.name_on_steam = name_on_steam
        self.avg_review_score = avg_review_score
        self.user_defined_genres = user_defined_genres
        self.app_detail = app_detail
    
    def toDict(self):
        return self.__dict__.copy()

    
