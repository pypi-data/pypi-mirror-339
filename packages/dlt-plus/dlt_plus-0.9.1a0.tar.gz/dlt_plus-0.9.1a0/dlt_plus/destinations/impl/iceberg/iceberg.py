import posixpath
from functools import wraps
from types import TracebackType
from typing import (
    List,
    Type,
    Iterable,
    Optional,
    Sequence,
    Any,
    Dict,
)

from dlt.common import json, pendulum, logger
from dlt.common.exceptions import MissingDependencyException
from dlt.common.libs.pyarrow import columns_to_arrow, pyarrow as pa
from dlt.common.schema import Schema
from dlt.common.schema.exceptions import SchemaCorruptedException
from dlt.common.schema.typing import TSchemaTables, TTableSchema, TWriteDisposition, TTableFormat
from dlt.common.schema.utils import get_columns_names_with_prop, is_nested_table
from dlt.common.storages import FileStorage, fsspec_from_config
from dlt.common.storages.load_package import LoadJobInfo, ParsedLoadJobFileName
from dlt.common.destination.capabilities import DestinationCapabilitiesContext
from dlt.common.destination.exceptions import (
    DestinationTransientException,
    DestinationTerminalException,
    OpenTableCatalogNotSupported,
    OpenTableFormatNotSupported,
)
from dlt.common.destination.client import (
    FollowupJobRequest,
    PreparedTableSchema,
    RunnableLoadJob,
    JobClientBase,
    WithStateSync,
    SupportsOpenTables,
    StorageSchemaInfo,
    StateInfo,
    LoadJob,
)
from dlt.destinations import duckdb as duckdb_destination
from dlt.common.destination.exceptions import DestinationUndefinedEntity
from dlt.common.typing import TFun

from dlt.destinations.job_impl import (
    ReferenceFollowupJobRequest,
    FinalizedLoadJobWithFollowupJobs,
)
from dlt.destinations.sql_client import WithSqlClient, SqlClientBase
from dlt.destinations.sql_jobs import SqlMergeFollowupJob


from dlt_plus import version
from dlt_plus.destinations.utils import get_dedup_sort_order_by_sql
from dlt_plus.destinations.impl.iceberg.configuration import (
    IcebergClientConfiguration,
    IcebergRESTCatalogCredentials,
    IcebergSqlCatalogCredentials,
)

try:
    from dlt.common.libs.pyiceberg import (
        ensure_iceberg_compatible_arrow_data,
        ensure_iceberg_compatible_arrow_schema,
        write_iceberg_table,
        get_sql_catalog,
        register_table,
        IcebergTable,
        IcebergCatalog,
    )
    from pyiceberg.table import ALWAYS_TRUE
    from pyiceberg.exceptions import NoSuchTableError, NoSuchViewError, NoSuchNamespaceError
    import duckdb
except ImportError:
    raise MissingDependencyException(
        "dlt+ iceberg destination",
        [f"{version.PKG_NAME}[iceberg]"],
        "iceberg needs pyiceberg, pyarrow, sqlalchemy and duckdb in order to work",
    )


def pyiceberg_error(f: TFun) -> TFun:
    @wraps(f)
    def _wrap(self: JobClientBase, *args: Any, **kwargs: Any) -> Any:
        try:
            return f(self, *args, **kwargs)
        except (
            NoSuchTableError,
            NoSuchViewError,
            NoSuchNamespaceError,
        ) as status_ex:
            raise DestinationUndefinedEntity(status_ex) from status_ex
        except Exception as e:
            raise DestinationTransientException(e) from e

    return _wrap  # type: ignore[return-value]


