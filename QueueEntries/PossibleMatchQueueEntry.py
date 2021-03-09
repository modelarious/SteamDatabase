from QueueEntries.MatchQueueEntry import MatchQueueEntry
class PossibleMatchQueueEntry:
    def __init__(self, steamName, steamIDNumber, matchScore):
        self.steamName = steamName
        self.steamIDNumber = steamIDNumber
        self.matchScore = matchScore
    
    def getMatchScore(self):
        return self.matchScore
    
    def getSteamName(self):
        return self.steamName

    def convertToMatchQueueEntry(self, gameNameOnDisk):
        return MatchQueueEntry(self.steamName, gameNameOnDisk, self.steamIDNumber)