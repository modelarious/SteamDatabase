from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from InternalDataFetchers.DirListFetcher import DirListFetcher
from ExternalDataFetchers.SteamGameListFetcher import SteamGameListFetcher

from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import (
    SteamGameListFetcherMOCKDATA,
)
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA
from State.DummyStateCommunicator import DummyStateCommunicator

import argh


@argh.arg("pathToGamesFolder", help="Path to the directory where your games are stored")
def cli(pathToGamesFolder: str):
    dummyStateCommunicator = DummyStateCommunicator()

    # steamGameListFetcher = SteamGameListFetcher()
    steamGameListFetcher = SteamGameListFetcherMOCKDATA()
    steamGamesList = steamGameListFetcher.fetch_games_list()

    # dirListFetcher = DirListFetcher()
    dirListFetcher = DirListFetcherMOCKDATA()
    gamesOnDisk = dirListFetcher.get_dirs(pathToGamesFolder)

    if gamesOnDisk == False:
        exit(f"no directories found at path {pathToGamesFolder}")

    match_steam_games_to_games_on_disk_and_store(
        steamGamesList, gamesOnDisk, dummyStateCommunicator, pathToGamesFolder
    )


if __name__ == "__main__":
    argh.dispatch_command(cli)
