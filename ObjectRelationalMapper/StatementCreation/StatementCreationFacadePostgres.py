from typing import Type
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from dataclasses import dataclass

from ObjectRelationalMapper.StatementCreation.TableCreatorPostgres import TableCreatorPostgres
from ObjectRelationalMapper.StatementCreation.TableInserterPostgres import TableInserterPostgres
from ObjectRelationalMapper.StatementCreation.TableSelectorPostgres import TableSelectorPostgres

@dataclass
class StatementCreationFacadePostgres:
    table_creator: TableCreatorPostgres
    table_inserter: TableInserterPostgres
    table_selector: TableSelectorPostgres
    
    def create_table_statement(self, ORMObjectClass: Type[ORMAbstractBase]) -> str:
        return self.table_creator.create(ORMObjectClass)
    
    def get_insert_data_statement(self, ORMObjectClass: Type[ORMAbstractBase]):
        return self.table_inserter.create(ORMObjectClass)
    
    def get_select_statement(self, ORMObjectClass: Type[ORMAbstractBase]):
        return self.table_selector.create(ORMObjectClass)