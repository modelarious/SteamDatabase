from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from State.States import *
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory


class StateTracker:
    def __init__(self, websocketRegistry : WebsocketClientHandlerRegistry):
        print("STATETRACKER - waiting on sockets")
        websocketRegistry.waitForAllSocketsReady()
        print("STATETRACKER - all needed sockets have been connected")

        # creating observable data structures
        factoryMethod = ObserverSocketHookupFactory(websocketRegistry).hookUpObservableDataStructure

        self.upcoming  = factoryMethod(UPCOMING_STATE)
        self.findingNameActive = factoryMethod(FINDING_NAME_ACTIVE_STATE)

    def setUpcomingState(self, gameTitle : str):
        self.upcoming.add(gameTitle)
    
    def setFindingNameActiveState(self, gameTitle : str):
        self.upcoming.remove(gameTitle)
        self.findingNameActive.add(gameTitle)