from typing import Any, Dict
from Constants import END_OF_QUEUE
from Server.SocketWrapper import SocketWrapper
from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry, COMMAND
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.StateCommunicatorQueues import StateCommunicationQueueWriter, StateCommunicationQueueReader

from ObservedDataStructure.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from SteamDatabase import match_steam_games_to_games_on_disk_and_store

from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA

from multiprocessing import Manager


SHUTDOWN_COMMAND = "shutdown"
START_GAME_MATCH_COMMAND = "start game match"


COMMAND_NAME = 'command_name'
from abc import ABC, abstractmethod
class Command(ABC):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter):
        self.command_name = message[COMMAND_NAME]
        self.state_communicator = state_communicator

    @abstractmethod
    def execute(self):
        pass

    def get_command_name(self):
        return self.command_name

class StartGameMatchCommand(Command):
    def __init__(self, message: Dict[str, Any], state_communicator: StateCommunicationQueueWriter):
        super().__init__(message, state_communicator)
        self.path_on_disk = message['path_on_disk']
    
    def execute(self):
        print("IT WORKED!!")
        from time import sleep
        sleep(10)
        pass

class ShutdownCommand(Command):
    def execute(self):
        pass

class InvalidCommand(Exception):
    pass

class CommandFactory:
    def __init__(self, state_communicator: StateCommunicationQueueWriter):
        self.writer = state_communicator
        self.command_type_map = {
            START_GAME_MATCH_COMMAND : StartGameMatchCommand,
            SHUTDOWN_COMMAND: ShutdownCommand
        }
    
    def create(self, message: Dict[str, Any]):
        string_command = message[COMMAND_NAME]
        if string_command not in self.command_type_map:
            raise InvalidCommand(f"{string_command} not present in {self.command_type_map.keys()}")
        command_class = self.command_type_map[string_command]
        return command_class(message, self.writer)

class CommandDispatch:
    def __init__(self, command_socket: SocketWrapper, command_factory: CommandFactory):
        self.command_socket = command_socket
        self.command_factory = command_factory

    def command_loop(self):
        while True:
            message = self.command_socket.get_message()
            command = self.command_factory.create(message)

            if command.get_command_name() == SHUTDOWN_COMMAND:
                break

            # blocking
            command.execute()
        
if __name__ == '__main__':
    from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
    postgresGameDAOFactory = PostgresGameDAOFactory()
    gameDAO = postgresGameDAOFactory.createGameDAO()
    print(gameDAO.get_paths_of_all_stored_games())

    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

    command_socket = websocketRegistry.get_socket(COMMAND)
    # print("awaiting command")
    # print(command_socket.get_message())



    # now that we are guaranteed that the sockets are connected, we can use them
    observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
    stateCommunicatorFactory = StateCommunicatorFactory()
    stateCommunicator = stateCommunicatorFactory.createStateCommunicator(observerSocketHookupFactory)
    
    m = Manager()
    queue = m.Queue()
    writer = StateCommunicationQueueWriter(queue)
    reader = StateCommunicationQueueReader(stateCommunicator, queue)
    reader.start()

    # XXX this is shared with the cli - use abstract factory pattern to make mock data
    steamGameListFetcher = SteamGameListFetcherMOCKDATA()
    steamGamesList = steamGameListFetcher.fetch_games_list()

    dirListFetcher = DirListFetcherMOCKDATA()
    gamesOnDisk = dirListFetcher.get_dirs("")


    command_factory = CommandFactory(writer)
    command_dispatch = CommandDispatch(command_socket, command_factory)
    command_dispatch.command_loop()


    # XXX Are there duplicate steam titles in the list? The fast map might need to be changed!
    match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, writer)

    # XXX if you want this to join properly, you're going to have to tell the queues to shutdown
    reader.join()

    server.join()
    m.join()

        

