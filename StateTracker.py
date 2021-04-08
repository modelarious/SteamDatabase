from multiprocessing import Manager
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry

'''


Upcoming -> 


'''
# from abc import ABC
# class DataStructureInterface(ABC):
# def add(self, value):
# def remove(self, value):
# def get(self, association)

# class Array(DataStructureInterface):
# def add
# def remove
# def get xxxxxxxx

# class Dictionary(DataStructureInterface):
# def add
# def remove
# def get(key): return value

# Observer pattern but using socket instead of classic observers
class ObservedDataStructure:
    def __init__(self, socketToUpdate, initialInternalState=[]):
        self.socketToUpdate = socketToUpdate
        self.internalState = initialInternalState
        self._sendUpdate()
    
    def add(self, value):
        self.internalState.append(value)
        self._sendUpdate()

    def remove(self, value):
        self.internalState.remove(value)
        self._sendUpdate()
    
    def _sendUpdate(self):
        self.socketToUpdate.send_message(self.internalState)

class StateTracker:
    def __init__(self, websocketRegistry : WebsocketClientHandlerRegistry):
        self.websocketRegistry = websocketRegistry

        print("STATETRACKER - waiting on sockets")
        self.websocketRegistry.waitForAllSocketsReady()
        print("STATETRACKER - all needed sockets have been connected")

        # XXX factory
        upcomingSocket = self.websocketRegistry.get_socket('/upcoming')
        upcomingStateArray = []
        self.upcoming = ObservedDataStructure(upcomingSocket, upcomingStateArray)

        # XXX factory
        findingNameActiveSocket = self.websocketRegistry.get_socket('/findingNameActive')
        findingNameActiveStateArray = []
        self.findingNameActive = ObservedDataStructure(findingNameActiveSocket, findingNameActiveStateArray)

        # print("creating manager and queues")
        # m = Manager()
        # self.gameNameMatchesProcessingQueue = m.Queue()
        # self.userInputRequiredQueue = m.Queue()
        # print("created manager and queues")
    

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