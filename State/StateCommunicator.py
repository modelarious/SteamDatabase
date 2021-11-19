from Server.WebsocketClientHandlerRegistry import GAMES
from QueueEntries.Sendable import Sendable
from State.States import *
from State.StateCommunicatorInterface import StateCommunicatorInterface

# type hints
from typing import Dict
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from ObservedDataStructure.ObservedDataStructure import ObservedDataStructure
from GameModel import Game
from typing import List

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
        self.games = games_observable_data_structure

    def batchSetUpcomingState(self, game_titles_on_disk : List[str]):
        sendables = [Sendable(game_name_on_disk=title) for title in game_titles_on_disk]
        self.upcoming.batch_add(sendables)
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.upcoming.remove(Sendable(gameTitleOnDisk))
        self.findingNameActive.add(Sendable(gameTitleOnDisk))
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        self.findingNameActive.remove(userInputRequiredQueueEntry)
        self.awaitingUser.add(userInputRequiredQueueEntry)
    
    # XXX YYY XXX YYY should go back to old implementation - DO NOT COMMIT THIS PART OF THE CHANGE
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        self.findingNameActive.remove(userInputRequiredQueueEntry)
    
    # Could have been a 100% name match in which case, previous state was FindingNameActiveState.
    # Also could have been only a partial match to a few names and the user had to select
    # the correct one, so the previous state was AwaitingUserInputState.
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        self.findingNameActive.remove(matchQueueEntry)
        self.queuedForInfoRetrieval.add(matchQueueEntry)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        self.awaitingUser.remove(matchQueueEntry)
        self.queuedForInfoRetrieval.add(matchQueueEntry)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        self.queuedForInfoRetrieval.remove(matchQueueEntry)
        self.infoRetrievalActive.add(matchQueueEntry)
    
    def setStoredState(self, game : Game):
        self.infoRetrievalActive.remove(game)
        self.stored.add(game)
        self.games.add(game)
    
    # def storageFailed(self, game: Game):
    #     gameTitleOnDisk = game.game_name_on_disk
    #     self.stored.remove(gameTitleOnDisk)
    #     self._trackCurrentState(None, gameTitleOnDisk)

    