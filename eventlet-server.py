from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateCommunicatorFactory import StateCommunicatorFactory
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from State.StateCommunicator import StateCommunicator

if __name__ == '__main__':
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

    from time import sleep
    stateCommunicator.setUpcomingState('factorio')
    sleep(1)
    stateCommunicator.setUpcomingState('satisfactory')
    sleep(3)
    stateCommunicator.setFindingNameActiveState('factorio')
    sleep(3)
    stateCommunicator.setFindingNameActiveState('satisfactory')
    
    
    print("waiting on server")
    server.join()
