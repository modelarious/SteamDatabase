from difflib import SequenceMatcher
from multiprocessing import Queue
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from typing import Match
from multiprocessing import Process
from QueueEntries.Sendable import ErrorSendable

from QueueEntries.MatchQueueEntry import MatchQueueEntry
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from Utilities.Constants import END_OF_QUEUE


# minimum edit distance algo with support for junk detection
def similarity(a, b):
    return SequenceMatcher(a=a, b=b).ratio()


# applies minimum edit distance to find close matches into a list.
# if it finds an exact match, it sends this off to the next step (gameNameMatchesProcessingQueue).
# if it doesn't find an exact match, it sends the list off to get input from the user (userInputRequiredQueue).
def apply_minimum_edit_distance(
    targetGame,
    gameNameMatchesProcessingQueue,
    userInputRequiredQueue,
    steamGamesList,
    quickSteamTitleMap,
    stateCommunicator,
):
    stateCommunicator.setFindingNameActiveState(targetGame)

    # try the fast method
    try:
        # XXX encapsulate the data access in an object - this logic should be paired with build_steam_title_map.
        # XXX We shouldn't have to know to pass it in lower case, for example.
        game = quickSteamTitleMap[targetGame.lower()]
        steamIDNumber = game["appid"]
        steamName = game["name"]
        mqe = MatchQueueEntry(targetGame, steamName, steamIDNumber)
        stateCommunicator.setQueuedForInfoRetrievalStateFromFindingNameActive(mqe)
        gameNameMatchesProcessingQueue.put(mqe)
        return

    except KeyError:
        # didn't find the title in the quick map - this is fine
        pass

    # XXX could refactor to the following which makes the game object smarter
    # XXX Though this section could use optimization if anything - maybe refactoring to
    # XXX use more objects would be a detriment
    # possibleMatches = UserInputRequiredQueueEntry(targetGame)
    # for game in steamGamesList:
    #     score = game.calculateSimilarity(targetGame)
    #     if score >= 0.7:
    #         possibleMatches.trackCloseMatch(game, score)

    #         # if perfect match
    #         if score == 1.0:
    #             queueLayer.addPerfectNameMatch(game, targetGame)
    #             break
    # else:
    #     queueLayer.askUserForSelection(possibleMatches)

    # fallback to the slow method
    minSimilarity = 0.7
    possibleMatchesList = []
    for game in steamGamesList:
        # XXX encapsulate the data access in an object
        steamName = game["name"]
        steamIDNumber = game["appid"]
        score = similarity(steamName.lower(), targetGame.lower())
        if score >= minSimilarity:
            possibleMatchesList.append(
                PossibleMatchQueueEntry(steamName, steamIDNumber, score)
            )
            # XXX YYY investigate - with the quickSteamTitleMap, is it still possible to hit this case?
            if score == 1.0:
                print(steamName, targetGame, "added immediately")
                mqe = MatchQueueEntry(targetGame, steamName, steamIDNumber)
                stateCommunicator.setQueuedForInfoRetrievalStateFromFindingNameActive(
                    mqe
                )
                gameNameMatchesProcessingQueue.put(mqe)
                break
    # score wasn't 1.0 for any of the values... XXX do the investigation mentioned above
    # if you find the 1.0 case isn't possible, you can take this out of the "else" block
    else:
        # sort by closest match first
        sortedMatches = sorted(
            possibleMatchesList, key=lambda x: x.get_match_score(), reverse=True
        )
        uire = UserInputRequiredQueueEntry(targetGame, sortedMatches)

        if len(sortedMatches) == 0:
            errorString = f"No matches exist for {uire.get_game_name_on_disk()} above {minSimilarity*100}%"
            stateCommunicator.transitionToErrorState(ErrorSendable(uire, errorString))
            return

        stateCommunicator.setAwaitingUserInputState(uire)
        userInputRequiredQueue.put(uire)


def minimum_edit_distance_processing(
    userInputRequiredQueue,
    gameNameMatchesProcessingQueue,
    steamGamesList,
    gamesOnDisk,
    quickSteamTitleMap,
    stateCommunicator,
):
    # (in an ideal world)
    # one core for the game_lookup_and_storage_process
    # one core for the user input process
    # the rest are used 2 per core for doing "nearest titles" search - MinimumEditDistanceProcess
    PER_CORE = 2
    OTHER_PROCESS_COUNT = 2
    MAX_WORKER_COUNT = 61
    availableCores = (cpu_count() - OTHER_PROCESS_COUNT) * PER_CORE
    numDesignatedCores = min(max(1, availableCores), MAX_WORKER_COUNT)
    print(f"numDesignatedCores = {numDesignatedCores}")

    print("starting process pool executor")
    with ProcessPoolExecutor(
        max_workers=numDesignatedCores
    ) as MinimumEditDistanceProcessPool:
        print("created process pool executor")
        # future = MinimumEditDistanceProcessPool.submit(pow, 323, 1235)
        # executor.map(is_prime, PRIMES)

        # fastest method of exhausting an iterable when you don't care about the output
        # https://code.activestate.com/lists/python-ideas/23364
        # exhaust_iterable = deque(maxlen=0).extend
        # exhaust_iterable(futureMap)

        # XXX https://bugs.python.org/issue30549 due to a bug in python3 up to 3.8
        # (and eventlet requires 3.7 specifically),
        # process pools will hang if they fail to serialize something. Apparently one of those
        # things that won't serialize are queues based on manager object, which makes NO sense
        # because I've been happily using them so far - praying that the following continues working
        #
        # XXX gather queues up into one object: QueueLayer (https://github.com/modelarious/SteamDatabase/issues/17)
        futureMap = {
            MinimumEditDistanceProcessPool.submit(
                apply_minimum_edit_distance,
                targetGame,
                gameNameMatchesProcessingQueue,
                userInputRequiredQueue,
                steamGamesList,
                quickSteamTitleMap,
                stateCommunicator,
            ): targetGame
            for targetGame in gamesOnDisk
        }
        print("submitted all the needed jobs")

        for future in as_completed(futureMap):
            possible_exception = future.exception()
            if possible_exception:
                print(possible_exception)  # XXX XXX XXX XXX XXX YYY YYY log this!!!

    # no more user input required after this
    userInputRequiredQueue.put(END_OF_QUEUE)
    print("placed END OF QUEUE onto the user input required queue")