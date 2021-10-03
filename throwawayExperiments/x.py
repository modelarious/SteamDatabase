# from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
# from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry



class MatchQueueEntry:
    def __init__(self, gameNameFromSteam, gameNameOnDisk, steamIDNumber):
        self.gameNameFromSteam = gameNameFromSteam
        self.gameNameOnDisk = gameNameOnDisk
        self.steamIDNumber = steamIDNumber

    def getGameNameFromSteam(self):
        return self.gameNameFromSteam
    
    def getGameNameOnDisk(self):
        return self.gameNameOnDisk

    def getSteamIDNumber(self):
        return self.steamIDNumber


from json import dumps
class UserInputRequiredQueueEntry:
    def __init__(self, gameName: str, possibleMatchesList):
        self.gameName = gameName
        self.possibleMatchesList = possibleMatchesList
    
    def getGameName(self):
        return self.gameName
    
    def getPossibleMatchesList(self):
        return self.possibleMatchesList
    
    def toJson(self):
        props = self.__dict__
        # need to apply __dict__ to sub objects in the possibleMatchesList
        props['possibleMatchesList'] = [x.__dict__ for x in self.possibleMatchesList]
    
        return dumps(props)



class PossibleMatchQueueEntry:
    def __init__(self, steamName: str, steamIDNumber: str, matchScore: float):
        self.steamName = steamName
        self.steamIDNumber = steamIDNumber
        self.matchScore = matchScore
    
    def getMatchScore(self) -> float:
        return self.matchScore
    
    def getSteamName(self) -> str:
        return self.steamName

    def convertToMatchQueueEntry(self, gameNameOnDisk: str):
        return MatchQueueEntry(self.steamName, gameNameOnDisk, self.steamIDNumber)
    


gameTitle = "Hello, I'm a game title"
possibleTitleMatch1 = "Hello, I'm a game title (tm)"
possibleTitleMatch2 = "Hello, I'm a game title 2"
possibleMatch1 = PossibleMatchQueueEntry(possibleTitleMatch1, "", 0.91)
possibleMatch2 = PossibleMatchQueueEntry(possibleTitleMatch2, "", 0.98)
possibleMatches = [
    possibleMatch1, 
    possibleMatch2
]
userInputRequiredQueueEntry = UserInputRequiredQueueEntry(gameTitle, possibleMatches)

print(userInputRequiredQueueEntry.toJson())