from State.States import *
from State.ObserverSocketHookupFactory import ObserverSocketHookupFactory

# type checking
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from State.ObservedDataStructure import ObservedDataStructure

# XXX concurrency
class StateTracker:
    def __init__(self, observerSocketHookupFactory : ObserverSocketHookupFactory):
        factoryMethod = observerSocketHookupFactory.hookUpObservableDataStructure

        self.previousState = {}

        # creating observable data structures with helpful names so accesses in member functions
        # are easy to read
        self.upcoming  = factoryMethod(UPCOMING_STATE)
        self.findingNameActive = factoryMethod(FINDING_NAME_ACTIVE_STATE)
        self.awaitingUser = factoryMethod(AWAITING_USER_STATE)
        self.queuedForInfoRetrieval = factoryMethod(QUEUED_FOR_INFO_RETRIEVAL_STATE)
        self.infoRetrievalActive = factoryMethod(INFO_RETRIEVAL_ACTIVE_STATE)
        self.stored = factoryMethod(STORED)

    def setUpcomingState(self, gameTitle : str):
        self.upcoming.add(gameTitle)
        self._trackCurrentState(self.upcoming, gameTitle)
    
    def setFindingNameActiveState(self, gameTitle : str):
        self.upcoming.remove(gameTitle)
        self.findingNameActive.add(gameTitle)
        self._trackCurrentState(self.findingNameActive, gameTitle)
    
    def setAwaitingUserInputState(self, userInputRequiredEntry : UserInputRequiredQueueEntry):
        gameTitle = userInputRequiredQueueEntry.getGameName()
        self.findingNameActive.remove(gameTitle)
        self.awaitingUser.addByTag(gameTitle, userInputRequiredQueueEntry.toJson())
        self._trackCurrentState(self.awaitingUser, gameTitle)
    
    # XXX this needs to remove the value from awaitingUser state
    def rejectedByUser(self):
        pass
    
    def setQueuedForInfoRetrievalState(self, matchQueueEntry : MatchQueueEntry):
        gameTitle = matchQueueEntry.getGameNameOnDisk()

        # Could have been a 100% name match in which case, previous state was FindingNameActiveState.
        # Also could have been only a partial match to a few names and the user had to select
        # the correct one, so the previous state was AwaitingUserInputState.
        prevState = self._getPreviousState(gameTitle)
        prevState.remove(gameTitle)

        self.queuedForInfoRetrieval.addByTag(gameTitle, matchQueueEntry.toJson())
        self._trackCurrentState(self.queuedForInfoRetrieval, gameTitle)
    
    def setInfoRetrievalActiveState(self):
        pass
    
    def setStoredState(self):
        pass
    
    def _trackCurrentState(self, state: ObservedDataStructure, gameTitle: str):
        self.previousState[gameTitle] = state
        
    def _wasPreviousState(self, gameTitle: str):
        return self.previousState[gameTitle]

    



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
