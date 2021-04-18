from QueueEntries.MatchQueueEntry import MatchQueueEntry
class PossibleMatchQueueEntry:
    def __init__(self, steamName: str, steamIDNumber: str, matchScore: float):
        self.steamName = steamName
        self.steamIDNumber = steamIDNumber
        self.matchScore = matchScore
    
    def getMatchScore(self) -> float:
        return self.matchScore
    
    def getSteamName(self) -> str:
        return self.steamName

    def convertToMatchQueueEntry(self, gameNameOnDisk: str) -> MatchQueueEntry:
        return MatchQueueEntry(self.steamName, gameNameOnDisk, self.steamIDNumber)

