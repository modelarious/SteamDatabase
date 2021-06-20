from State.StateCommunicatorInterface import StateCommunicatorInterface
from ExternalDataFetchers.UserDefinedGenresFetcher import UserDefinedGenresFetcher
from ExternalDataFetchers.SteamAPIDataFetcher import AppDetailFactory, SteamAPIDataFetcher
from minimum_edit_distance_processing import minimum_edit_distance_processing
from game_lookup_and_storage_process import game_lookup_and_storage_process
from Constants import END_OF_QUEUE
from Database.PostgresGameDAOFactory import PostgresGameDAOFactory

from multiprocessing import Process, Manager

def build_steam_title_map(steamGamesList):
    steamTitleMap = dict()
    for gameObj in steamGamesList:
        gameTitle = gameObj["name"].lower()
        steamTitleMap[gameTitle] = gameObj
    return steamTitleMap

# XXX this is ripe for refactor.
# XXX Go all Dependency Injection on it's ass.
# XXX move UI handling into a dedicated function or class
def match_steam_games_to_games_on_disk_and_store(steamGamesList, gamesOnDisk, stateCommunicator: StateCommunicatorInterface):
    stateCommunicator.batchSetUpcomingState(gamesOnDisk)
    
    quickSteamTitleMap = build_steam_title_map(steamGamesList)

    print("creating manager and queues")
    # XXX do these need to be manager queues anymore or could they be multiprocessing queues now?
    m = Manager()
    gameNameMatchesProcessingQueue = m.Queue()
    userInputRequiredQueue = m.Queue()
    print("created manager and queues")

    print("constructing necessary objects")
    postgresGameDAOFactory = PostgresGameDAOFactory()
    gameDAO = postgresGameDAOFactory.createGameDAO()
    userDefinedGenresFetcher = UserDefinedGenresFetcher()
    app_detail_factory = AppDetailFactory()
    steamAPIDataFetcher = SteamAPIDataFetcher(app_detail_factory)
    pathOnDisk = "/Volumes/babyBlue/Games/PC/"
    print("finished constructing necessary objects")

    print("launching game storage process")
    gameLookupAndStorageProcess = Process(target=game_lookup_and_storage_process, args=(gameNameMatchesProcessingQueue, gameDAO, userDefinedGenresFetcher, steamAPIDataFetcher, pathOnDisk, stateCommunicator))
    gameLookupAndStorageProcess.start()
    print("finished launching game storage process")
    
    # This process goes through the steamGamesList and applies the min edit dist algo. (uses a pool of processes to accomplish this quicker)
    # adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
    print("launching minimum edit distance handling process")
    minimumEditDistanceProcess = Process(target=minimum_edit_distance_processing, args=(userInputRequiredQueue, gameNameMatchesProcessingQueue, steamGamesList, gamesOnDisk, quickSteamTitleMap, stateCommunicator))
    minimumEditDistanceProcess.start()
    print("finished launching minimum edit distance handling process")

    from time import sleep
    from random import randint

    print("launching user input handling")
    unmatchedGames = []
    uire = userInputRequiredQueue.get()
    while uire != END_OF_QUEUE:
        nameOnDisk = uire.getGameName()
        inputs = ['n', 'y']
        for idx, possibleMatch in enumerate(uire.getPossibleMatchesList()):
            # XXX What are you doing to that poor possibleMatch object? Why are you grabbing internals?
            # userInput = input(f"does it match '{possibleMatch.getSteamName()}' - {possibleMatch.steamIDNumber} - {possibleMatch.matchScore}? (y/n)")
            # sleep(randint(1, 10))
            userInput = inputs[idx]
            userInput = 'y'
            if userInput.lower() == 'y':
                mqe = possibleMatch.convertToMatchQueueEntry(nameOnDisk)
                stateCommunicator.setQueuedForInfoRetrievalStateFromAwaitingUser(mqe)
                gameNameMatchesProcessingQueue.put(mqe) 
                break
        else:
            stateCommunicator.rejectedByUser(uire)
            unmatchedGames.append(nameOnDisk)
        uire = userInputRequiredQueue.get()
    print("finished user input handling")

    # this process will signal to the user input process that it is finished by putting END_OF_QUEUE
    # on the userInputRequiredQueue
    # XXX YYY XXX YYY
    minimumEditDistanceProcess.join()
    print("finished processing games on the harddrive")

    # by this point there is nothing that will write to the gameNameMatchesProcessingQueue (that is being read by gameLookupAndStorageProcess)
    gameNameMatchesProcessingQueue.put(END_OF_QUEUE)

    unableToInsert = gameLookupAndStorageProcess.join()
    print(f"unmatchedGames={unmatchedGames}, unableToInsert={unableToInsert}")
    m.join()
    


# One process for going through the steamGamesList and applying the min edit dist algo - adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
# Main process for user input - allow user to make decisions about the games that don't have a 1.0 score - adds to the GamePerfectMatches queue
# One process for GameData - fetches from GamePerfectMatches queue to get the steam id and fetches from appreviews and appdetails - writes result to database
