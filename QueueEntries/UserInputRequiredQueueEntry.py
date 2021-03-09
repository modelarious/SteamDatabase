class UserInputRequiredQueueEntry:
    def __init__(self, targetName, possibleMatchesList):
        self.targetName = targetName
        self.possibleMatchesList = possibleMatchesList
    
    def getTargetName(self):
        return self.targetName
    
    def getPossibleMatchesList(self):
        return self.possibleMatchesList