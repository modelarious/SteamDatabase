from difflib import SequenceMatcher

# minimum edit distance algo with support for junk detection
def similarity(a, b):
    return SequenceMatcher(a=a, b=b).ratio()

END_OF_QUEUE = None


from UserDefinedTagsFetcher import UserDefinedTagsFetcher
from SteamAPIDataFetcher import SteamAPIDataFetcher
import pickle
from GameModel import Game

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

    def getGameNameFromSteam(self):
        return self.gameNameFromSteam
    
    def getGameNameOnDisk(self):
        return self.gameNameOnDisk

    def getSteamIDNumber(self):
        return self.steamIDNumber

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

# GameListProcessingService
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
    userInputRequiredQueue.put(END_OF_QUEUE)

def gameLookupAndStorageProcess(gameNameMatchesProcessingQueue, gameDAO, userDefinedTagsFetcher, steamAPIDataFetcher, pathOnDisk):
    gnmpe = gameNameMatchesProcessingQueue.get()
    while gnmpe != END_OF_QUEUE:
        print("found a game")
        steamIDNumber = gnmpe.getSteamIDNumber()
        userTags = userDefinedTagsFetcher.getTags(steamIDNumber)
        reviewScore = steamAPIDataFetcher.getAvgReviewScore(steamIDNumber)

        gameNameOnDisk = gnmpe.getGameNameOnDisk()

        game = Game(
            steam_id=steamIDNumber, 
            name_on_harddrive=gameNameOnDisk, 
            path_on_harddrive=pathOnDisk + gameNameOnDisk, 
            name_on_steam=gnmpe.getGameNameFromSteam(), 
            avg_review_score=reviewScore,
            user_defined_tags=userTags
        )

        gameDAO.commitGame(game)
        gnmpe = gameNameMatchesProcessingQueue.get()



#-----------------------------------------------------------------------------------------

# XXX mocks
with open('mockSteamReturn.txt', 'rb') as mockSteamReturn:
    steamGamesList = pickle.load(mockSteamReturn)
# XXX mocks
with open('mockGamesList.txt', 'rb') as mockGamesList:
    gamesOnDisk = pickle.load(mockGamesList)

from multiprocessing import Process, Queue
from GameDAOPostgresImplementation import PostgresGameDAOFactory

if __name__ == '__main__':
    gameNameMatchesProcessingQueue = Queue()
    userInputRequiredQueue = Queue()
    unmatchedGames = []

    gameDAO = PostgresGameDAOFactory.createGameDAO()
    userDefinedTagsFetcher = UserDefinedTagsFetcher()
    steamAPIDataFetcher = SteamAPIDataFetcher()
    pathOnDisk = "/Volumes/babyBlue/Games/PC/"
    GameLookupAndStorageProcess = Process(target=gameLookupAndStorageProcess, args=(gameNameMatchesProcessingQueue, gameDAO, userDefinedTagsFetcher, steamAPIDataFetcher, pathOnDisk))
    GameLookupAndStorageProcess.start()

    # One process for going through the steamGamesList and applying the min edit dist algo.
    # adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
    GameListIteratorAndMinimumEditDistanceProcess = Process(target=iterateOverGamesListAndApplyMinimumEditDistance, args=(gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, gamesOnDisk))
    GameListIteratorAndMinimumEditDistanceProcess.start()

    uire = userInputRequiredQueue.get()
    while uire != END_OF_QUEUE:
        nameOnDisk = uire.getTargetName()
        print(f"found {nameOnDisk}")
        for possibleMatch in uire.getPossibleMatchesList():
            userInput = input(f"does it match '{possibleMatch.getSteamName()}' - {possibleMatch.steamIDNumber} - {possibleMatch.matchScore}? (y/n)")
            if userInput.lower() == 'y':
                gameNameMatchesProcessingQueue.put(possibleMatch.convertToMatchQueueEntry(nameOnDisk)) 
                break
        else:
            unmatchedGames.append(nameOnDisk)
        uire = userInputRequiredQueue.get()

    GameListIteratorAndMinimumEditDistanceProcess.join()

    # by this point there is nothing that will write to the gameNameMatchesProcessingQueue (that is being read by GameLookupAndStorageProcess)
    gameNameMatchesProcessingQueue.put(END_OF_QUEUE)
    GameLookupAndStorageProcess.join()
    print(f"unmatchedGames={unmatchedGames}")


# One process for going through the steamGamesList and applying the min edit dist algo - adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
# Main process for user input - allow user to make decisions about the games that don't have a 1.0 score - adds to the GamePerfectMatches queue
# One process for GameData - fetches from GamePerfectMatches queue to get the steam id and fetches from appreviews and appdetails - writes result to database

