from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory

from multiprocessing import Manager

from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA

if __name__ == '__main__':
    m = Manager()

    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

    # now that we are guaranteed that the sockets are connected, we can use them
    observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry, m)
    stateCommunicatorFactory = StateCommunicatorFactory()
    stateCommunicator = stateCommunicatorFactory.createStateCommunicator(observerSocketHookupFactory)
    
    # XXX this is shared with the cli - use abstract factory pattern to make mock data
    steamGameListFetcher = SteamGameListFetcherMOCKDATA()
    steamGamesList = steamGameListFetcher.fetch_games_list()

    dirListFetcher = DirListFetcherMOCKDATA()
    gamesOnDisk = dirListFetcher.get_dirs("")

    # XXX it's terrible that you are passing this "lock" through the code and having to acquire it manually
    # when you want to access the serverProxyObject. This is bad for two reasons:
    # - you can easily forget to acquire the lock before accessing the object, it should instead happen 
    #     for you in the background
    # - it's a single lock for the entire serverProxyObject. As far as I know, the serverProxyObject doesn't
    #     need a lock, you actually need individual locks for the dictionaries inside of 
    #     ObservedDataStructure instances.  Ideally, you don't have to use ShareObjectBetweenProcesses at
    #     all

    # XXX Are there duplicate steam titles in the list? The fast map might need to be updated!
    match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, stateCommunicator)

    
    server.join()
    m.join()

