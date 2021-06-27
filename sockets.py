from CommandDispatch.CommandDispatchFactory import CommandDispatchFactory
from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.StateCommunicatorQueues import StateCommunicationQueueWriter, StateCommunicationQueueReader

from ObservedDataStructure.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from multiprocessing import Manager

if __name__ == '__main__':
    from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
    postgresGameDAOFactory = PostgresGameDAOFactory()
    gameDAO = postgresGameDAOFactory.createGameDAO()
    gameDAO.create_tables()
    gameDAO.get_all_games()

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
    
    m = Manager()
    queue = m.Queue()
    writer = StateCommunicationQueueWriter(queue)
    reader = StateCommunicationQueueReader(stateCommunicator, queue)
    reader.start()

    # command dispatch
    command_dispatch_factory = CommandDispatchFactory()
    command_dispatch = command_dispatch_factory.create(websocketRegistry, writer)
    command_dispatch.command_loop()

    # XXX if you want this to join properly, you're going to have to tell the queues to shutdown
    reader.join()

    server.join()
    m.join()


