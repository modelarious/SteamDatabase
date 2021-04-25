from State.States import *
from State.StateCommunicatorInterface import StateCommunicatorInterface

# type hints
from typing import Dict
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from State.ObservedDataStructure import ObservedDataStructure
from GameModel import Game

# XXX concurrency, which should be handled in ObservedDataStructure

# XXX This was only made to handle the case where you have unique games - if you have duplicates then this
# XXX will break
class StateCommunicator(StateCommunicatorInterface):
    def __init__(self, connections : Dict[StateStrType, ObservedDataStructure]):

        self.previousState = {}

        # doing this with helpful names so accesses in member functions are easy to read
        self.upcoming  = connections[UPCOMING_STATE]
        self.findingNameActive = connections[FINDING_NAME_ACTIVE_STATE]
        self.awaitingUser = connections[AWAITING_USER_STATE]
        self.queuedForInfoRetrieval = connections[QUEUED_FOR_INFO_RETRIEVAL_STATE]
        self.infoRetrievalActive = connections[INFO_RETRIEVAL_ACTIVE_STATE]
        self.stored = connections[STORED]

    def setUpcomingState(self, gameTitleOnDisk : str):
        self.upcoming.add(gameTitleOnDisk)
        self._trackCurrentState(self.upcoming, gameTitleOnDisk)
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.upcoming.remove(gameTitleOnDisk)
        self.findingNameActive.add(gameTitleOnDisk)
        self._trackCurrentState(self.findingNameActive, gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        gameTitleOnDisk = userInputRequiredQueueEntry.getGameName()
        self.findingNameActive.remove(gameTitleOnDisk)
        self.awaitingUser.add(userInputRequiredQueueEntry.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.awaitingUser, gameTitleOnDisk)
    
    def rejectedByUser(self, gameTitle: str):
        self.awaitingUser.remove(gameTitle)
    
    def setQueuedForInfoRetrievalState(self, matchQueueEntry : MatchQueueEntry):
        if not isinstance(matchQueueEntry, MatchQueueEntry):
            raise Exception("WTF")
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()

        # Could have been a 100% name match in which case, previous state was FindingNameActiveState.
        # Also could have been only a partial match to a few names and the user had to select
        # the correct one, so the previous state was AwaitingUserInputState.
        prevState = self._getPreviousState(gameTitleOnDisk)
        prevState.remove(gameTitleOnDisk)

        self.queuedForInfoRetrieval.add(matchQueueEntry.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.queuedForInfoRetrieval, gameTitleOnDisk)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()
        self.queuedForInfoRetrieval.remove(gameTitleOnDisk)

        self.infoRetrievalActive.add(matchQueueEntry.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.infoRetrievalActive, gameTitleOnDisk)
    
    def setStoredState(self, game : Game):
        gameTitleOnDisk = game.name_on_harddrive
        self.infoRetrievalActive.remove(gameTitleOnDisk)
        self.stored.add(game.toDict(), gameTitleOnDisk)
        self._trackCurrentState(self.stored, gameTitleOnDisk)
    
    def _trackCurrentState(self, state: ObservedDataStructure, gameTitleOnDisk: str):
        self.previousState[gameTitleOnDisk] = state
        
    def _getPreviousState(self, gameTitleOnDisk: str):
        return self.previousState[gameTitleOnDisk]

    