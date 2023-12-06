from queue import Queue
from Database.PostgresGameDAO import PostgresGameDAO
from State.StateCommunicatorInterface import StateCommunicatorInterface
from ExternalDataFetchers.SteamAPIDataFetcher import (
    IncorrectAppTypeException,
    NoResponseException,
    ResponseUnsuccesfulException,
)
from Constants import END_OF_QUEUE
from psycopg2.errors import UniqueViolation
from GameFactory import GameFactory, FailedToGetAppDetailsException
from QueueEntries.Sendable import ErrorSendable
import logging

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="out.txt",
)


class DatabaseInsertException(Exception):
    pass


def game_lookup_and_storage_process(
    gameNameMatchesProcessingQueue: Queue,
    gameDAO: PostgresGameDAO,
    stateCommunicator: StateCommunicatorInterface,
    gameFactory: GameFactory,
):
    unableToInsert = []
    gnmpe = gameNameMatchesProcessingQueue.get()
    while gnmpe != END_OF_QUEUE:
        print("got ", gnmpe)
        gameNameOnDisk = gnmpe.get_game_name_on_disk()
        stateCommunicator.setInfoRetrievalActiveState(gnmpe)
        print("set ", gnmpe, "to info retrieval")
        try:
            game = gameFactory.create(gnmpe)
            print("created game")
            try:
                print("try to commit game")
                gameDAO.commit_game(game)
                stateCommunicator.setStoredState(game)
                print("success")
            except UniqueViolation as e:
                print("failure")
                errorString = f"Unable to insert: {gnmpe.get_steam_id_number()}, {gameNameOnDisk}\n{e}\ngame={game}"
                raise DatabaseInsertException(errorString)

        # YYY on exceptions, should I be tracking a state change to error?
        except (
            FailedToGetAppDetailsException,
            NoResponseException,
            ResponseUnsuccesfulException,
            IncorrectAppTypeException,
            DatabaseInsertException,
        ) as e:
            stateCommunicator.transitionToErrorState(ErrorSendable(gnmpe, e))
            unableToInsert.append(gameNameOnDisk)
            print(e)
            logging.critical(e)

        gnmpe = gameNameMatchesProcessingQueue.get()

    return unableToInsert
