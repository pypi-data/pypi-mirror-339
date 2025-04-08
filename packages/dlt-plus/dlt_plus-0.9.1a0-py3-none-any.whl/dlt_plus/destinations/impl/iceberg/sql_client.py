import duckdb

from urllib.parse import urlparse

from dlt.common import logger
from dlt.common.destination.typing import PreparedTableSchema

from dlt.destinations.sql_client import raise_database_error
from dlt.destinations.impl.filesystem.sql_client import WithTableScanners
from dlt.destinations.impl.duckdb.configuration import DuckDbCredentials
from dlt.sources.credentials import (
    AwsCredentials,
    AzureCredentials,
    AzureServicePrincipalCredentials,
)

from dlt_plus.destinations.impl.iceberg.iceberg import PyIcebergJobClient, IcebergTable


class IcebergSqlClient(WithTableScanners):
    def __init__(
        self,
        remote_client: PyIcebergJobClient,
        dataset_name: str = None,
        cache_db: DuckDbCredentials = None,
        persist_secrets: bool = False,
    ) -> None:
        super().__init__(remote_client, dataset_name, cache_db, persist_secrets)
        self.remote_client: PyIcebergJobClient = remote_client
        self._catalog = remote_client._catalog
        self.filesystem_config = remote_client.config.filesystem
        self.use_filesystem_auth = (
            self.filesystem_config is not None
            and self.filesystem_config.credentials is not None
            and self.filesystem_config.credentials.is_resolved()
        )

    def can_create_view(self, table_schema: PreparedTableSchema) -> bool:
        return True

    def should_replace_view(self, view_name: str, table_schema: PreparedTableSchema) -> bool:
        # here we could make views refresh ie. after some time
        return self.use_filesystem_auth and self.filesystem_config.protocol == "abfss"

    @raise_database_error
    def create_view(self, view_name: str, table_schema: PreparedTableSchema) -> None:
        # get snapshot and io from catalog
        iceberg_table = self.remote_client.load_open_table("iceberg", table_schema["name"])
        last_metadata_file = iceberg_table.metadata_location
        table_location = iceberg_table.location()

        if not self.use_filesystem_auth:
            # TODO: vended credentials may
            #  have expiration time so it makes sense to store expiry time and do
            #  should_replace_view
            if self._register_file_io_secret(iceberg_table):
                logger.info(
                    f"Successfully registered duckdb secret for table location {table_location}"
                )
            elif self._register_filesystem(iceberg_table):
                logger.warning(
                    "Catalog vended credentials in a form that cannot be persisted as duckdb "
                    "secret. Transformation engine like dbt that connects to duckdb separately "
                    "won't be able to use this credentials. Define `filesystem` config field or "
                    "use STS credentials vending on s3. "
                    f"The requested table location was {table_location}"
                )
                logger.info(
                    "Successfully registered fsspec filesystem for table location "
                    f"{iceberg_table.location()}"
                )
            else:
                logger.warning(
                    "Pyiceberg instantiated Arrow filesystem which cannot be used with duckdb. "
                    f"The requested table location was {table_location}. "
                    "Creating views will most probably fail."
                )
        else:
            logger.info(
                "Credentials in `filesystem` configuration were used for secrets for table "
                f"location {table_location}"
            )

        if ".gz." in last_metadata_file:
            compression = ", metadata_compression_codec = 'gzip'"
        else:
            compression = ""

        from_statement = (
            f"iceberg_scan('{last_metadata_file}' {compression}, skip_schema_inference=true)"
        )

        # create view
        view_name = self.make_qualified_table_name(view_name)
        create_table_sql_base = (
            f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM {from_statement}"
        )
        self._conn.execute(create_table_sql_base)

    def _register_file_io_secret(self, iceberg_table: IcebergTable) -> bool:
        """Register FileIO as duckdb secret if possible"""
        # check credential types that we can convert into duckdb secrets
        aws_credentials = AwsCredentials.from_pyiceberg_fileio_config(iceberg_table.config)
        if aws_credentials.is_resolved():
            self.create_secret(
                iceberg_table.location(),
                aws_credentials,
            )
            return True
        azure_credentials = AzureCredentials.from_pyiceberg_fileio_config(iceberg_table.config)
        if azure_credentials.is_resolved() and azure_credentials.azure_storage_account_key:
            self.create_secret(
                iceberg_table.location(),
                azure_credentials,
            )
            return True
        azure_tenant_credentials = AzureServicePrincipalCredentials.from_pyiceberg_fileio_config(
            iceberg_table.config
        )
        if azure_tenant_credentials.is_resolved():
            self.create_secret(
                iceberg_table.location(),
                azure_tenant_credentials,
            )
            return True
        # none of the gcp credentials can be converted from file io to duckdb

        return False

    def _register_filesystem(self, iceberg_table: IcebergTable) -> bool:
        """Tries to register FileIO in `iceberg_table` as fsspec filesystem in duckdb"""
        from pyiceberg.io.fsspec import FsspecFileIO

        uri = urlparse(iceberg_table.metadata.location)

        if isinstance(iceberg_table.io, FsspecFileIO):
            fs = iceberg_table.io.get_fs(uri.scheme)
            self._conn.register_filesystem(fs)
            if fs.protocol != uri.scheme:
                fs.protocol = uri.scheme
            self._conn.register_filesystem(fs)
            return True
        return False

    def open_connection(self) -> duckdb.DuckDBPyConnection:
        first_connection = self.credentials.never_borrowed
        super().open_connection()

        if first_connection and self.filesystem_config and self.filesystem_config.is_resolved():
            # NOTE: hopefully duckdb will implement REST catalog connection working with all
            #   main bucket. see create_view to see how we deal with vended credentials.
            #   Current best option (performance) is to pass credentials via filesystem or use STS
            if self.filesystem_config.protocol != "file":
                # create single authentication for the whole client if filesystem is specified
                self.create_secret(
                    self.filesystem_config.bucket_url, self.filesystem_config.credentials
                )

        return self._conn
