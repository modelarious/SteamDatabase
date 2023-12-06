from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from ObservedDataStructure.ObserverSocketHookupFactory import (
    ObserverSocketHookupFactory,
)

from multiprocessing import Manager

from Helpers.SteamDatabase import match_steam_games_to_games_on_disk_and_store
from ExternalDataFetchers.SteamGameListFetcherMOCKDATA import (
    SteamGameListFetcherMOCKDATA,
)
from InternalDataFetchers.DirListFetcherMOCKDATA import DirListFetcherMOCKDATA

from State.StateCommunicatorQueues import (
    StateCommunicationQueueWriter,
    StateCommunicationQueueReader,
)


m = Manager()
# XXX this is going to have to change, because you'll
# need one for each function in the StateCommunicationInterface
# which will get out of hand!
# consider a "StateCommunicatorQueueContainerFactor" which takes an instance of the manager and creates a
# queue for each function of a StateCommunicatorInterface, storing them in a StateCommunicatorQueueContainer that can be passed around
upcomingQueue = m.Queue()
writer = StateCommunicationQueueWriter(upcomingQueue)

websocketRegistry = WebsocketClientHandlerRegistry()
server = Server(websocketRegistry)
server.startInThread()

print("waiting on sockets")
websocketRegistry.waitForAllSocketsReady()
print("all needed sockets have been connected")

# now that we are guaranteed that the sockets are connected, we can use them
observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry, m)
stateCommunicatorFactory = StateCommunicatorFactory()
stateCommunicator = stateCommunicatorFactory.createStateCommunicator(
    observerSocketHookupFactory
)

# XXX this is shared with the cli - use abstract factory pattern to make mock data
# steamGameListFetcher = SteamGameListFetcherMOCKDATA()
# steamGamesList = steamGameListFetcher.fetch_games_list()

# dirListFetcher = DirListFetcherMOCKDATA()
# gamesOnDisk = dirListFetcher.get_dirs("")

reader = StateCommunicationQueueReader(stateCommunicator, upcomingQueue)
reader.start()
writer.setUpcomingState("hello world")

from time import sleep

sleep(4)


# XXX Are there duplicate steam titles in the list? The fast map might need to be changed!
# match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, stateCommunicator)

# XXX if you want the reader to join properly, you're going to have to tell the queues to shutdown
reader.join()

server.join()
m.join()
