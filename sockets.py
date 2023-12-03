from Constants import END_OF_QUEUE
from State.States import STATES
from CommandDispatch.CommandDispatchFactory import CommandDispatchFactory
from Server.WebsocketClientHandlerRegistry import GAMES, WebsocketClientHandlerRegistry
from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.StateCommunicatorQueues import (
    StateCommunicationQueueWriter,
    StateCommunicationQueueReader,
)

from ObservedDataStructure.ObserverSocketHookupFactory import (
    ObserverSocketHookupFactory,
)
from multiprocessing import Manager

if __name__ == "__main__":
    postgresGameDAOFactory = PostgresGameDAOFactory()
    gameDAO = postgresGameDAOFactory.createGameDAO()
    gameDAO.create_tables()

    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

    # now that we are guaranteed that the sockets are connected, we can use them.
    # next iteration of this would be having sockets that can be disconnected (and the messages get queued) and then reconnected and it will send all the queued messages along
    # the next iteration after that (assuming we are still sending full state and haven't moved to sending only the parts of state that have updated) would be to only send the most recent queued message
    observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
    games_observable_data_structure = (
        observerSocketHookupFactory.hookUpObservableDataStructure(GAMES)
    )
    games_observable_data_structure.batch_add(gameDAO.get_all_games())
    stateCommunicatorFactory = StateCommunicatorFactory()
    stateCommunicator = stateCommunicatorFactory.createStateCommunicator(
        observerSocketHookupFactory, STATES, games_observable_data_structure
    )

    m = Manager()
    queue = m.Queue()
    writer = StateCommunicationQueueWriter(queue)
    reader = StateCommunicationQueueReader(stateCommunicator, queue)
    reader.start()

    # command dispatch
    command_dispatch_factory = CommandDispatchFactory()
    command_dispatch = command_dispatch_factory.create(websocketRegistry, writer)
    command_dispatch.command_loop()

    # tell the queue to shutdown after it finishes current tasks
    queue.put(END_OF_QUEUE)
    reader.join()

    # XXX Still need to figure out how to make the server join properly
    server.join()
