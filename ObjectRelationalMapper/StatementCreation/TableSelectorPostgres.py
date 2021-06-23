from typing import Type
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from ObjectRelationalMapper.StatementCreation.StatementCreatorBase import StatementCreatorBase


class TableSelectorPostgres(StatementCreatorBase):
    def create(self, ORMObjectClass: Type[ORMAbstractBase]):
        return f"SELECT *\nFROM {ORMObjectClass.get_table_name()};"