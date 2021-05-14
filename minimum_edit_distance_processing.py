from difflib import SequenceMatcher
from multiprocessing import Queue
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from typing import Match
from multiprocessing import Process

from QueueEntries.MatchQueueEntry import MatchQueueEntry
from QueueEntries.PossibleMatchQueueEntry import PossibleMatchQueueEntry
from QueueEntries.UserInputRequiredQueueEntry import UserInputRequiredQueueEntry
from Constants import END_OF_QUEUE

# minimum edit distance algo with support for junk detection
def similarity(a, b):
    return SequenceMatcher(a=a, b=b).ratio()

# # applies minimum edit distance to find close matches into a list.
# # if it finds an exact match, it sends this off to the next step (gameNameMatchesProcessingQueue).
# # if it doesn't find an exact match, it sends the list off to get input from the user (userInputRequiredQueue).
# def apply_minimum_edit_distance(gameInputQueue, gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, quickSteamTitleMap, stateCommunicator, errorQueue):
#     try:
#         targetGame = gameInputQueue.get()
#         while targetGame != END_OF_QUEUE:
#             stateCommunicator.setFindingNameActiveState(targetGame)
#             print(targetGame)

#             # try the fast method
#             try:
#                 # XXX encapsulate the data access in an object - this logic should be paired with build_steam_title_map
#                 game = quickSteamTitleMap[targetGame.lower()]
#                 steamIDNumber = game['appid']
#                 steamName = game['name']
#                 mqe = MatchQueueEntry(steamName, targetGame, steamIDNumber)
#                 stateCommunicator.setQueuedForInfoRetrievalStateFromFindingNameActive(mqe)
#                 gameNameMatchesProcessingQueue.put(mqe)

#                 # XXX this is so bad
#                 targetGame = gameInputQueue.get()

#             except KeyError:
#                 # didn't find the title in the quick map - this is fine
#                 pass

#             # XXX could refactor to the following which makes the game object smarter
#             # XXX Though this section could use optimization if anything - maybe refactoring to
#             # XXX use more objects would be a detriment
#             # possibleMatches = UserInputRequiredQueueEntry(targetGame)
#             # for game in steamGamesList:
#             #     score = game.calculateSimilarity(targetGame)
#             #     if score >= 0.7:
#             #         possibleMatches.trackCloseMatch(game, score)

#             #         # if perfect match
#             #         if score == 1.0:
#             #             queueLayer.addPerfectNameMatch(game, targetGame)
#             #             break
#             # else:
#             #     queueLayer.askUserForSelection(possibleMatches)
            

            
#             # fallback to the slow method
#             possibleMatchesList = []
#             for game in steamGamesList:
#                 # XXX encapsulate the data access in an object
#                 steamName = game['name']
#                 steamIDNumber = game['appid']
#                 score = similarity(steamName.lower(), targetGame.lower())
#                 if score >= 0.7:
#                     possibleMatchesList.append(PossibleMatchQueueEntry(steamName, steamIDNumber, score))
#                     if score == 1.0:
#                         print("\n\n\n")
#                         print(steamName, targetGame, "added immediately")
#                         print("\n\n\n")
#                         mqe = MatchQueueEntry(steamName, targetGame, steamIDNumber)
#                         stateCommunicator.setQueuedForInfoRetrievalStateFromFindingNameActive(mqe)
#                         gameNameMatchesProcessingQueue.put(mqe)
#                         break
#             else:
#                 # sort by closest match first
#                 sortedMatches = sorted(possibleMatchesList, key=lambda x: x.getMatchScore(), reverse=True)
#                 uire = UserInputRequiredQueueEntry(targetGame, sortedMatches)
#                 stateCommunicator.setAwaitingUserInputState(uire)
#                 userInputRequiredQueue.put(uire)
            
#             targetGame = gameInputQueue.get()
#     except Exception as e:
#         errorQueue.put(e)

