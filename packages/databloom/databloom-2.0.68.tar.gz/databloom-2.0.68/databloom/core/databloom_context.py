"""
Main context class for DataBloom SDK.
"""
import logging
import os
from typing import Optional, Dict, Any
import duckdb
from sqlalchemy import create_engine as sqlalchemy_create_engine
from pyspark.sql import SparkSession
import pyspark
from typing import Dict, Optional, Union, Callable

from ..dataset.dataset import Dataset
from ..api.credentials import CredentialsManager
from ..core.connector.mysql import MySQLConnector
from ..core.connector.postgresql import PostgreSQLConnector
from ..core.connector.spark_postgresql import SparkPostgreSQLConnector
from ..core.spark.session import SparkSessionManager
from .lighter_context import LighterContext

logger = logging.getLogger(__name__)

class DataBloomContext:
    """Main context class for DataBloom SDK."""
    
    def __init__(self):
        """Initialize DataBloom context."""
        self._dataset = Dataset()
        self._credentials = CredentialsManager()
        self._duckdb_con = None
        self._attached_sources = {}
        self._connectors = {}
        self._spark_manager = SparkSessionManager()
        self._spark_connectors = {}
        self._lighter_context = None
        
    def get_duck_con(self) -> duckdb.DuckDBPyConnection:
        """Get DuckDB connection."""
        if not self._duckdb_con:
            self._duckdb_con = duckdb.connect(":memory:")
            self._setup_duckdb()
        return self._duckdb_con
        
    def _setup_duckdb(self):
        """Setup DuckDB with required extensions and settings."""
        con = self.get_duck_con()
        
        # Install and load extensions
        con.execute("INSTALL httpfs;")
        con.execute("LOAD httpfs;")
        con.execute("INSTALL iceberg;")
        con.execute("LOAD iceberg;")
        
        # Get S3 credentials from manager
        s3_creds = self._credentials.get_s3_credentials()
        
        # Configure S3 settings
        con.execute(f"SET s3_endpoint='{s3_creds['endpoint']}';")
        con.execute(f"SET s3_region='{s3_creds['region']}';")
        con.execute(f"SET s3_access_key_id='{s3_creds['access_key']}';")
        con.execute(f"SET s3_secret_access_key='{s3_creds['secret_key']}';")
        con.execute("SET s3_url_style='path';")
        con.execute("SET s3_use_ssl=false;")
        con.execute("SET enable_http_metadata_cache=false;")
        con.execute("SET enable_object_cache=false;")
        con.execute("SET s3_uploader_max_parts_per_file=10000;")
        con.execute("SET memory_limit='5GB';")
        con.execute("SET s3_url_compatibility_mode=true;")
        
    def attach_source(self, source: str, dbname: str, dest: str) -> bool:
        """
        Attach a data source to DuckDB.
        
        Args:
            source: Source identifier in format 'type/name'
            dbname: Database name to connect to
            dest: Destination name for the attached source
            
        Returns:
            bool: True if source was attached successfully
        """
        source_type, source_name = source.split("/")
        creds = self._credentials.get_credentials_by_uuid(self._credentials.DEFAULT_UUID, source_type)
        
        if not creds:
            raise ValueError(f"No credentials found for {source}")
            
        try:
            if source_type == "mysql":
                # Install MySQL extension if needed
                self.get_duck_con().execute("INSTALL mysql;")
                self.get_duck_con().execute("LOAD mysql;")
                
                # Create MySQL connector
                connector = MySQLConnector(creds)
                self._connectors[dest] = connector
                
                # Build connection string
                conn_str = (
                    f"host={creds['host']}"
                    f" port={creds['port']}"
                    f" user={creds['user']}"
                    f" password={creds['password']}"
                    f" database={dbname}"
                )
                
                # Attach MySQL database
                self.get_duck_con().execute(f"ATTACH '{conn_str}' AS {dest} (TYPE mysql);")
                self._attached_sources[dest] = {"type": "mysql", "dbname": dbname}
                return True
                
            elif source_type == "postgresql":
                # Install PostgreSQL extension if needed
                self.get_duck_con().execute("INSTALL postgres;")
                self.get_duck_con().execute("LOAD postgres;")
                
                # Create PostgreSQL connector
                connector = PostgreSQLConnector(creds)
                self._connectors[dest] = connector
                
                # Create Spark PostgreSQL connector
                spark_connector = SparkPostgreSQLConnector(self.get_spark_session(), creds)
                self._spark_connectors[dest] = spark_connector
                
                # Build connection string
                conn_str = (
                    f"host={creds['host']}"
                    f" port={creds['port']}"
                    f" user={creds['user']}"
                    f" password={creds['password']}"
                    f" dbname={dbname}"
                )
                
                # Attach PostgreSQL database
                self.get_duck_con().execute(f"ATTACH '{conn_str}' AS {dest} (TYPE postgres);")
                self._attached_sources[dest] = {"type": "postgresql", "dbname": dbname}
                return True
                
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
                
        except Exception as e:
            logger.error(f"Error attaching source {source}: {e}")
            raise
            
    def create_sqlalchemy_engine(self, source: str, database:str="postgres"):
        """
        Create SQLAlchemy engine for database connection.
        
        Args:
            type: Database type ('postgresql' or 'mysql')
            database: Database name to connect to
            
        Returns:
            SQLAlchemy Engine instance
        """
        type = source.split("/")[0]
        if type == "postgresql":
            creds = self._credentials.get_credentials_by_uuid(self._credentials.DEFAULT_UUID, "postgresql")
            if not creds:
                raise ValueError("No PostgreSQL credentials found")
            return sqlalchemy_create_engine(
                f"postgresql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{database}"
            )
        elif type == "mysql":
            creds = self._credentials.get_credentials_by_uuid(self._credentials.DEFAULT_UUID, "mysql")
            if not creds:
                raise ValueError("No MySQL credentials found")
            return sqlalchemy_create_engine(
                f"mysql+pymysql://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{database}"
            )
        else:
            raise ValueError(f"Unsupported database type: {type}")
            
    def get_attached_sources(self) -> Dict[str, Dict[str, str]]:
        """Get dictionary of attached sources."""
        return self._attached_sources
        
    def get_connector(self, dest: str) -> Optional[Any]:
        """
        Get connector instance for an attached source.
        
        Args:
            dest: Destination name of the attached source
            
        Returns:
            Connector instance or None if not found
        """
        return self._connectors.get(dest)
        
    def duckdb_sql(self, query: str):
        """Execute a SQL query with DuckDB."""
        return self._dataset.duck_run_sql(query)
        
    def get_spark_session(self, app_name: str = "DataBloom") -> SparkSession:
        """
        Get or create a Spark session.
        
        Args:
            app_name: Name for the Spark application
            
        Returns:
            SparkSession instance
        """
        return self._spark_manager.get_session(app_name)

    def write_spark_table(self, df: pyspark.sql.DataFrame, source: Optional[str] = None, table: Optional[str] = None, mode: Optional[str] = "append"):
        spark = self.get_spark_session()
        assert table is not None, "Table name is required"
        assert mode in ["overwrite", "append"], "Invalid mode"
        if source is None:
            table = f"nessie.{table}"
            try:
                (df.write
                .format("iceberg")
                .mode(mode)
                .saveAsTable(table))
                logger.info(f"Successfully wrote table {table}")
            except Exception as e:
                logger.error(f"Failed to write table {table}: {str(e)}")
                raise ValueError(f"Failed to write table {table}") from e
            return True

        table_name = f"{source}.{table}"
        df.write.mode(mode).saveAsTable(table)
        return True

    def spark_read_data(self, source: Optional[str] = None, table: Optional[str] = None, query: Optional[str] = None):
        spark = self.get_spark_session()
        if query:
            return spark.sql(query)

        if source.startswith("postgresql/"):
            dbname = table.split(".")[0]
            api_jdbc_url = self._credentials.get_jdbc_credentials_from_env(type='postgresql', dbname=dbname)
        
            # Read from PostgreSQL
            df = spark.read \
                .format("jdbc") \
                .option("url", api_jdbc_url) \
                .option("dbtable", f"{table}") \
                .option("driver", "org.postgresql.Driver") \
                .load()
            return df

        if source is None:
            table = f"nessie.{table}"

        return spark.table(table)
        
    def close(self):
        """Close all connections and resources."""
        if self._duckdb_con:
            self._duckdb_con.close()
            self._duckdb_con = None
            
        if self._spark_manager:
            self._spark_manager.stop_session()

    def run_spark_job(self, code_fn: Callable, mode: str = "cluster", executors: Dict[str, Union[int, float]] = {"num_executors": 4, "cpu": 1, "mem": 1}) -> Optional[dict]:
        """Run a Spark job with specified configuration
        
        Args:
            code_fn: Function containing the Spark code
            mode: Execution mode ("cluster" or "client")
            executors: Dictionary with executor configuration:
                - num_executors: Number of executors
                - cpu: CPU cores per executor
                - mem: Memory per executor in GB
        
        Returns:
            Dictionary containing job results if successful
        """
        if self._lighter_context is None:
            self._lighter_context = LighterContext()
        return self._lighter_context.run_spark_job(code_fn, mode, executors) 