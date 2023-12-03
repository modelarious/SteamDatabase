from requests import get


class SteamGameListFetcher:
    def fetch_games_list(self):
        URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"

        requestReturn = get(url=URL)
        gamesObject = requestReturn.json()
        steamGamesList = gamesObject["applist"]["apps"]

        return steamGamesList
