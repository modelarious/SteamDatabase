from ExternalDataFetchers.UserDefinedTagsFetcher import UserDefinedTagsFetcher
from ExternalDataFetchers.SteamAPIDataFetcher import SteamAPIDataFetcher
from minimumEditDistanceProcessing import minimumEditDistanceProcessing
from gameLookupAndStorageProcess import gameLookupAndStorageProcess
from Constants import END_OF_QUEUE
from Database.PostgresGameDAOFactory import PostgresGameDAOFactory

import pickle
from multiprocessing import Process, Manager

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



#-----------------------------------------------------------------------------------------


def build_steam_title_map(steamGamesList):
    steamTitleMap = dict()
    print(steamGamesList)
    for gameObj in steamGamesList:
        gameTitle = gameObj["name"].lower()
        steamTitleMap[gameTitle] = gameObj
    return steamTitleMap


# XXX this is ripe for refactor
def match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk):

    quickSteamTitleMap = build_steam_title_map(steamGamesList)

    print("creating manager and queues")
    m = Manager()
    gameNameMatchesProcessingQueue = m.Queue()
    userInputRequiredQueue = m.Queue()
    print("created manager and queues")

    print("constructing necessary objects")
    gameDAO = PostgresGameDAOFactory.createGameDAO()
    userDefinedTagsFetcher = UserDefinedTagsFetcher()
    steamAPIDataFetcher = SteamAPIDataFetcher()
    pathOnDisk = "/Volumes/babyBlue/Games/PC/"
    print("finished constructing necessary objects")

    print("launching game storage process")
    # XXX gameLookupAndStorageProcess -> game_lookup_and_storage_process
    GameLookupAndStorageProcess = Process(target=gameLookupAndStorageProcess, args=(gameNameMatchesProcessingQueue, gameDAO, userDefinedTagsFetcher, steamAPIDataFetcher, pathOnDisk))
    GameLookupAndStorageProcess.start()
    print("finished launching game storage process")


    # This process goes through the steamGamesList and applies the min edit dist algo. (uses a pool of processes to accomplish this quicker)
    # adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
    print("launching minimum edit distance handling process")
    MinimumEditDistanceProcess = Process(target=minimumEditDistanceProcessing, args=(userInputRequiredQueue, gameNameMatchesProcessingQueue, steamGamesList, gamesOnDisk, quickSteamTitleMap))
    MinimumEditDistanceProcess.start()
    print("finished launching minimum edit distance handling process")

    print("launching user input handling")
    unmatchedGames = []
    uire = userInputRequiredQueue.get()
    while uire != END_OF_QUEUE:
        nameOnDisk = uire.getTargetName()
        for possibleMatch in uire.getPossibleMatchesList():
            userInput = input(f"does it match '{possibleMatch.getSteamName()}' - {possibleMatch.steamIDNumber} - {possibleMatch.matchScore}? (y/n)")
            if userInput.lower() == 'y':
                gameNameMatchesProcessingQueue.put(possibleMatch.convertToMatchQueueEntry(nameOnDisk)) 
                break
        else:
            unmatchedGames.append(nameOnDisk)
        uire = userInputRequiredQueue.get()
    print("finished user input handling")

    # this process will signal to the user input process that it is finished by putting END_OF_QUEUE
    # on the userInputRequiredQueue
    MinimumEditDistanceProcess.join()
    print("finished processing games on the harddrive")

    # by this point there is nothing that will write to the gameNameMatchesProcessingQueue (that is being read by GameLookupAndStorageProcess)
    gameNameMatchesProcessingQueue.put(END_OF_QUEUE)

    unableToInsert = GameLookupAndStorageProcess.join()
    print(f"unmatchedGames={unmatchedGames}, unableToInsert={unableToInsert}")


if __name__ == '__main__':
    # XXX mocks
    print("mocking the steam games list from API")
    with open('mockSteamReturn.txt', 'rb') as mockSteamReturn:
        steamGamesList = pickle.load(mockSteamReturn)
    print("finished mocking the steam games list from API")

    # XXX mocks
    print("mocking the local games list from directory")
    with open('mockGamesList.txt', 'rb') as mockGamesList:
        gamesOnDisk = pickle.load(mockGamesList)
    print("finished mocking the local games list from directory")
    
    match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk)

    


# One process for going through the steamGamesList and applying the min edit dist algo - adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
# Main process for user input - allow user to make decisions about the games that don't have a 1.0 score - adds to the GamePerfectMatches queue
# One process for GameData - fetches from GamePerfectMatches queue to get the steam id and fetches from appreviews and appdetails - writes result to database

