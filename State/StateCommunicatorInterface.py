from abc import ABC, abstractmethod
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game
from typing import List

class StateCommunicatorInterface(ABC):
    @abstractmethod
    def batchSetUpcomingState(self, gameTitlesOnDisk : List[str]):
        pass
    
    @abstractmethod
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        pass
    
    @abstractmethod
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        pass
    
    @abstractmethod
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        pass
    
    @abstractmethod
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        pass

    @abstractmethod
    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        pass
    
    @abstractmethod
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        pass
    
    @abstractmethod
    def setStoredState(self, game : Game):
        pass
