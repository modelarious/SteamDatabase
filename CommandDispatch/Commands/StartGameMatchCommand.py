from CommandDispatch.Commands.Command import Command
from typing import Dict, Any
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA
from SteamDatabase import match_steam_games_to_games_on_disk_and_store


class StartGameMatchCommand(Command):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter):
        super().__init__(message, state_communicator)
        self.path_on_disk = message['path_on_disk']
    
    def execute(self):
        # XXX this is shared with the cli - use abstract factory pattern to make mock data
        steamGameListFetcher = SteamGameListFetcherMOCKDATA()
        steamGamesList = steamGameListFetcher.fetch_games_list()

        dirListFetcher = DirListFetcherMOCKDATA()
        gamesOnDisk = dirListFetcher.get_dirs(self.path_on_disk)

        # XXX Are there duplicate steam titles in the list? The fast map might need to be changed!
        match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, self.state_communicator)
