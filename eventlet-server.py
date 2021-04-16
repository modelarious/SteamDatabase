from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server
from State.StateTracker import StateTracker

if __name__ == '__main__':
    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

    observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
    stateTracker = StateTracker(observerSocketHookupFactory)

    from time import sleep
    stateTracker.setUpcomingState('factorio')
    sleep(1)
    stateTracker.setUpcomingState('satisfactory')
    sleep(3)
    stateTracker.setFindingNameActiveState('factorio')
    sleep(3)
    stateTracker.setFindingNameActiveState('satisfactory')
    
    
    print("waiting on server")
    server.join()
