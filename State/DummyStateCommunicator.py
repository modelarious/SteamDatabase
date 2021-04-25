from State.StateCommunicatorInterface import StateCommunicatorInterface
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game

class DummyStateCommunicator(StateCommunicatorInterface):
    def setUpcomingState(self, gameTitleOnDisk : str):
        pass
    
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        pass
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        pass
    
    def rejectedByUser(self, gameTitle: str):
        pass
    
    def setQueuedForInfoRetrievalState(self, matchQueueEntry : MatchQueueEntry):
        pass
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        pass
    
    def setStoredState(self, game : Game):
        pass
    