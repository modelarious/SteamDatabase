from State.States import *

# type hints
from typing import Dict
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from State.ObservedDataStructure import ObservedDataStructure

# XXX concurrency, which should be handled in ObservedDataStructure
class StateTracker:
    def __init__(self, connections : Dict[StateStrType, ObservedDataStructure]):

        self.previousState = {}

        # doing this with helpful names so accesses in member functions are easy to read
        self.upcoming  = connections[UPCOMING_STATE]
        self.findingNameActive = connections[FINDING_NAME_ACTIVE_STATE]
        self.awaitingUser = connections[AWAITING_USER_STATE]
        self.queuedForInfoRetrieval = connections[QUEUED_FOR_INFO_RETRIEVAL_STATE]
        self.infoRetrievalActive = connections[INFO_RETRIEVAL_ACTIVE_STATE]
        self.stored = connections[STORED]

    def setUpcomingState(self, gameTitle : str):
        self.upcoming.add(gameTitle)
        self._trackCurrentState(self.upcoming, gameTitle)
    
    def setFindingNameActiveState(self, gameTitle : str):
        self.upcoming.remove(gameTitle)
        self.findingNameActive.add(gameTitle)
        self._trackCurrentState(self.findingNameActive, gameTitle)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        gameTitle = userInputRequiredQueueEntry.getGameName()
        self.findingNameActive.remove(gameTitle)
        self.awaitingUser.add(userInputRequiredQueueEntry.toDict(), gameTitle)
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

        self.queuedForInfoRetrieval.add(matchQueueEntry.toDict(), gameTitle)
        self._trackCurrentState(self.queuedForInfoRetrieval, gameTitle)
    
    def setInfoRetrievalActiveState(self):
        pass
    
    def setStoredState(self):
        pass
    
    def _trackCurrentState(self, state: ObservedDataStructure, gameTitle: str):
        self.previousState[gameTitle] = state
        
    def _wasPreviousState(self, gameTitle: str):
        return self.previousState[gameTitle]

    