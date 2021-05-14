from State.StateCommunicatorInterface import StateCommunicatorInterface
import inspect
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from GameModel import Game
from typing import Any

class DummyStateCommunicator(StateCommunicatorInterface):
    def show(self, payload: Any):
        funcName = self._determine_function_name()
        print(f"[{funcName}] - {payload}")

    def setUpcomingState(self, gameTitleOnDisk : str):
        self.show(gameTitleOnDisk)
  
    def setFindingNameActiveState(self, gameTitleOnDisk : str):
        self.show(gameTitleOnDisk)
    
    def setAwaitingUserInputState(self, userInputRequiredQueueEntry : UserInputRequiredQueueEntry):
        self.show(userInputRequiredQueueEntry)
    
    def rejectedByUser(self, userInputRequiredQueueEntry: UserInputRequiredQueueEntry):
        self.show(userInputRequiredQueueEntry)
    
    def setQueuedForInfoRetrievalStateFromFindingNameActive(self, matchQueueEntry : MatchQueueEntry):
        self.show(matchQueueEntry)

    def setQueuedForInfoRetrievalStateFromAwaitingUser(self, matchQueueEntry : MatchQueueEntry):
        self.show(matchQueueEntry)
    
    def setInfoRetrievalActiveState(self, matchQueueEntry : MatchQueueEntry):
        self.show(matchQueueEntry)
    
    def setStoredState(self, game : Game):
        self.show(game)
    
    def _determine_function_name(self):
        return inspect.stack()[2][3]
    