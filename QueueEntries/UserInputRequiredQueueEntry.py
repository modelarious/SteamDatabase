from typing import List
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry

class UserInputRequiredQueueEntry:
    def __init__(self, gameName: str, possibleMatchesList: List[PossibleMatchQueueEntry]):
        self.gameName = gameName
        self.possibleMatchesList = possibleMatchesList
    
    def getGameName(self):
        return self.gameName
    
    def getPossibleMatchesList(self):
        return self.possibleMatchesList
    
    def toDict(self):
        props = self.__dict__
        # need to apply __dict__ to sub objects in the possibleMatchesList
        props['possibleMatchesList'] = [x.__dict__ for x in self.possibleMatchesList]
    
        return props
