from typing import List
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry

class UserInputRequiredQueueEntry:
    def __init__(self, gameName, possibleMatchesList: List[PossibleMatchQueueEntry]):
        self.gameName = gameName
        self.possibleMatchesList = possibleMatchesList
    
    def getGameName(self):
        return self.gameName
    
    def getPossibleMatchesList(self):
        return self.possibleMatchesList