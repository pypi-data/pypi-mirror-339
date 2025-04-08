from typing import Sequence, List, cast

from dlt.common.schema import TColumnSchema
from dlt.common.destination.client import PreparedTableSchema
from dlt.destinations.impl.snowflake.snowflake import SnowflakeClient
from dlt_plus.destinations.impl.snowflake_plus.configuration import SnowflakePlusClientConfiguration


class SnowflakePlusClient(SnowflakeClient):
    def _is_iceberg_table(self, table: PreparedTableSchema) -> bool:
        return table.get("table_format") == "iceberg"

    def _make_create_table(self, qualified_name: str, table: PreparedTableSchema) -> str:
        if not self._is_iceberg_table(table):
            return super()._make_create_table(qualified_name, table)

        not_exists_clause = " "
        if (
            table["name"] in self.schema.dlt_table_names()
            and self.capabilities.supports_create_table_if_not_exists
        ):
            not_exists_clause = " IF NOT EXISTS "
        return f"CREATE ICEBERG TABLE{not_exists_clause}{qualified_name}"

    def _get_table_update_sql(
        self,
        table_name: str,
        new_columns: Sequence[TColumnSchema],
        generate_alter: bool,
        separate_alters: bool = False,
    ) -> List[str]:
        table = self.prepare_load_table(table_name)

        if not self._is_iceberg_table(table):
            return super()._get_table_update_sql(table_name, new_columns, generate_alter)

        if not generate_alter:
            sql = super()._get_table_update_sql(table_name, new_columns, generate_alter)

            config = cast(SnowflakePlusClientConfiguration, self.config)

            iceberg_sql = []
            iceberg_sql.append(f"CATALOG = '{config.catalog}'")
            iceberg_sql.append(f"EXTERNAL_VOLUME = '{config.external_volume}'")

            dataset_name = self.sql_client.dataset_name
            base_location = (
                config.base_location
                if config.base_location is not None
                else f"{dataset_name}/{table_name}"
            )
            iceberg_sql.append(f"BASE_LOCATION = '{base_location}'")

            if config.catalog_sync:
                iceberg_sql.append(f"CATALOG_SYNC = '{config.catalog_sync}'")

            sql[0] = sql[0] + "\n" + "\n".join(iceberg_sql)
        else:
            sql = []
            qualified_name = self.sql_client.make_qualified_table_name(table_name)
            add_column_statements = self._make_add_column_sql(new_columns, table)
            column_sql = ",\n".join(add_column_statements)
            sql.append(f"ALTER ICEBERG TABLE {qualified_name}\n {column_sql}")
            constraints_sql = self._get_constraints_sql(table_name, new_columns, generate_alter)
            if constraints_sql:
                sql.append(constraints_sql)

        return sql
