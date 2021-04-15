from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from InternalDataFetchers.DirListFetcher import DirListFetcher
from ExternalDataFetchers.SteamGameListFetcher import SteamGameListFetcher

def cli(pathToGamesFolder: str):

    steamGameListFetcher = SteamGameListFetcher()
    steamGamesList = steamGameListFetcher.fetch_games_list()

    dirListFetcher = DirListFetcher()
    gamesOnDisk = dirListFetcher.get_dirs(pathToGamesFolder)

    if gamesOnDisk == False:
        exit(f'no directories found at path {pathToGamesFolder}')

    match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk)


cli("/tmp/games")