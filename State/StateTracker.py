from Server.WebsocketClientHandlerRegistry import WebsocketClientHandlerRegistry
from State.States import *
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory

from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry

# XXX concurrency
class StateTracker:
    def __init__(self, websocketRegistry : WebsocketClientHandlerRegistry):
        print("STATETRACKER - waiting on sockets")
        websocketRegistry.waitForAllSocketsReady()
        print("STATETRACKER - all needed sockets have been connected")

        # creating observable data structures
        factoryMethod = ObserverSocketHookupFactory(websocketRegistry).hookUpObservableDataStructure

        self.upcoming  = factoryMethod(UPCOMING_STATE)
        self.findingNameActive = factoryMethod(FINDING_NAME_ACTIVE_STATE)
        self.awaitingUser = factoryMethod(AWAITING_USER_STATE)

    def setUpcomingState(self, gameTitle : str):
        self.upcoming.add(gameTitle)
    
    def setFindingNameActiveState(self, gameTitle : str):
        self.upcoming.remove(gameTitle)
        self.findingNameActive.add(gameTitle)
    
    def setAwaitingUserInputState(self, userInputRequiredEntry : UserInputRequiredQueueEntry):
        gameTitle = userInputRequiredQueueEntry.getTargetName()
        self.findingNameActive.remove(gameTitle)
        self.awaitingUser.addByTag(gameTitle, userInputRequiredQueueEntry.toJson()) 
    



# awaiting an available process to start retrieving info
QUEUED_FOR_INFO_RETRIEVAL_STATE = '/queuedForInfoRetrieval'

# info about game is currently being collected - scraping steam page, hitting steam API
INFO_RETRIEVAL_ACTIVE_STATE = '/infoRetrievalActive'

# game has been persisted to database and will now show up on main screen
STORED = '/stored'

# states:
#  - upcoming
#  - finding name (active)
#  - awaiting user input
#  - queued for info retrieval
#  - info retrieval (active)
#  - stored
