from GameModel import Game
from Constants import END_OF_QUEUE
from psycopg2.errors import UniqueViolation

def gameLookupAndStorageProcess(gameNameMatchesProcessingQueue, gameDAO, userDefinedTagsFetcher, steamAPIDataFetcher, pathOnDisk):
    unableToInsert = []
    gnmpe = gameNameMatchesProcessingQueue.get()
    while gnmpe != END_OF_QUEUE:
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

        try:
            gameDAO.commitGame(game)
        except UniqueViolation:
            unableToInsert.append(gameNameOnDisk)
        
        gnmpe = gameNameMatchesProcessingQueue.get()
        
    return unableToInsert