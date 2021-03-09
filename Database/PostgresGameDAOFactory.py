from Database.PostgresGameDAO import PostgresGameDAO
from Database.PostgresConnectionFactory import PostgresConnectionFactory
class PostgresGameDAOFactory:
    @staticmethod
    def createGameDAO():
        return PostgresGameDAO(PostgresConnectionFactory)