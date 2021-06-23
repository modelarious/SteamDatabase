from ObjectRelationalMapper.ORMMapper import ORMMapper
from ObjectRelationalMapper.StatementCreation.StatementCreationFacadePostgresFactory import StatementCreationFacadePostgresFactory
from Database.PostgresGameDAO import PostgresGameDAO
from Database.PostgresConnectionFactory import PostgresConnectionFactory
class PostgresGameDAOFactory:
    def createGameDAO(self):
        statement_creation_facade = StatementCreationFacadePostgresFactory()
        orm_mapper = ORMMapper(statement_creation_facade.create())
        postgres_connection_factory = PostgresConnectionFactory
        return PostgresGameDAO(postgres_connection_factory, orm_mapper)