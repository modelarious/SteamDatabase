from dataclasses import fields
from typing import Type
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from ObjectRelationalMapper.StatementCreation.StatementCreatorBase import (
    StatementCreatorBase,
)


class TableInserterPostgres(StatementCreatorBase):
    def create(self, ORMObjectClass: Type[ORMAbstractBase]):
        data_fields = fields(ORMObjectClass)
        data_field_names = [data_field.name for data_field in data_fields]
        placeholders = ["%s"] * len(data_fields)
        seper = ",\n\t"
        statement = f"INSERT INTO {ORMObjectClass.get_table_name()} (\n\t{seper.join(data_field_names)}\n)\nVALUES ({','.join(placeholders)});"
        return statement
