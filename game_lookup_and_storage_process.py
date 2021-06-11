from GameModel import Game
from Constants import END_OF_QUEUE
from psycopg2.errors import UniqueViolation

def game_lookup_and_storage_process(gameNameMatchesProcessingQueue, gameDAO, userDefinedGenresFetcher, steamAPIDataFetcher, pathOnDisk, stateCommunicator):
    unableToInsert = []
    gnmpe = gameNameMatchesProcessingQueue.get()
    while gnmpe != END_OF_QUEUE:
        stateCommunicator.setInfoRetrievalActiveState(gnmpe)

        # XXX factory
        gameNameOnDisk = gnmpe.getGameNameOnDisk()
        steamIDNumber = gnmpe.getSteamIDNumber()
        userGenres = userDefinedGenresFetcher.getGenres(steamIDNumber)
        reviewScore = steamAPIDataFetcher.getAvgReviewScore(steamIDNumber)
        app_detail = steamAPIDataFetcher.get_app_detail(steamIDNumber)
        
        game = Game(
            steam_id=steamIDNumber, 
            name_on_harddrive=gameNameOnDisk, 
            path_on_harddrive=pathOnDisk + gameNameOnDisk, 
            name_on_steam=gnmpe.getGameNameFromSteam(), 
            avg_review_score=reviewScore,
            user_defined_genres=userGenres,
            app_detail=app_detail
        )

        # YYY on exceptions, should I be tracking a state change to error?
        try:
            gameDAO.commitGame(game)
            stateCommunicator.setStoredState(game)
        except UniqueViolation:
            unableToInsert.append(gameNameOnDisk)
        
        gnmpe = gameNameMatchesProcessingQueue.get()
        
    return unableToInsert