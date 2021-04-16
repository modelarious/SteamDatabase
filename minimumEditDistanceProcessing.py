from difflib import SequenceMatcher
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count

from QueueEntries.MatchQueueEntry import MatchQueueEntry
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from Constants import END_OF_QUEUE


# minimum edit distance algo with support for junk detection
def similarity(a, b):
    return SequenceMatcher(a=a, b=b).ratio()


# applies minimum edit distance to find close matches into a list.
# if it finds an exact match, it sends this off to the next step (gameNameMatchesProcessingQueue).
# if it doesn't find an exact match, it sends the list off to get input from the user (userInputRequiredQueue).
def apply_minimum_edit_distance(targetGame, gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, quickSteamTitleMap):
    print(targetGame)

    # try the fast method
    try:
        # XXX encapsulate the data access in an object - this logic should be paired with build_steam_title_map
        game = quickSteamTitleMap[targetGame.lower()]
        steamIDNumber = game['appid']
        steamName = game['name']
        gameNameMatchesProcessingQueue.put(MatchQueueEntry(steamName, targetGame, steamIDNumber))
        return
    except KeyError:
        # didn't find the title in the quick map - this is fine
        pass

    # fallback to the slow method
    possibleMatchesList = []
    for game in steamGamesList:
        # XXX encapsulate the data access in an object
        steamName = game['name']
        steamIDNumber = game['appid']
        score = similarity(steamName.lower(), targetGame.lower())
        if score >= 0.7:
            possibleMatchesList.append(PossibleMatchQueueEntry(steamName, steamIDNumber, score))
            if score == 1.0:
                print(steamName, targetGame, "added immediately")
                gameNameMatchesProcessingQueue.put(MatchQueueEntry(steamName, targetGame, steamIDNumber))
                break
    else:
        # sort by closest match first
        sortedMatches = sorted(possibleMatchesList, key=lambda x: x.getMatchScore(), reverse=True)
        uire = UserInputRequiredQueueEntry(targetGame, sortedMatches)
        userInputRequiredQueue.put(uire)


def minimumEditDistanceProcessing(userInputRequiredQueue, gameNameMatchesProcessingQueue, steamGamesList, gamesOnDisk, quickSteamTitleMap):
    # (in an ideal world)
    # one core for the gameLookupAndStorageProcess
    # one core for the user input process
    # the rest are used 2 per core for doing "nearest titles" search - MinimumEditDistanceProcess
    PER_CORE = 2
    OTHER_PROCESS_COUNT = 2
    availableCores = (cpu_count() - OTHER_PROCESS_COUNT) * PER_CORE
    numDesignatedCores = max(1, availableCores)
    print(f"numDesignatedCores = {numDesignatedCores}")

    print("starting process pool executor")
    with ProcessPoolExecutor(max_workers=numDesignatedCores) as MinimumEditDistanceProcessPool:
        # future = MinimumEditDistanceProcessPool.submit(pow, 323, 1235)
        # executor.map(is_prime, PRIMES)

        # fastest method of exhausting an iterable when you don't care about the output
        # https://code.activestate.com/lists/python-ideas/23364
        # exhaust_iterable = deque(maxlen=0).extend
        # exhaust_iterable(futureMap)

        # XXX gather queues up into one object: QueueLayer (https://github.com/modelarious/SteamDatabase/issues/17)
        futureMap = {
            MinimumEditDistanceProcessPool.submit(
                apply_minimum_edit_distance, targetGame, gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, quickSteamTitleMap
            ) : targetGame
            for targetGame in gamesOnDisk
        }

        for future in as_completed(futureMap):
            result = future.result() # unused

    # no more user input required after this
    userInputRequiredQueue.put(END_OF_QUEUE)