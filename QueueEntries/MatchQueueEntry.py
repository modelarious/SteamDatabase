from dataclasses import dataclass

@dataclass
class MatchQueueEntry:
    gameNameFromSteam: str
    gameNameOnDisk: str
    steamIDNumber: int

    def getGameNameFromSteam(self):
        return self.gameNameFromSteam
    
    def getGameNameOnDisk(self):
        return self.gameNameOnDisk

    def getSteamIDNumber(self):
        return self.steamIDNumber
    
    def to_dict(self):
        return self.__dict__.copy()