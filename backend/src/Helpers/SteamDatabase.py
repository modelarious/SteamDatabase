from Game.GameFactory import GameFactory
from State.StateCommunicatorInterface import StateCommunicatorInterface
from Helpers.minimum_edit_distance_processing import minimum_edit_distance_processing
from Helpers.game_lookup_and_storage_process import game_lookup_and_storage_process
from Utilities.Constants import END_OF_QUEUE
from Database.PostgresGameDAOFactory import PostgresGameDAOFactory
from QueueEntries.MatchQueueEntry import MatchQueueEntry
from multiprocessing import Process, Manager
from queue import Empty
from typing import Callable
from Server.SocketWrapper import SocketWrapper


def build_steam_title_map(steamGamesList):
    steamTitleMap = dict()
    for gameObj in steamGamesList:
        gameTitle = gameObj["name"].lower()
        steamTitleMap[gameTitle] = gameObj
    return steamTitleMap


def ui_handling(
    userInputRequiredQueue,
    gameNameMatchesProcessingQueue,
    stateCommunicator,
    input_socket_fetch_function,
):
    queuedGames = []
    while queuedGames != [END_OF_QUEUE]:
        print(f"queuedGames = {queuedGames}")
        # block on waiting for message from socket from user input section
        input_socket = input_socket_fetch_function()
        match_queue_entry = MatchQueueEntry(**input_socket.get_message())

        # transistion to the info retrieval state
        stateCommunicator.setQueuedForInfoRetrievalStateFromAwaitingUser(
            match_queue_entry
        )
        gameNameMatchesProcessingQueue.put(match_queue_entry)

        # gather all currently queued items
        inputAvailable = True
        while inputAvailable:
            try:
                game = userInputRequiredQueue.get(block=False)
                queuedGames.append(game)
            except Empty:
                inputAvailable = False

        # remove the one we just dealt with from the array to ensure we approach the exit condition
        for queuedGame in queuedGames:
            if queuedGame.game_name_on_disk == match_queue_entry.game_name_on_disk:
                queuedGames.remove(queuedGame)
                break
        else:
            errorString = f"\n\n\n\n\n\n\n\nFAILED TO FIND MATCH FOR GAME {match_queue_entry}\n\n\n\n\n\n\n\n\n"
            raise Exception(errorString)


# XXX this is ripe for refactor.
# XXX Go all Dependency Injection on it's ass.
def match_steam_games_to_games_on_disk_and_store(
    steamGamesList,
    gamesOnDisk,
    stateCommunicator: StateCommunicatorInterface,
    pathOnDisk: str,
    input_socket_fetch_function: Callable[[], SocketWrapper],
):
    stateCommunicator.batchSetUpcomingState(gamesOnDisk)

    quickSteamTitleMap = build_steam_title_map(steamGamesList)

    print("creating manager and queues")
    m = Manager()
    gameNameMatchesProcessingQueue = m.Queue()
    userInputRequiredQueue = m.Queue()
    print("created manager and queues")

    print("constructing necessary objects")
    postgresGameDAOFactory = PostgresGameDAOFactory()
    gameDAO = postgresGameDAOFactory.createGameDAO()
    gameFactory = GameFactory(pathOnDisk)
    print("finished constructing necessary objects")

    print("launching game storage process")
    gameLookupAndStorageProcess = Process(
        target=game_lookup_and_storage_process,
        args=(gameNameMatchesProcessingQueue, gameDAO, stateCommunicator, gameFactory),
    )
    gameLookupAndStorageProcess.start()
    print("finished launching game storage process")

    # This process goes through the steamGamesList and applies the min edit dist algo. (uses a pool of processes to accomplish this quicker)
    # adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
    print("launching minimum edit distance handling process")
    minimumEditDistanceProcess = Process(
        target=minimum_edit_distance_processing,
        args=(
            userInputRequiredQueue,
            gameNameMatchesProcessingQueue,
            steamGamesList,
            gamesOnDisk,
            quickSteamTitleMap,
            stateCommunicator,
        ),
    )
    minimumEditDistanceProcess.start()
    print("finished launching minimum edit distance handling process")

    # this is intendid to be blocking
    print("launching user input handling")
    ui_handling(
        userInputRequiredQueue,
        gameNameMatchesProcessingQueue,
        stateCommunicator,
        input_socket_fetch_function,
    )
    print("finished user input handling")

    # this process will signal to the user input process that it is finished by putting END_OF_QUEUE
    # on the userInputRequiredQueue
    minimumEditDistanceProcess.join()
    print("finished processing games on the harddrive")

    # by this point there is nothing that will write to the gameNameMatchesProcessingQueue (that is being read by gameLookupAndStorageProcess)
    gameNameMatchesProcessingQueue.put(END_OF_QUEUE)
    print("placed END OF QUEUE onto the game name matches queue")

    unableToInsert = gameLookupAndStorageProcess.join()
    print(f"unableToInsert={unableToInsert}")


# One process for going through the steamGamesList and applying the min edit dist algo - adds matches that are 1.0 to the GamePerfectMatches queue, adds anything else UserInputRequired queue for user input process to consume
# Main process for user input - allow user to make decisions about the games that don't have a 1.0 score - adds to the GamePerfectMatches queue
# One process for GameData - fetches from GamePerfectMatches queue to get the steam id and fetches from appreviews and appdetails - writes result to database
