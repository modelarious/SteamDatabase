from multiprocessing import Manager
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from State.States import *

# Observer pattern, but sending updates over a socket
class ObservedDataStructure:
    def sendUpdateDecorator(func):
        # updates socket after performing an action
        def update_sock(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.socketToUpdate.send_message(self.set)
        return update_sock

    @sendUpdateDecorator
    def __init__(self, socketToUpdate):
        self.socketToUpdate = socketToUpdate
        self.set = set()
    
    @sendUpdateDecorator
    def add(self, value):
        self.set.add(value)

    @sendUpdateDecorator
    def remove(self, value):
        self.set.remove(value)


class ObserverSocketHookupFactory:
    def __init__(self, websocketRegistry):
        self.websocketRegistry = websocketRegistry

    def hookUpObservableDataStructure(self, socketName):
        socket = self.websocketRegistry.get_socket(socketName)
        return ObservedDataStructure(socket)

class StateTracker:
    def __init__(self, websocketRegistry : WebsocketClientHandlerRegistry):
        # self.websocketRegistry = websocketRegistry

        print("STATETRACKER - waiting on sockets")
        websocketRegistry.waitForAllSocketsReady()
        print("STATETRACKER - all needed sockets have been connected")

        # creating observable data structures
        factory = ObserverSocketHookupFactory(websocketRegistry).hookUpObservableDataStructure

        self.upcoming  = factory(UPCOMING_STATE)
        self.findingNameActive = factory(FINDING_NAME_ACTIVE_STATE)

    def setUpcomingState(self, gameTitle : str):
        self.upcoming.add(gameTitle)
    
    def setFindingNameActiveState(self, gameTitle : str):
        self.upcoming.remove(gameTitle)
        self.findingNameActive.add(gameTitle)

# states:
#  - upcoming
#  - finding name (active)
#  - awaiting user input
#  - queued for info retrieval
#  - info retrieval (active)
#  - stored