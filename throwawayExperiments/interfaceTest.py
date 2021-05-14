from abc import ABC, abstractmethod

class StateCommunicatorInterface(ABC):
    @abstractmethod
    def setUpcomingState(self, gameTitleOnDisk):
        pass

    @abstractmethod
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        pass
    
    @abstractmethod
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry):
        pass
    
    @abstractmethod
    def rejectedByUser(self, userInputRequiredQueueEntry):
        pass
    
    @abstractmethod
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry):
        pass

    @abstractmethod
    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry):
        pass
    
    @abstractmethod
    def setInfoRetrievalActiveState(self, matchQueueEntry):
        pass
    
    @abstractmethod
    def setStoredState(self, game):
        pass

print(publicMethods)