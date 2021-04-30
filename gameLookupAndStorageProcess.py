from GameModel import Game
from Constants import END_OF_QUEUE
from psycopg2.errors import UniqueViolation

def gameLookupAndStorageProcess(gameNameMatchesProcessingQueue, gameDAO, userDefinedTagsFetcher, steamAPIDataFetcher, pathOnDisk, stateCommunicator):
    unableToInsert = []
    gnmpe = gameNameMatchesProcessingQueue.get()
    while gnmpe != END_OF_QUEUE:
        stateCommunicator.setInfoRetrievalActiveState(gnmpe)

        gameNameOnDisk = gnmpe.getGameNameOnDisk()
        steamIDNumber = gnmpe.getSteamIDNumber()
        userTags = userDefinedTagsFetcher.getTags(steamIDNumber)
        reviewScore = steamAPIDataFetcher.getAvgReviewScore(steamIDNumber)
        
        game = Game(
            steam_id=steamIDNumber, 
            name_on_harddrive=gameNameOnDisk, 
            path_on_harddrive=pathOnDisk + gameNameOnDisk, 
            name_on_steam=gnmpe.getGameNameFromSteam(), 
            avg_review_score=reviewScore,
            user_defined_tags=userTags
        )

        # YYY on exceptions, should I be tracking a state change to error?
        try:
            gameDAO.commitGame(game)
            stateCommunicator.setStoredState(game)
        except UniqueViolation:
            unableToInsert.append(gameNameOnDisk)
        
        gnmpe = gameNameMatchesProcessingQueue.get()
        
    return unableToInsert