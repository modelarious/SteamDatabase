from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
from CommandDispatch.Commands.Command import Command
from typing import Dict, Any
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA
from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from os import sep

class StartGameMatchCommand(Command):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter):
        super().__init__(message, state_communicator)
        self.path_on_disk = message['path_on_disk']
    
    def execute(self):
        # XXX this is shared with the cli - use abstract factory pattern to make mock data
        steamGameListFetcher = SteamGameListFetcherMOCKDATA()
        steamGamesList = steamGameListFetcher.fetch_games_list()

        dirListFetcher = DirListFetcherMOCKDATA()
        games_titles_on_disk = dirListFetcher.get_dirs(self.path_on_disk)

        postgres_dao_factory = PostgresGameDAOFactory()
        postgres_dao = postgres_dao_factory.createGameDAO()
        game_paths_from_postgres = set(postgres_dao.get_paths_of_all_stored_games())

        filtered_game_titles = [ 
            game_title for game_title in games_titles_on_disk
                if self.path_on_disk + sep + game_title not in game_paths_from_postgres
        ]

        for game_title in games_titles_on_disk:
            file_path = self.path_on_disk + sep + game_title
            print(file_path)
            if file_path not in game_paths_from_postgres:
                print("added")

        # XXX Are there duplicate steam titles in the list? The fast map might need to be changed!
        # Reason I'm concerned is that there are (for example) two steam ids for Majesty 2
        match_steam_games_to_games_on_disk_and_store(steamGamesList, filtered_game_titles, self.state_communicator)
