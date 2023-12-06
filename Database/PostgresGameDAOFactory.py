from ObjectRelationalMapper.Helpers.GameFromORMFactory import GameFromORMFactory
from ObjectRelationalMapper.ORMMapper import ORMMapper
from ObjectRelationalMapper.StatementCreation.StatementCreationFacadePostgresFactory import (
    StatementCreationFacadePostgresFactory,
)
from Database.PostgresGameDAO import PostgresGameDAO
from Database.PostgresConnectionFactory import PostgresConnectionFactory


class PostgresGameDAOFactory:
    def createGameDAO(self):
        statement_creation_facade = StatementCreationFacadePostgresFactory()
        game_from_orm_factory = GameFromORMFactory()
        orm_mapper = ORMMapper(
            statement_creation_facade.create(), game_from_orm_factory
        )
        postgres_connection_factory = PostgresConnectionFactory()
        return PostgresGameDAO(postgres_connection_factory, orm_mapper)
