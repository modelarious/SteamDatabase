from difflib import SequenceMatcher

# minimum edit distance algo with support for junk detection
def similarity(a, b):
    return SequenceMatcher(a=a, b=b).ratio()

END_OF_QUEUE = None


from UserDefinedTagsFetcher import UserDefinedTagsFetcher
import pickle

#---------------------------------------------------------------------------------------
# https://store.steampowered.com/appreviews/2028850?json=1  
# review
# https://store.steampowered.com/api/appdetails?appids=2028850 
# "2028850" -> "data" -> "detailed_description"
# "2028850" -> "data" -> "categories":[
        #     {
        #        "id":2,
        #        "description":"Single-player"
        #     },
        #     {
        #        "id":21,
        #        "description":"Downloadable Content"
        #     },
        #     {
        #        "id":22,
        #        "description":"Steam Achievements"
        #     },
        #     {
        #        "id":28,
        #        "description":"Full controller support"
        #     },
        #     {
        #        "id":23,
        #        "description":"Steam Cloud"
        #     }
        #  ],
        #  "genres":[
        #     {
        #        "id":"1",
        #        "description":"Action"
        #     }
        #  ],
        #  "screenshots":[
        #     {
        #        "id":0,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_c6f3fbf3e9f4cb1777462150203a7174608dfcd9.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_c6f3fbf3e9f4cb1777462150203a7174608dfcd9.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":1,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_d45294620026ff41f7e6b8610c6d60e13645fbf3.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_d45294620026ff41f7e6b8610c6d60e13645fbf3.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":2,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_3a364ffdcd2c1eeb3957435c624fc7c383d8cb69.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_3a364ffdcd2c1eeb3957435c624fc7c383d8cb69.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":3,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_26e2d983948edfb911db3e0d2c3679900b4ef9fa.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_26e2d983948edfb911db3e0d2c3679900b4ef9fa.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":4,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_4616da02724c2beaa8afc74a501929d27a65542a.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_4616da02724c2beaa8afc74a501929d27a65542a.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":5,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_fd6f5de55332f6c3cd119a01a9e017e840765c0e.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_fd6f5de55332f6c3cd119a01a9e017e840765c0e.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":6,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_37f25110f8d76335ddbc29a381bc6961e209acf6.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_37f25110f8d76335ddbc29a381bc6961e209acf6.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":7,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_dc76723504ce89c1ed1f66fd468682ba76548c32.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_dc76723504ce89c1ed1f66fd468682ba76548c32.1920x1080.jpg?t=1560961334"
        #     },
        #     {
        #        "id":8,
        #        "path_thumbnail":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_e98deaf0e334206b84c2462276aee98107fa20d0.600x338.jpg?t=1560961334",
        #        "path_full":"https:\/\/cdn.akamai.steamstatic.com\/steam\/apps\/2028850\/ss_e98deaf0e334206b84c2462276aee98107fa20d0.1920x1080.jpg?t=1560961334"
        #     }
        #  ],
        #  "release_date":{
        #     "coming_soon":false,
        #     "date":"25 Jun, 2013"
        #  },




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

def GameLookupAndStorageProcess(gameNameMatchesProcessingQueue):


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

    GameLookupAndStorageProcess = Process(target=GameLookupAndStorageProcess, args=(gameNameMatchesProcessingQueue))

    # One process for going through the steamGamesList and applying the min edit dist algo.
    # adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
    GameListIteratorAndMinimumEditDistanceProcess = Process(target=iterateOverGamesListAndApplyMinimumEditDistance, args=(gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, gamesOnDisk))
    GameListIteratorAndMinimumEditDistanceProcess.start()
    
    userDefinedTagsFetcher = UserDefinedTagsFetcher()

    uire = userInputRequiredQueue.get()
    while uire != END_OF_QUEUE:
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

    # by this point there is nothing that will write to the gameNameMatchesProcessingQueue (that is being read by GameLookupAndStorageProcess)
    gameNameMatchesProcessingQueue.put(END_OF_QUEUE)
    print(f"unmatchedGames={unmatchedGames}")


# One process for going through the steamGamesList and applying the min edit dist algo - adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
# Main process for user input - allow user to make decisions about the games that don't have a 1.0 score - adds to the GamePerfectMatches queue
# One process for GameData - fetches from GamePerfectMatches queue to get the steam id and fetches from appreviews and appdetails - writes result to database

