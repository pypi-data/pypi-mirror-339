import typing as t

from dlt.common.schema.typing import TColumnSchema
from dlt.common.configuration import resolve_configuration, known_sections
from dlt.common.destination import DestinationCapabilitiesContext
from dlt.common.destination.reference import TDestinationConfig
from dlt.common.destination.typing import PreparedTableSchema
from dlt.common.exceptions import TerminalValueError
from dlt.common.normalizers.naming import NamingConvention

from dlt.destinations.impl.snowflake.factory import snowflake, SnowflakeTypeMapper
from dlt.destinations.impl.snowflake.configuration import SnowflakeClientConfiguration
from dlt_plus.destinations.impl.snowflake_plus.configuration import SnowflakePlusClientConfiguration

if t.TYPE_CHECKING:
    from dlt_plus.destinations.impl.snowflake_plus.snowflake_plus import SnowflakePlusClient


class SnowflakePlusTypeMapper(SnowflakeTypeMapper):
    dbt_to_sct = {
        # Snowflake
        "varchar": "text",
        "float": "double",
        "boolean": "bool",
        "date": "date",
        "timestamp_tz": "timestamp",
        "binary": "binary",
        "variant": "json",
        "time": "time",
        # Iceberg
        "double": "double",
        "timestamp": "timestamp",
        "timestamptz": "timestamp",
        "decimal": "decimal",
        "tinyint": "bigint",
        "smallint": "bigint",
        "int": "bigint",
        "long": "bigint",
        "string": "text",
    }

    sct_to_iceberg_unbound_dbt = {
        "json": "string",
        "text": "string",
        "double": "double",
        "bool": "boolean",
        "date": "date",
        "timestamp": "timestamp",
        "bigint": "bigint",
        "binary": "binary",
        "time": "string",
    }

    def to_destination_type(self, column: TColumnSchema, table: PreparedTableSchema) -> str:
        if table.get("table_format") == "iceberg":
            if column["data_type"] == "double":
                return "double"
            elif column["data_type"] == "text":
                return "string"
            elif column["data_type"] == "json":
                return "string"
            elif column["data_type"] in ("decimal", "wei"):
                precision_tup = self.precision_tuple_or_default(column["data_type"], column)
                if precision_tup:
                    return "decimal(%i,%i)" % precision_tup
                else:
                    return "decimal"
            else:
                return super().to_destination_type(column, table)
        else:
            return super().to_destination_type(column, table)

    def to_db_datetime_type(
        self,
        column: TColumnSchema,
        table: PreparedTableSchema = None,
    ) -> str:
        if table.get("table_format") == "iceberg":
            return "timestamp"
        else:
            return super().to_db_datetime_type(column, table)

    def to_db_time_type(self, column: TColumnSchema, table: PreparedTableSchema = None) -> str:
        if table.get("table_format") == "iceberg":
            return "time"
        else:
            return super().to_db_time_type(column, table)

    def to_db_integer_type(self, column: TColumnSchema, table: PreparedTableSchema = None) -> str:
        if table.get("table_format") != "iceberg":
            return super().to_db_integer_type(column, table)

        precision = column.get("precision")
        if precision is None:
            return "long"
        if precision <= 8:
            return "int"
        elif precision <= 16:
            return "int"
        elif precision <= 32:
            return "int"
        elif precision <= 64:
            return "long"
        raise TerminalValueError(
            f"bigint with {precision} bits precision cannot be mapped into an Iceberg integer type"
        )


class snowflake_plus(snowflake):
    spec = SnowflakePlusClientConfiguration

    CONFIG_SECTION = "snowflake"

    def _raw_capabilities(self) -> DestinationCapabilitiesContext:
        caps = super()._raw_capabilities()
        caps.type_mapper = SnowflakePlusTypeMapper
        return caps

    @property
    def client_class(self) -> t.Type["SnowflakePlusClient"]:
        from dlt_plus.destinations.impl.snowflake_plus.snowflake_plus import SnowflakePlusClient

        return SnowflakePlusClient

    @classmethod
    def adjust_capabilities(
        cls,
        caps: DestinationCapabilitiesContext,
        config: SnowflakeClientConfiguration,
        naming: t.Optional[NamingConvention],
    ) -> DestinationCapabilitiesContext:
        config = t.cast(SnowflakePlusClientConfiguration, config)
        if config.force_iceberg:
            caps.preferred_table_format = "iceberg"

        return super().adjust_capabilities(caps, config, naming)

    def configuration(
        self, initial_config: TDestinationConfig, accept_partial: bool = False
    ) -> t.Union[TDestinationConfig, SnowflakePlusClientConfiguration]:
        config = resolve_configuration(
            initial_config or self.spec(),
            sections=(known_sections.DESTINATION, self.CONFIG_SECTION),
            explicit_value=self.config_params,
            accept_partial=accept_partial,
        )
        return config


snowflake_plus.register()
