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
    def __init__(self, observedDataStructures : Dict[StateStrType, ObservedDataStructure]):
        # doing this with helpful names so accesses in member functions are easy to read
        self.upcoming  = observedDataStructures[UPCOMING_STATE]
        self.findingNameActive = observedDataStructures[FINDING_NAME_ACTIVE_STATE]
        self.awaitingUser = observedDataStructures[AWAITING_USER_STATE]
        self.queuedForInfoRetrieval = observedDataStructures[QUEUED_FOR_INFO_RETRIEVAL_STATE]
        self.infoRetrievalActive = observedDataStructures[INFO_RETRIEVAL_ACTIVE_STATE]
        self.stored = observedDataStructures[STORED]

    def batchSetUpcomingState(self, gameTitlesOnDisk : List[str]):
        self.upcoming.batch_add(gameTitlesOnDisk)
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.upcoming.remove(gameTitleOnDisk)
        self.findingNameActive.add(gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        gameTitleOnDisk = userInputRequiredQueueEntry.get_game_name_on_disk()
        self.findingNameActive.remove(gameTitleOnDisk)
        self.awaitingUser.add(userInputRequiredQueueEntry.to_dict(), gameTitleOnDisk)
    
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        gameTitleOnDisk = userInputRequiredQueueEntry.get_game_name_on_disk()
        self.awaitingUser.remove(gameTitleOnDisk)
    
    # Could have been a 100% name match in which case, previous state was FindingNameActiveState.
    # Also could have been only a partial match to a few names and the user had to select
    # the correct one, so the previous state was AwaitingUserInputState.
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()
        self.findingNameActive.remove(gameTitleOnDisk)
        self.queuedForInfoRetrieval.add(matchQueueEntry.to_dict(), gameTitleOnDisk)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()
        self.awaitingUser.remove(gameTitleOnDisk)
        self.queuedForInfoRetrieval.add(matchQueueEntry.to_dict(), gameTitleOnDisk)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        gameTitleOnDisk = matchQueueEntry.getGameNameOnDisk()
        self.queuedForInfoRetrieval.remove(gameTitleOnDisk)
        self.infoRetrievalActive.add(matchQueueEntry.to_dict(), gameTitleOnDisk)
    
    def setStoredState(self, game : Game):
        gameTitleOnDisk = game.name_on_harddrive
        self.infoRetrievalActive.remove(gameTitleOnDisk)
        self.stored.add(game.to_dict(), gameTitleOnDisk)
    
    # def storageFailed(self, game: Game):
    #     gameTitleOnDisk = game.name_on_harddrive
    #     self.stored.remove(gameTitleOnDisk)
    #     self._trackCurrentState(None, gameTitleOnDisk)

    