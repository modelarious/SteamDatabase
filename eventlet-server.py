from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from Server.Server import Server

from State.StateTrackerFactory import StateTrackerFactory
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory
from State.StateTracker import StateTracker

if __name__ == '__main__':
    websocketRegistry = WebsocketClientHandlerRegistry()
    server = Server(websocketRegistry)
    server.startInThread()

    print("waiting on sockets")
    websocketRegistry.waitForAllSocketsReady()
    print("all needed sockets have been connected")

    # now that we are guaranteed that the sockets are connected, we can use them
    observerSocketHookupFactory = ObserverSocketHookupFactory(websocketRegistry)
    stateTrackerFactory = StateTrackerFactory()
    stateTracker = stateTrackerFactory.createStateTracker(observerSocketHookupFactory)

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
