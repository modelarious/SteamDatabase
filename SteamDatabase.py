from difflib import SequenceMatcher

# minimum edit distance algo with support for junk detection
def similarity(a, b):
    return SequenceMatcher(a=a, b=b).ratio()




from UserDefinedTagsFetcher import UserDefinedTagsFetcher
import pickle

#---------------------------------------------------------------------------------------
# https://store.steampowered.com/appreviews/2028850?json=1
# https://store.steampowered.com/api/appdetails?appids=2028850
# from pprint import pprint
# import requests

# URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"

# requestReturn = requests.get(url = URL) 
# gamesObject = requestReturn.json()
# steamGamesList = gamesObject["applist"]["apps"]



# with open('mockSteamReturn.txt', 'wb') as mockSteamReturn:
#     pickle.dump(steamGamesList, mockSteamReturn)

# exit(1)

# import os
# gamesOnDisk = os.listdir("/Volumes/babyBlue/Games/PC/")

class MatchQueueEntry:
    def __init__(self, gameNameFromSteam, gameNameOnDisk, steamIDNumber):
        self.gameNameFromSteam = gameNameFromSteam
        self.gameNameOnDisk = gameNameOnDisk
        self.steamIDNumber = steamIDNumber

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

class UserInputRequiredQueueEntry:
    def __init__(self, targetName, possibleMatchesList):
        self.targetName = targetName
        self.possibleMatchesList = possibleMatchesList
    
    def getTargetName(self):
        return self.targetName
    
    def getPossibleMatchesList(self):
        return self.possibleMatchesList

def iterateOverGamesListAndApplyMinimumEditDistance(gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, gamesOnDisk):
    for targetGame in gamesOnDisk:
        possibleMatchesList = []
        for game in steamGamesList:
            steamName = game['name']
            steamIDNumber = game['appid']
            score = similarity(steamName.lower(), targetGame.lower())
            if score >= 0.7:
                possibleMatchesList.append(PossibleMatchQueueEntry(steamName, steamIDNumber, score))
                if score == 1.0:
                    #print(steamName, targetGame, "added immediately")
                    gameNameMatchesProcessingQueue.put(MatchQueueEntry(steamName, targetGame, steamIDNumber))
                    break
        else:
            sortedMatches = sorted(possibleMatchesList, key=lambda x: x.getMatchScore(), reverse=True)
            uire = UserInputRequiredQueueEntry(targetGame, sortedMatches)
            userInputRequiredQueue.put(uire)

    # no more user input required after this
    userInputRequiredQueue.put(None)



#-----------------------------------------------------------------------------------------

# XXX mocks
with open('mockSteamReturn.txt', 'rb') as mockSteamReturn:
    steamGamesList = pickle.load(mockSteamReturn)
# XXX mocks
with open('mockGamesList.txt', 'rb') as mockGamesList:
    gamesOnDisk = pickle.load(mockGamesList)

from multiprocessing import Process, Queue

if __name__ == '__main__':
    gameNameMatchesProcessingQueue = Queue()
    userInputRequiredQueue = Queue()
    unmatchedGames = []

    # One process for going through the steamGamesList and applying the min edit dist algo.
    # adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
    GameListIteratorAndMinimumEditDistanceProcess = Process(target=iterateOverGamesListAndApplyMinimumEditDistance, args=(gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, gamesOnDisk))
    GameListIteratorAndMinimumEditDistanceProcess.start()
    
    userDefinedTagsFetcher = UserDefinedTagsFetcher()

    uire = userInputRequiredQueue.get()
    while uire != None:
        nameOnDisk = uire.getTargetName()
        print(f"found {nameOnDisk}")
        for possibleMatch in uire.getPossibleMatchesList():
            userInput = input(f"does it match '{possibleMatch.getSteamName()}' - {possibleMatch.steamIDNumber} - {possibleMatch.matchScore}? (y/n)")
            if userInput.lower() == 'y':
                gameNameMatchesProcessingQueue.put(possibleMatch.convertToMatchQueueEntry(nameOnDisk)) 
                userDefinedTagsFetcher.getTags(possibleMatch.steamIDNumber)       
                break
        else:
            unmatchedGames.append(nameOnDisk)
        uire = userInputRequiredQueue.get()


    
    GameListIteratorAndMinimumEditDistanceProcess.join()
    print(unmatchedGames)


# One process for going through the steamGamesList and applying the min edit dist algo - adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
# Main process for user input - allow user to make decisions about the games that don't have a 1.0 score - adds to the GamePerfectMatches queue
# One process for GameData - fetches from GamePerfectMatches queue to get the steam id and fetches from appreviews and appdetails - writes result to database

