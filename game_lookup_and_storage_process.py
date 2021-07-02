from GameModel import Game
from Constants import END_OF_QUEUE
from psycopg2.errors import UniqueViolation

import logging

logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/tmp/out.txt'
)

class FailedToGetAppDetailsException(Exception):
    pass

def game_lookup_and_storage_process(gameNameMatchesProcessingQueue, gameDAO, userDefinedGenresFetcher, steamAPIDataFetcher, pathOnDisk, stateCommunicator):
    unableToInsert = []
    gnmpe = gameNameMatchesProcessingQueue.get()
    while gnmpe != END_OF_QUEUE:
        stateCommunicator.setInfoRetrievalActiveState(gnmpe)
        gameNameOnDisk = gnmpe.getGameNameOnDisk()
        steamIDNumber = gnmpe.getSteamIDNumber()

        try:

            # XXX factory
            userGenres = userDefinedGenresFetcher.getGenres(steamIDNumber)
            reviewScore = steamAPIDataFetcher.getAvgReviewScore(steamIDNumber)
            app_detail = steamAPIDataFetcher.get_app_detail(steamIDNumber)

            if not app_detail:
                error_message = f'failed get_app_detail for {steamIDNumber}, {gnmpe}'
                raise FailedToGetAppDetailsException(error_message)
            
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
                gameDAO.commit_game(game)
                stateCommunicator.setStoredState(game)
            except UniqueViolation as e:
                unableToInsert.append(gameNameOnDisk)
                message = f'Unable to insert: {steamIDNumber}, {gameNameOnDisk}\n{e}\ngame={game}'
                logging.critical(message)
        except FailedToGetAppDetailsException as e:
            unableToInsert.append(gameNameOnDisk)
            logging.critical(e)

        gnmpe = gameNameMatchesProcessingQueue.get()
        
    return unableToInsert
