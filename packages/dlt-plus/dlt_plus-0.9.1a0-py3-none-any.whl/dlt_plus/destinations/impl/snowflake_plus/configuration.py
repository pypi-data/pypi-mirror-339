from typing import Optional

from dlt.common.configuration import configspec

from dlt.destinations.impl.snowflake.configuration import SnowflakeClientConfiguration


@configspec
class SnowflakePlusClientConfiguration(SnowflakeClientConfiguration):
    external_volume: str = None
    catalog: str = "SNOWFLAKE"
    base_location: Optional[str] = None
    catalog_sync: Optional[str] = None
    force_iceberg: Optional[bool] = None
