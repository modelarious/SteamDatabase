from requests import get
from InternalDataFetchers.DirListFetcher import remove_non_approved_characters

class SteamGameListFetcher:
    def fetch_games_list(self):
        URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"

        requestReturn = get(url=URL)
        gamesObject = requestReturn.json()
        steamGamesList = gamesObject["applist"]["apps"]

        steamGamesList = [{'appid': 570, 'name': 'Dota ...'}]

        # steamGamesList is list of [{'appid': 570, 'name': 'Dota 2'}, {'appid': 730, 'name': 'Counter-Strike: Global Offensive'}, ...]
        # apply remove_non_approved_characters to the names, but keep the structure the same
        for game in steamGamesList:
            game["name"] = remove_non_approved_characters(game["name"])

        print(steamGamesList)

        

        return steamGamesList
