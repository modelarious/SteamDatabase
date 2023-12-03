from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
from CommandDispatch.Commands.Command import Command
from typing import Dict, Any, Callable
from State.StateCommunicatorQueues import StateCommunicationQueueWriter
# from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from ExternalDataFetchers.SteamGameListFetcher import SteamGameListFetcher
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcher import DirListFetcher
from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from Server.SocketWrapper import SocketWrapper


class StartGameMatchCommand(Command):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter, input_socket_fetch_function: Callable[[], SocketWrapper]):
        super().__init__(message, state_communicator, input_socket_fetch_function)
        self.path_on_disk = message['path_on_disk']
    
    def execute(self):
        # XXX this is shared with the cli - use abstract factory pattern to make mock data
        steamGameListFetcher = SteamGameListFetcher()
        # steamGameListFetcher = SteamGameListFetcherMOCKDATA()
        steamGamesList = steamGameListFetcher.fetch_games_list()

        dirListFetcher = DirListFetcherMOCKDATA()
        game_titles_on_disk_mock = dirListFetcher.get_dirs(self.path_on_disk)
        dirListFetcher = DirListFetcher()
        game_titles_on_disk = dirListFetcher.get_files_and_dirs(self.path_on_disk)

        postgres_dao_factory = PostgresGameDAOFactory()
        postgres_dao = postgres_dao_factory.createGameDAO()
        game_titles_from_postgres = set(postgres_dao.get_titles_of_all_stored_games())

        filtered_game_titles = sorted(list(set( 
            game_title for game_title in game_titles_on_disk
                if game_title not in game_titles_from_postgres
        )))

        # XXX Are there duplicate steam titles in the list? The fast map might need to be changed!
        # Reason I'm concerned is that there are (for example) two steam ids for Majesty 2
        match_steam_games_to_games_on_disk_and_store(steamGamesList, filtered_game_titles, self.state_communicator, self.path_on_disk, self.input_socket_fetch_function)
