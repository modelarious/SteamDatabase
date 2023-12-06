from ObjectRelationalMapper.StatementCreation.TableCreatorPostgres import (
    TableCreatorPostgres,
)
from ObjectRelationalMapper.StatementCreation.TableInserterPostgres import (
    TableInserterPostgres,
)
from ObjectRelationalMapper.StatementCreation.TableSelectorPostgres import (
    TableSelectorPostgres,
)
from ObjectRelationalMapper.StatementCreation.StatementCreationFacadePostgres import (
    StatementCreationFacadePostgres,
)


class StatementCreationFacadePostgresFactory:
    def create(self) -> StatementCreationFacadePostgres:
        table_creator = TableCreatorPostgres()
        table_inserter = TableInserterPostgres()
        table_select = TableSelectorPostgres()
        orm_mapper = StatementCreationFacadePostgres(
            table_creator, table_inserter, table_select
        )
        return orm_mapper
