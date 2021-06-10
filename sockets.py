from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry, COMMAND
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.StateCommunicatorQueues import StateCommunicationQueueWriter, StateCommunicationQueueReader

from ObservedDataStructure.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from SteamDatabase import match_steam_games_to_games_on_disk_and_store

from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA

from multiprocessing import Manager

if __name__ == '__main__':
    from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
    postgresGameDAOFactory = PostgresGameDAOFactory()
    gameDAO = postgresGameDAOFactory.createGameDAO()
    print(gameDAO.get_paths_of_all_stored_games())

    m = Manager()

    queue = m.Queue()
    writer = StateCommunicationQueueWriter(queue)

    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

    command_socket = websocketRegistry.get_socket(COMMAND)
    print("awaiting command")
    print(command_socket.get_message())

    # now that we are guaranteed that the sockets are connected, we can use them
    observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
    stateCommunicatorFactory = StateCommunicatorFactory()
    stateCommunicator = stateCommunicatorFactory.createStateCommunicator(observerSocketHookupFactory)
    
    # XXX this is shared with the cli - use abstract factory pattern to make mock data
    steamGameListFetcher = SteamGameListFetcherMOCKDATA()
    steamGamesList = steamGameListFetcher.fetch_games_list()

    dirListFetcher = DirListFetcherMOCKDATA()
    gamesOnDisk = dirListFetcher.get_dirs("")

    reader = StateCommunicationQueueReader(stateCommunicator, queue)
    reader.start()

    # XXX Are there duplicate steam titles in the list? The fast map might need to be changed!
    match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, writer)

    # XXX if you want this to join properly, you're going to have to tell the queues to shutdown
    reader.join()

    server.join()
    m.join()




