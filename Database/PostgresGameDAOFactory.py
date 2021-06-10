from Database.PostgresGameDAO import PostgresGameDAO
from Database.PostgresConnectionFactory import PostgresConnectionFactory
class PostgresGameDAOFactory:
    def createGameDAO(self):
        return PostgresGameDAO(PostgresConnectionFactory)