class IcebergLoadJob(RunnableLoadJob):
    def __init__(
        self, file_path: str, catalog: IcebergCatalog, table: PreparedTableSchema, table_id: str
    ):
        super().__init__(file_path)
        self._catalog: IcebergCatalog = catalog
        self._table: PreparedTableSchema = table
        self._file_paths = ReferenceFollowupJobRequest.resolve_references(self._file_path)
        self._table_id = table_id

    @pyiceberg_error
    def run(self) -> None:
        # load table
        iceberg_table = self._catalog.load_table(self._table_id)
        if self._table["write_disposition"] == "merge":
            strategy = self._table["x-merge-strategy"]  # type: ignore[typeddict-item]
            if strategy == "delete-insert":
                self._run_delete_insert(iceberg_table)
            else:
                pass
                # TODO: reuse code from delete-insert to do hard-delete
                # assume upsert
                # if "parent" in schema:
                #     unique_column = get_first_column_name_with_prop(schema, "unique")
                #     predicate = f"target.{unique_column} = source.{unique_column}"
                # else:
                #     primary_keys = get_columns_names_with_prop(schema, "primary_key")
                #     predicate = " AND ".join([f"target.{c} = source.{c}" for c in primary_keys])

                # partition_by = get_columns_names_with_prop(schema, "partition")
                # qry = (
                #     table.merge(
                #         source=ensure_delta_compatible_arrow_data(data, partition_by),
                #         predicate=predicate,
                #         source_alias="source",
                #         target_alias="target",
                #     )
                #     .when_matched_update_all()
                #     .when_not_matched_insert_all()
                # )

                # qry.execute()
            pass
        else:
            from dlt.common.libs.pyarrow import pyarrow

            write_iceberg_table(
                table=iceberg_table,
                data=pyarrow.dataset.dataset(self._file_paths).to_table(),
                write_disposition="append",
            )

    def _run_delete_insert(self, iceberg_table: Any) -> None:
        from dlt.common.libs.pyarrow import pyarrow
        from pyiceberg.expressions import In, Or

        def get_delete_filter(primary_keys: List[str], merge_keys: List[str]) -> Any:
            # we know we have one primary key and/or one merge key, because we have already
            # checked this in `verify_schema` method
            assert primary_keys or merge_keys
            assert len(primary_keys) <= 1
            assert len(merge_keys) <= 1
            if primary_keys and merge_keys:
                primary_key, merge_key = primary_keys[0], merge_keys[0]
                key_vals = arrow_table.select([primary_key, merge_key]).to_pydict()
                return Or(
                    In(primary_key, key_vals[primary_key]),
                    In(merge_key, key_vals[merge_key]),
                )
            elif primary_keys:
                primary_key = primary_keys[0]
                key_vals = arrow_table.select([primary_key]).to_pydict()
                return In(primary_key, key_vals[primary_key])
            elif merge_keys:
                merge_key = merge_keys[0]
                key_vals = arrow_table.select([merge_key]).to_pydict()
                return In(merge_key, key_vals[merge_key])

        arrow_table = pyarrow.dataset.dataset(self._file_paths).to_table()

        # get key from schema and deduplicate if primary key
        if primary_keys := get_columns_names_with_prop(self._load_table, "primary_key"):
            # deduplicate
            order_by = get_dedup_sort_order_by_sql(self._load_table)
            con = duckdb.connect()
            arrow_table = (
                con.sql(f"""
                FROM arrow_table
                QUALIFY row_number() OVER (PARTITION BY {primary_keys[0]} ORDER BY {order_by}) = 1;
            """)
                .arrow()
                .cast(arrow_table.schema)
            )

        # prepare deletes
        merge_keys = get_columns_names_with_prop(self._load_table, "merge_key")
        delete_filter = get_delete_filter(primary_keys, merge_keys)

        # prepare inserts

        # remove hard-deleted records
        caps = duckdb_destination()._raw_capabilities()
        hard_delete_col, not_deleted_cond = SqlMergeFollowupJob._get_hard_delete_col_and_cond(
            self._load_table,
            caps.escape_identifier,
            caps.escape_literal,
            invert=True,
        )
        if hard_delete_col is not None:
            con = duckdb.connect()
            arrow_table = (
                con.execute(f"FROM arrow_table WHERE {not_deleted_cond};")
                .arrow()
                .cast(arrow_table.schema)
            )

        # execute deletes and inserts in single transaction
        with iceberg_table.transaction() as txn:
            txn.delete(delete_filter)
            txn.append(ensure_iceberg_compatible_arrow_data(arrow_table))


