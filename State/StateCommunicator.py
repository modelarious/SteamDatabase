from dataclasses import dataclass
from Server.WebsocketClientHandlerRegistry import GAMES
from QueueEntries.Sendable import Sendable, ErrorSendable
from State.States import *
from State.StateCommunicatorInterface import StateCommunicatorInterface

# type hints
from typing import Dict
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from ObservedDataStructure.ObservedDataStructure import ObservedDataStructure
from GameModel import Game
from typing import List

@dataclass
class InternalStateTracker:
    def __init__(self):
        self.previousStateTracker = {}

    def track(self, sendable: Sendable, state: ObservedDataStructure):
        game_on_disk = sendable.get_game_name_on_disk()
        self.previousStateTracker[game_on_disk] = state
    
    def remove(self, sendable: Sendable):
        game_on_disk = sendable.get_game_name_on_disk()
        del self.previousStateTracker[game_on_disk]
    
    def get(self, sendable: Sendable) -> ObservedDataStructure:
        game_on_disk = sendable.get_game_name_on_disk()
        return self.previousStateTracker[game_on_disk]


# XXX This was only made to handle the case where you have unique games - if you have duplicates then this
# XXX will break. This is because the observedDataStructure is powered by a data structure
# that assumes the titles are unique within a batch
class StateCommunicator(StateCommunicatorInterface):
    def __init__(self, observedDataStructures : Dict[StateStrType, ObservedDataStructure], games_observable_data_structure: ObservedDataStructure):
        # doing this with helpful names so accesses in member functions are easy to read
        self.upcoming  = observedDataStructures[UPCOMING_STATE]
        self.findingNameActive = observedDataStructures[FINDING_NAME_ACTIVE_STATE]
        self.awaitingUser = observedDataStructures[AWAITING_USER_STATE]
        self.queuedForInfoRetrieval = observedDataStructures[QUEUED_FOR_INFO_RETRIEVAL_STATE]
        self.infoRetrievalActive = observedDataStructures[INFO_RETRIEVAL_ACTIVE_STATE]
        self.stored = observedDataStructures[STORED]
        self.errorState = observedDataStructures[ERROR_STATE]
        self.games = games_observable_data_structure
        self.internalStateTracker = InternalStateTracker() # XXX DI

    def batchSetUpcomingState(self, game_titles_on_disk : List[str]):
        sendables = [Sendable(game_name_on_disk=title) for title in game_titles_on_disk]
        self.upcoming.batch_add(sendables)
        for sendable in sendables:
            self.internalStateTracker.track(sendable, self.upcoming)
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        sendable = Sendable(gameTitleOnDisk)
        self.upcoming.remove(sendable)
        self.findingNameActive.add(sendable)
        self.internalStateTracker.track(sendable, self.findingNameActive)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        self.findingNameActive.remove(userInputRequiredQueueEntry)
        self.awaitingUser.add(userInputRequiredQueueEntry)
        self.internalStateTracker.track(userInputRequiredQueueEntry, self.awaitingUser)
    
    
    # Could have been a 100% name match in which case, previous state was FindingNameActiveState.
    # Also could have been only a partial match to a few names and the user had to select
    # the correct one, so the previous state was AwaitingUserInputState.
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        self.findingNameActive.remove(matchQueueEntry)
        self.queuedForInfoRetrieval.add(matchQueueEntry)
        self.internalStateTracker.track(matchQueueEntry, self.queuedForInfoRetrieval)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        self.awaitingUser.remove(matchQueueEntry)
        self.queuedForInfoRetrieval.add(matchQueueEntry)
        self.internalStateTracker.track(matchQueueEntry, self.queuedForInfoRetrieval)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        self.queuedForInfoRetrieval.remove(matchQueueEntry)
        self.infoRetrievalActive.add(matchQueueEntry)
        self.internalStateTracker.track(matchQueueEntry, self.infoRetrievalActive)
    
    def setStoredState(self, game : Game):
        self.infoRetrievalActive.remove(game)
        self.stored.add(game)
        self.games.add(game)
        self.internalStateTracker.remove(game)
    
    def transitionToErrorState(self, errorSendable: ErrorSendable):
        self.errorState.add(errorSendable)
        previousState = self.internalStateTracker.get(errorSendable)
        previousState.remove(errorSendable)
        self.internalStateTracker.remove(errorSendable)
