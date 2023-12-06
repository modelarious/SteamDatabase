from typing import Dict, Type, get_type_hints
from ObjectRelationalMapper.ORMMappedObjects.ORMAbstractBase import ORMAbstractBase
from ObjectRelationalMapper.StatementCreation.StatementCreatorBase import (
    StatementCreatorBase,
)


python_to_postrgres_type_map = {str: "VARCHAR ( 50000 )", int: "int", bool: "boolean"}


# CREATE TABLE IF NOT EXISTS AppDetail (
#   steam_id int UNIQUE NOT NULL,
#   detailed_description VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   about_the_game VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   short_description VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   header_image_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   metacritic_score int NOT NULL,
#   controller_support boolean NOT NULL,
#   background_image_url VARCHAR ( 1000 ) UNIQUE NOT NULL,
#   FOREIGN KEY (steam_id) REFERENCES Games(steam_id),
#   PRIMARY KEY (steam_id)
# );
# no user input here - no need to worry about injection attacks
class TableCreatorPostgres(StatementCreatorBase):
    def create(self, ORMObjectClass: Type[ORMAbstractBase]) -> str:
        return self._get_create_table_statement(
            get_type_hints(ORMObjectClass), ORMObjectClass
        )

    def _get_create_table_statement(
        self,
        orm_column_title_name_to_type_map: Dict[str, type],
        ORMObjectClass: Type[ORMAbstractBase],
    ):
        statement = f"CREATE TABLE IF NOT EXISTS {ORMObjectClass.get_table_name()} (\n"
        statement += self._get_columns(
            orm_column_title_name_to_type_map, ORMObjectClass
        )
        statement += self._get_foreign_key_mappings(ORMObjectClass)
        statement += self._get_primary_key_mapping(ORMObjectClass)

        # correct the case where we have a dangling comma.
        # this would happen if we had a foreign key and no primary key
        if statement[-2] == ",":
            # remove dangling comma
            statement = statement[:-2] + statement[-1:]

        statement += ");\n"
        return statement

    def _get_columns(
        self, title_to_type_map: Dict[str, type], ORMObjectClass: Type[ORMAbstractBase]
    ) -> str:
        statement_addition = ""
        for column_title, python_type in title_to_type_map.items():
            try:
                postgres_type = python_to_postrgres_type_map[python_type]
            except KeyError as e:
                raise KeyError(
                    f"Had issue with column {column_title} for class {ORMObjectClass}\n {e}"
                )
            unique_value = (
                " UNIQUE"
                if column_title not in ORMObjectClass.get_non_unique_mappings()
                else ""
            )
            null_value = (
                " NOT NULL"
                if column_title not in ORMObjectClass.get_nullable_fields()
                else ""
            )
            statement_addition += (
                f"\t{column_title} {postgres_type}{unique_value}{null_value},\n"
            )
        return statement_addition

    def _get_foreign_key_mappings(self, ORMObjectClass: Type[ORMAbstractBase]) -> str:
        statement_addition = ""
        for (
            column_title,
            foreign_table,
        ) in ORMObjectClass.get_foreign_key_mappings().items():
            statement_addition += f"\tFOREIGN KEY ({column_title}) REFERENCES {foreign_table}({column_title}),\n"
        return statement_addition

    def _get_primary_key_mapping(self, ORMObjectClass: Type[ORMAbstractBase]) -> str:
        primary_key = ORMObjectClass.get_primary_key()
        if primary_key:
            return f"\tPRIMARY KEY ({primary_key})\n"
        return ""