# applies minimum edit distance to find close matches into a list.
# if it finds an exact match, it sends this off to the next step (gameNameMatchesProcessingQueue).
# if it doesn't find an exact match, it sends the list off to get input from the user (userInputRequiredQueue).
def apply_minimum_edit_distance(targetGame, gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, quickSteamTitleMap, stateCommunicator):
    try:
        stateCommunicator.setFindingNameActiveState(targetGame)
        print(targetGame)

        # try the fast method
        try:
            # XXX encapsulate the data access in an object - this logic should be paired with build_steam_title_map
            game = quickSteamTitleMap[targetGame.lower()]
            steamIDNumber = game['appid']
            steamName = game['name']
            mqe = MatchQueueEntry(steamName, targetGame, steamIDNumber)
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
        possibleMatchesList = []
        for game in steamGamesList:
            # XXX encapsulate the data access in an object
            steamName = game['name']
            steamIDNumber = game['appid']
            # returnQueue = Queue()
            # process = Process(target=similarity, args=(steamName.lower(), targetGame.lower(), returnQueue))
            # process.start()
            # process.join()
            # score = returnQueue.get()
            score = similarity(steamName.lower(), targetGame.lower())
            if score >= 0.7:
                possibleMatchesList.append(PossibleMatchQueueEntry(steamName, steamIDNumber, score))
                if score == 1.0:
                    print("\n\n\n")
                    print(steamName, targetGame, "added immediately")
                    print("\n\n\n")
                    mqe = MatchQueueEntry(steamName, targetGame, steamIDNumber)
                    stateCommunicator.setQueuedForInfoRetrievalStateFromFindingNameActive(mqe)
                    gameNameMatchesProcessingQueue.put(mqe)
                    break
        else:
            # sort by closest match first
            sortedMatches = sorted(possibleMatchesList, key=lambda x: x.getMatchScore(), reverse=True)
            uire = UserInputRequiredQueueEntry(targetGame, sortedMatches)
            stateCommunicator.setAwaitingUserInputState(uire)
            userInputRequiredQueue.put(uire)
        
    except Exception as e:
        print(e)

def minimum_edit_distance_processing(userInputRequiredQueue, gameNameMatchesProcessingQueue, steamGamesList, gamesOnDisk, quickSteamTitleMap, stateCommunicator):
    # (in an ideal world)
    # one core for the game_lookup_and_storage_process
    # one core for the user input process
    # the rest are used 2 per core for doing "nearest titles" search - MinimumEditDistanceProcess
    PER_CORE = 2
    OTHER_PROCESS_COUNT = 2
    availableCores = (cpu_count() - OTHER_PROCESS_COUNT) * PER_CORE
    numDesignatedCores = max(1, availableCores)
    print(f"numDesignatedCores = {numDesignatedCores}")

    # gameInputQueue = Queue()
    # for item in gamesOnDisk:
    #     gameInputQueue.put(item)
    
    # errorQueue = Queue()

    # from multiprocessing import Process
    # processes = []
    # for _ in range(4):
    #     process = Process(target=apply_minimum_edit_distance, args=(gameInputQueue, gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, quickSteamTitleMap, stateCommunicator, errorQueue))
    #     process.start()
    #     processes.append(process)
    
    # for process in processes:
    #     process.join()
    #     print("\n\n\n\nJOINED PROCESS")
    #     print("looking for error")
    #     try:
    #         e = errorQueue.get(timeout=5)
    #         print(f"got {e}")
    #     except:
    #         pass
    
    # userInputRequiredQueue.put(END_OF_QUEUE)
    # print("placed END OF QUEUE onto the user input required queue")



    # from multiprocessing.pool import Pool
    # pool = Pool(numDesignatedCores)
    # pool.apply_async

    print("starting process pool executor")
    with ProcessPoolExecutor(max_workers=numDesignatedCores) as MinimumEditDistanceProcessPool:
        print("created process pool executor")
        # future = MinimumEditDistanceProcessPool.submit(pow, 323, 1235)
        # executor.map(is_prime, PRIMES)

        # fastest method of exhausting an iterable when you don't care about the output
        # https://code.activestate.com/lists/python-ideas/23364
        # exhaust_iterable = deque(maxlen=0).extend
        # exhaust_iterable(futureMap)

        # XXX due to a bug in python3 up to 3.8 (and eventlet requires 3.7 specifically), 
        # process pools will hang if they fail to serialize something. Apparently one of those
        # things that won't serialize are queues based on manager object, which makes NO sense
        # because I've been happily using them so far
        #
        # XXX gather queues up into one object: QueueLayer (https://github.com/modelarious/SteamDatabase/issues/17)
        futureMap = {
            MinimumEditDistanceProcessPool.submit(
                apply_minimum_edit_distance, targetGame, gameNameMatchesProcessingQueue, userInputRequiredQueue, steamGamesList, quickSteamTitleMap, stateCommunicator
            ) : targetGame
            for targetGame in gamesOnDisk
        }
        print("submitted all the needed jobs")
        print(futureMap)

        for future in as_completed(futureMap):
            result = future.result() # unused

    # no more user input required after this
    userInputRequiredQueue.put(END_OF_QUEUE)
    print("placed END OF QUEUE onto the user input required queue")