class PyIcebergJobClient(JobClientBase, WithStateSync, WithSqlClient, SupportsOpenTables):
    def __init__(
        self,
        schema: Schema,
        config: IcebergClientConfiguration,
        capabilities: DestinationCapabilitiesContext,
    ):
        super().__init__(schema, config, capabilities)
        self.config: IcebergClientConfiguration = config
        self.dataset_name = config.normalize_dataset_name(schema)
        # TODO: pass catalog name via config. this will allow pyiceberg yaml to be used
        #  to configure catalogs
        self._catalog = self._create_catalog("default")
        self._sql_client: SqlClientBase[Any] = None

    def initialize_storage(self, truncate_tables: Optional[Iterable[str]] = None) -> None:
        """Prepares storage to be used ie. creates database schema or file system folder. Truncates"
        requested tables.
        """
        if not self.is_storage_initialized():
            self._catalog.create_namespace(self.dataset_name)
        if truncate_tables:
            for table_name in truncate_tables:
                table_identifier = self.make_qualified_table_name(table_name)
                if self._catalog.table_exists(table_identifier):
                    self.write_records([], table_name=table_name, write_disposition="replace")

    def is_storage_initialized(self) -> bool:
        """Returns if storage is ready to be read/written."""
        try:
            self._catalog.load_namespace_properties(self.dataset_name)
            return True
        except NoSuchNamespaceError:
            return False

    def drop_storage(self) -> None:
        """Brings storage back into not initialized state. Typically data in storage is
        destroyed.
        """
        # purges all known (in schema) tables in the namespace
        for table_name in self.schema.tables.keys():
            table_id = self.make_qualified_table_name(table_name)
            if self._catalog.table_exists(table_id):
                self._catalog.purge_table(table_id)
        # purge remaining tables
        for table_ident in self._catalog.list_tables(self.dataset_name):
            self._catalog.purge_table(table_ident)
        # remove namespace (will raise if still containing tables)
        self._catalog.drop_namespace(self.dataset_name)

    def update_stored_schema(
        self,
        only_tables: Iterable[str] = None,
        expected_update: TSchemaTables = None,
    ) -> Optional[TSchemaTables]:
        applied_update: TSchemaTables = {}
        for table_name in only_tables or self.schema.tables.keys():
            applied_update[table_name] = self._create_or_evolve_table(table_name)
        self._update_schema_in_storage()
        return expected_update

    def verify_schema(
        self, only_tables: Iterable[str] = None, new_jobs: Iterable[ParsedLoadJobFileName] = None
    ) -> List[PreparedTableSchema]:
        tables = super().verify_schema(only_tables, new_jobs)
        for table in tables:
            if (
                table.get("table_format") == "iceberg"
                and table["write_disposition"] == "merge"
                and table["x-merge-strategy"] == "delete-insert"  # type: ignore[typeddict-item]
            ):
                primary_key = get_columns_names_with_prop(table, "primary_key")
                merge_key = get_columns_names_with_prop(table, "merge_key")
                for key in [primary_key, merge_key]:
                    key_type = "primary_key" if key == primary_key else "merge_key"
                    if len(key) > 1:
                        raise SchemaCorruptedException(
                            self.schema.name,
                            f"Found multiple `{key_type}` columns for table"
                            f""" "{table["name"]}" while only one is allowed when using `iceberg`"""
                            " table format and `delete-insert` merge strategy:"
                            f""" {", ".join([f'"{k}"' for k in key])}.""",
                        )
                if is_nested_table(table):
                    raise SchemaCorruptedException(
                        self.schema.name,
                        f'Found nested table "{table["name"]}". Nested tables are not supported'
                        " when using `iceberg` table format and `delete-insert` merge strategy.",
                    )

        return tables

    # def prepare_load_table(self, table_name: str) -> PreparedTableSchema:
    #     return prepare_load_table(
    #         self.schema.tables, self.schema.get_table(table_name), self.capabilities
    #     )

    def create_load_job(
        self, table: PreparedTableSchema, file_path: str, load_id: str, restore: bool = False
    ) -> LoadJob:
        """Creates a load job for a particular `table` with content in `file_path`.
        Table is already prepared to be loaded.
        """
        # a reference job for a delta table indicates a table chain followup job
        table_format = table.get("table_format")
        assert table_format == "iceberg", f"Only iceberg table format supported, got {table_format}"
        # TODO: execute append/replace jobs immediately, do not chain. also upsert
        # (at least for now)
        #   does not need to be chained
        if ReferenceFollowupJobRequest.is_reference_job(file_path):
            with self:
                return IcebergLoadJob(
                    file_path, self._catalog, table, self.make_qualified_table_name(table["name"])
                )

        # otherwise just continue to collect jobs and to create a full table chain
        return FinalizedLoadJobWithFollowupJobs(file_path)

    # def should_truncate_table_before_load(self, table_name: str) -> bool:
    #     return self.prepare_load_table(table_name)["write_disposition"] == "replace"

    def create_table_chain_completed_followup_jobs(
        self,
        table_chain: Sequence[PreparedTableSchema],
        completed_table_chain_jobs: Optional[Sequence[LoadJobInfo]] = None,
    ) -> List[FollowupJobRequest]:
        """Creates a list of followup jobs that should be executed after a table chain is
        completed. Tables are already prepared to be loaded.
        """
        assert completed_table_chain_jobs is not None
        jobs = super().create_table_chain_completed_followup_jobs(
            table_chain, completed_table_chain_jobs
        )
        for table in table_chain:
            table_job_paths = [
                job.file_path
                for job in completed_table_chain_jobs
                if job.job_file_info.table_name == table["name"]
            ]
            if table_job_paths:
                file_name = FileStorage.get_file_name_from_file_path(table_job_paths[0])
                jobs.append(ReferenceFollowupJobRequest(file_name, table_job_paths))

        return jobs

    def _update_schema_in_storage(self) -> None:
        records = [
            {
                self.schema.naming.normalize_identifier("version"): self.schema.version,
                self.schema.naming.normalize_identifier(
                    "engine_version"
                ): self.schema.ENGINE_VERSION,
                self.schema.naming.normalize_identifier("inserted_at"): pendulum.now(),
                self.schema.naming.normalize_identifier("schema_name"): self.schema.name,
                self.schema.naming.normalize_identifier(
                    "version_hash"
                ): self.schema.stored_version_hash,
                self.schema.naming.normalize_identifier("schema"): json.dumps(
                    self.schema.to_dict()
                ),
            }
        ]
        self.write_records(records, table_name=self.schema.version_table_name)

    def complete_load(self, load_id: str) -> None:
        records = [
            {
                self.schema.naming.normalize_identifier("load_id"): load_id,
                self.schema.naming.normalize_identifier("schema_name"): self.schema.name,
                self.schema.naming.normalize_identifier("status"): 0,
                self.schema.naming.normalize_identifier("inserted_at"): pendulum.now(),
                self.schema.naming.normalize_identifier("schema_version_hash"): None,
            }
        ]
        self.write_records(
            records,
            table_name=self.schema.loads_table_name,
        )

    def __enter__(self) -> "JobClientBase":
        return self

    def __exit__(
        self, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType
    ) -> None:
        pass

    @property
    def sql_client_class(self) -> Type[SqlClientBase[Any]]:
        from dlt_plus.destinations.impl.iceberg.sql_client import IcebergSqlClient

        return IcebergSqlClient

    @property
    def sql_client(self) -> SqlClientBase[Any]:
        # we use an inner import here, since the sql client depends on duckdb and will
        # only be used for read access on data, some users will not need the dependency
        from dlt_plus.destinations.impl.iceberg.sql_client import IcebergSqlClient

        if not self._sql_client:
            self._sql_client = IcebergSqlClient(self, dataset_name=self.dataset_name)
        return self._sql_client

    # state sync
    @pyiceberg_error
    def get_stored_schema(self, schema_name: str = None) -> Optional[StorageSchemaInfo]:
        p_version_hash = self.schema.naming.normalize_identifier("version_hash")
        p_inserted_at = self.schema.naming.normalize_identifier("inserted_at")
        p_schema_name = self.schema.naming.normalize_identifier("schema_name")
        p_version = self.schema.naming.normalize_identifier("version")
        p_engine_version = self.schema.naming.normalize_identifier("engine_version")
        p_schema = self.schema.naming.normalize_identifier("schema")

        try:
            version_table = self.load_open_table("iceberg", self.schema.version_table_name)
            row_filter = f"{p_schema_name} = '{schema_name}'" if schema_name else None
            schemas_table: pa.Table = (
                version_table.scan(row_filter=row_filter or ALWAYS_TRUE)
                .to_arrow()
                .sort_by([(p_inserted_at, "descending")])
            )

            if schemas_table.num_rows == 0:
                return None

            most_recent_schema = schemas_table.take([0]).to_pylist()[0]

            return StorageSchemaInfo(
                version_hash=most_recent_schema[p_version_hash],
                schema_name=most_recent_schema[p_schema_name],
                version=most_recent_schema[p_version],
                engine_version=most_recent_schema[p_engine_version],
                inserted_at=most_recent_schema[p_inserted_at],
                schema=most_recent_schema[p_schema],
            )
        except NoSuchTableError:
            return None

    @pyiceberg_error
    def get_stored_schema_by_hash(self, version_hash: str) -> StorageSchemaInfo:
        """Retrieves newest schema from destination storage."""
        p_version_hash = self.schema.naming.normalize_identifier("version_hash")
        p_inserted_at = self.schema.naming.normalize_identifier("inserted_at")
        p_schema_name = self.schema.naming.normalize_identifier("schema_name")
        p_version = self.schema.naming.normalize_identifier("version")
        p_engine_version = self.schema.naming.normalize_identifier("engine_version")
        p_schema = self.schema.naming.normalize_identifier("schema")

        try:
            version_table = self.load_open_table("iceberg", self.schema.version_table_name)

            schemas_table: pa.Table = (
                (version_table.scan(row_filter=f'{p_version_hash} = "{version_hash}"'))
                .to_arrow()
                .sort_by([(p_inserted_at, "descending")])
            )

            if schemas_table.num_rows == 0:
                return None

            most_recent_schema = schemas_table.take([0]).to_pylist()[0]

            return StorageSchemaInfo(
                version_hash=most_recent_schema[p_version_hash],
                schema_name=most_recent_schema[p_schema_name],
                version=most_recent_schema[p_version],
                engine_version=most_recent_schema[p_engine_version],
                inserted_at=most_recent_schema[p_inserted_at],
                schema=most_recent_schema[p_schema],
            )
        except NoSuchTableError:
            return None

    @pyiceberg_error
    def get_stored_state(self, pipeline_name: str) -> Optional[StateInfo]:
        """Retrieves the latest completed state for a pipeline."""
        state_table_ = self.load_open_table("iceberg", self.schema.state_table_name)
        loads_table_ = self.load_open_table("iceberg", self.schema.loads_table_name)

        # normalize property names
        p_load_id = self.schema.naming.normalize_identifier("load_id")
        p_dlt_load_id = self.schema.naming.normalize_identifier(
            self.schema.data_item_normalizer.c_dlt_load_id  # type: ignore[attr-defined]
        )
        p_pipeline_name = self.schema.naming.normalize_identifier("pipeline_name")
        p_status = self.schema.naming.normalize_identifier("status")
        p_version = self.schema.naming.normalize_identifier("version")
        p_engine_version = self.schema.naming.normalize_identifier("engine_version")
        p_state = self.schema.naming.normalize_identifier("state")
        p_created_at = self.schema.naming.normalize_identifier("created_at")
        p_version_hash = self.schema.naming.normalize_identifier("version_hash")

        # Read the tables into memory as Arrow tables, with pushdown predicates,
        # so we pull as little
        # data into memory as possible.
        state_table = state_table_.scan(
            row_filter=f"{p_pipeline_name} = '{pipeline_name}'"
        ).to_arrow()
        loads_table = loads_table_.scan(row_filter=f"{p_status} = 0").to_arrow()

        # Join arrow tables in-memory.
        joined_table: pa.Table = state_table.join(
            loads_table, keys=p_dlt_load_id, right_keys=p_load_id, join_type="inner"
        ).sort_by([(p_dlt_load_id, "descending")])

        if joined_table.num_rows == 0:
            return None

        state = joined_table.take([0]).to_pylist()[0]
        return StateInfo(
            version=state[p_version],
            engine_version=state[p_engine_version],
            pipeline_name=state[p_pipeline_name],
            state=state[p_state],
            created_at=pendulum.instance(state[p_created_at]),
            version_hash=state[p_version_hash],
            _dlt_load_id=state[p_dlt_load_id],
        )

    @pyiceberg_error
    def write_records(
        self,
        records: List[Dict[str, Any]],
        table_name: str,
        write_disposition: TWriteDisposition = "append",
    ) -> None:
        table_schema = self.prepare_load_table(table_name)
        arrow_schema = columns_to_arrow(table_schema["columns"], self.capabilities)
        # Convert records to Arrow table
        arrays = {col: [record.get(col, None) for record in records] for col in arrow_schema.names}
        table_data = pa.Table.from_pydict(arrays, schema=arrow_schema)
        iceberg_table = self._catalog.load_table(self.make_qualified_table_name(table_name))

        write_iceberg_table(iceberg_table, table_data, write_disposition=write_disposition)

    def make_qualified_table_name(self, table_name: str) -> str:
        return f"{self.dataset_name}.{table_name}"

    def _create_catalog(self, catalog_name: str) -> IcebergCatalog:
        # TODO: move to the configuration?
        if isinstance(self.config.credentials, IcebergSqlCatalogCredentials):
            return get_sql_catalog(
                catalog_name,
                self.config.credentials.to_native_representation(),
                self.config.filesystem.credentials,
                self.config.credentials.properties,
            )
        elif isinstance(self.config.credentials, IcebergRESTCatalogCredentials):
            from pyiceberg.catalog.rest import RestCatalog

            rest_credentials = self.config.credentials
            properties = dict(self.config.credentials.properties or {})
            if self.config.credentials.headers:
                headers = {"header." + k: v for k, v in self.config.credentials.headers.items()}
                properties.update(headers)
            if self.config.credentials.warehouse:
                properties["warehouse"] = self.config.credentials.warehouse
            if self.config.credentials.credential:
                properties["credential"] = self.config.credentials.credential
            return RestCatalog(catalog_name, uri=rest_credentials.uri, **properties)
        else:
            raise NotImplementedError(
                f"Iceberg catalog of type {self.config.catalog_type} with credentials "
                f"{type(self.config.credentials)} is not yet implemented."
            )

    @pyiceberg_error
    def _create_or_evolve_table(
        self,
        table_name: str,
    ) -> TTableSchema:
        prepared_table = self.prepare_load_table(table_name)
        table_id = self.make_qualified_table_name(table_name)
        arrow_schema = columns_to_arrow(prepared_table["columns"], self.capabilities)
        partition_columns = get_columns_names_with_prop(prepared_table, "partition")
        iceberg_table = None
        try:
            iceberg_table = self.load_open_table("iceberg", table_name)
            # table was found or registered
            new_columns = set(prepared_table["columns"].keys()).difference(
                iceberg_table.schema().column_names
            )
            # evolve schema
            # TODO: we may want to set table properties here as well ie. current snapshot.
            # then you cannot skip like below
            if new_columns:
                with iceberg_table.update_schema() as update:
                    update.union_by_name(ensure_iceberg_compatible_arrow_schema(arrow_schema))
            prepared_table["columns"] = {
                k: v for k, v in prepared_table["columns"].items() if k in new_columns
            }
        except NoSuchTableError:
            # found no metadata; create new table
            location = self.get_open_table_location("iceberg", table_name)
            with self._catalog.create_table_transaction(
                table_id,
                schema=ensure_iceberg_compatible_arrow_schema(arrow_schema),
                location=location,
            ) as txn:
                # TODO: add adapter to set partitions on columns and iceberg properties
                with txn.update_spec() as update_spec:
                    for col in partition_columns:
                        update_spec.add_identity(col)
        return prepared_table

    def get_open_table_catalog(
        self, table_format: TTableFormat, catalog_name: str = None
    ) -> IcebergCatalog:
        if table_format != "iceberg":
            raise OpenTableCatalogNotSupported(table_format, "iceberg")
        return self._catalog

    def get_open_table_location(self, table_format: TTableFormat, table_name: str) -> str:
        """Computes table location without loading table from a catalog. This requires
        absolute `table_location_layout` or `bucket_url` defined in `config.filesystem`.
        """
        if table_format != "iceberg":
            raise OpenTableFormatNotSupported(table_format, table_name, "iceberg")
        location = self.config.table_location_layout()
        # if location is set try to add namespace and table name to it
        if location:
            location = location.format(dataset_name=self.dataset_name, table_name=table_name)
        # assert location is not None
        logger.info(
            f"will use location: {location or '<catalog controller>'} for table {table_name}"
        )
        return location

    def load_open_table(
        self, table_format: TTableFormat, table_name: str, **kwargs: Any
    ) -> IcebergTable:
        """Loads table with `table_name` from catalog. If table does not exist and configuration
        allows to register new tables ('register_new_tables'), `filesystem` configuration will
        be used to find the newest metadata and add this table to the catalog.
        Note: we do not return static pyiceberg table if table is not in the catalog.
        """
        if table_format != "iceberg":
            raise OpenTableFormatNotSupported(table_format, table_name, "iceberg")
        table_id = self.make_qualified_table_name(table_name)
        try:
            return self._catalog.load_table(table_id)
        except NoSuchTableError:
            # try to register existing table
            if self.config.capabilities.register_new_tables:
                if self.config.filesystem is None or not self.config.filesystem.is_resolved():
                    raise DestinationTerminalException(
                        "Cannot register table without filesystem configuration. dlt needs location"
                        " and access to table storage to look for the newest metadata file"
                    )
                # TODO: metadata location may also be present in the dlt schema ie.
                # x-loader/iceberg/metadata_location
                # TODO: use similar search as duckdb (hints.txt, glob with metadata)
                fs_client = fsspec_from_config(self.config.filesystem)[0]
                location = self.get_open_table_location("iceberg", table_name)
                if location:
                    metadata_location = posixpath.join(
                        location,
                        self.config.capabilities.table_metadata_layout,
                    )
                    if fs_client.exists(metadata_location):
                        logger.info(
                            f"Registering table {table_id} at metadata location {metadata_location}"
                        )
                        try:
                            return register_table(
                                table_id,
                                metadata_path=metadata_location,
                                catalog=self._catalog,
                                fs_client=fs_client,
                                config=self.config.filesystem,
                            )
                        except NoSuchNamespaceError:
                            # create namespace and try again
                            self.initialize_storage()
                            return self.load_open_table("iceberg", table_name)
                    else:
                        logger.info(
                            f"Table metadata at {metadata_location} could not be found and "
                            "registered."
                        )
                else:
                    logger.info(
                        f"Table {table_name} not exists and could not be registered because "
                        "location could not be computed from destination config."
                    )
            # unable to register
            raise

    def is_open_table(self, table_format: TTableFormat, table_name: str) -> bool:
        return table_format == "iceberg"
