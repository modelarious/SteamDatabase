from requests import get


class SteamGameListFetcher:
    def fetch_games_list(self):
        URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
        gamesObject = get(url=URL).json()

        match gamesObject:
            case {"applist": {"apps": steamGamesList}}:
                return steamGamesList
            
            case _:
                raise Exception(f"Unknown response from Steam API: {gamesObject}")
