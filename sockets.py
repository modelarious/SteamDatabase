from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from ObservedDataStructure.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from State.DummyStateCommunicator import DummyStateCommunicator


from State.StateCommunicatorInterface import StateCommunicatorInterface

from multiprocessing import Manager

from SteamDatabase import match_steam_games_to_games_on_disk_and_store
from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import SteamGameListFetcherMOCKDATA
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA

from State.StateCommunicatorQueues import StateCommunicationQueueWriter, StateCommunicationQueueReader

class StateCommunicatorQueueContainerFactory:
    def __init__(self, managerInstance: Manager):
        self.manager = managerInstance
        self.queues = {}
    
    def create(self):
        self.queues = {}
        stateCommunicatorPublicMethods = [methodName for methodName in dir(StateCommunicatorInterface) if not methodName.startswith('_')]
        for methodName in stateCommunicatorPublicMethods:
            # XXX need to be joined or terminated in some way
            self.queues[methodName] = self.manager.Queue()
        return self.queues

def hit_dat_upcoming_state(writer, textToWrite):
    writer.setUpcomingState(textToWrite)

if __name__ == '__main__':
    m = Manager()

    queue = m.Queue()
    writer = StateCommunicationQueueWriter(queue)

    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

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




