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
        # print("got ", gnmpe)
        stateCommunicator.setInfoRetrievalActiveState(gnmpe)
        # print("set ", gnmpe, "to info retrieval")
        gameNameOnDisk = gnmpe.get_game_name_on_disk()
        steamIDNumber = gnmpe.get_steam_id_number()

        try:

            # XXX factory
            userGenres = userDefinedGenresFetcher.getGenres(steamIDNumber)
            reviewScore = steamAPIDataFetcher.getAvgReviewScore(steamIDNumber)
            app_detail = steamAPIDataFetcher.get_app_detail(steamIDNumber)

            if not app_detail:
                raise FailedToGetAppDetailsException(f'failed get_app_detail for {steamIDNumber}, {gnmpe}')
            
            game = Game(
                steam_id=steamIDNumber, 
                game_name_on_disk=gameNameOnDisk,
                path_on_harddrive=pathOnDisk, 
                game_name_from_steam=gnmpe.get_game_name_from_steam(), 
                avg_review_score=reviewScore,
                user_defined_genres=userGenres,
                app_detail=app_detail
            )

            # print(f"""
            #     steam_id={steamIDNumber}, 
            #     game_name_on_disk={gameNameOnDisk},
            #     path_on_harddrive={pathOnDisk}, 
            #     game_name_from_steam={gnmpe.get_game_name_from_steam()}, 
            #     avg_review_score={reviewScore},
            #     user_defined_genres={userGenres},
            #     app_detail={app_detail}
            #     """
            # )

            # print("created game")

            # YYY on exceptions, should I be tracking a state change to error?
            try:
                # print("try to commit game")
                gameDAO.commit_game(game)
                stateCommunicator.setStoredState(game)
                # print("success")
            except UniqueViolation as e:
                unableToInsert.append(gameNameOnDisk)
                message = f'Unable to insert: {steamIDNumber}, {gameNameOnDisk}\n{e}\ngame={game}'
                logging.critical(message)
                # print(f"failure {message}")
        except FailedToGetAppDetailsException as e:
            unableToInsert.append(gameNameOnDisk)
            logging.critical(e)

        gnmpe = gameNameMatchesProcessingQueue.get()
        
    return unableToInsert
