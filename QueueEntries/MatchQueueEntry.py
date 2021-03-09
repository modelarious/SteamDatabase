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