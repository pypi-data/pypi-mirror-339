"""
Core context class for DataBloom SDK.
"""
import logging
import os
from typing import Optional, Dict, Any
import duckdb
from sqlalchemy import create_engine as sqlalchemy_create_engine
from pyspark.sql import SparkSession
import pyspark

from ..dataset.dataset import Dataset
from ..api.credentials import CredentialsManager
from ..core.connector.mysql import MySQLConnector
from ..core.connector.postgresql import PostgreSQLConnector
from ..core.connector.spark_postgresql import SparkPostgreSQLConnector
from ..core.spark.session import SparkSessionManager

logger = logging.getLogger(__name__)
#!/usr/bin/env python3
import requests
import json
import time
from pathlib import Path
from typing import Dict, Optional, Union, Callable
import inspect
import random

class LighterContext:
    def __init__(self, base_url: str = "http://localhost:8080/lighter/api"):
        """Initialize LighterContext with API URL and namespace"""
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "X-Compatibility-Mode": "sparkmagic"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request to Lighter API"""
        url = f"{self.base_url}/{endpoint}"
        print(f"\nMaking {method} request to: {url}")
        print(f"Headers: {self.session.headers}")
        if 'json' in kwargs:
            print(f"Request data: {json.dumps(kwargs['json'], indent=2)}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response content: {response.text}")
            
            response.raise_for_status()
            return response.json() if response.content else None
            
        except requests.exceptions.RequestException as e:
            print(f"\nError making request:")
            print(f"  URL: {url}")
            print(f"  Method: {method}")
            print(f"  Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Status code: {e.response.status_code}")
                print(f"  Response headers: {dict(e.response.headers)}")
                print(f"  Response content: {e.response.text}")
            raise

    def _create_session(self):
        """Create a new Spark session"""
        config = {
            "kind": "pyspark",
            "name": "PySpark Job",
            "conf": {
                "spark.kubernetes.container.image": "registry.ird.vng.vn/databloom/databloom-worker:v2.0.61",
                "spark.kubernetes.executor.container.image": "registry.ird.vng.vn/databloom/databloom-worker:v2.0.61",
                "spark.kubernetes.authenticate.driver.serviceAccountName": "default",
                "spark.kubernetes.container.image.pullPolicy": "Always",
                "spark.kubernetes.container.image.pullSecrets": "harbor-registry",
                "spark.kubernetes.driver.container.image.pullSecrets": "harbor-registry",
                "spark.kubernetes.executor.container.image.pullSecrets": "harbor-registry",
                "spark.executor.instances": "4",
                "spark.executor.memory": "1g",
                "spark.executor.cores": "1",
                "spark.driver.memory": "1g",
                "spark.driver.cores": "1",
                "spark.kubernetes.namespace": "namvq",
                "spark.dynamicAllocation.enabled": "false"
            }
        }
        
        print("\nCreating new Spark session...")
        response = self._request("POST", "sessions", json=config)
        
        if not response or 'id' not in response:
            print("Failed to get session ID from response")
            print(f"Response: {response}")
            raise Exception("Failed to create session")
        
        session_id = response['id']
        print(f"Session created with ID: {session_id}")
        return session_id

    def _wait_for_session(self, session_id: str, timeout: int = 300) -> bool:
        """Wait for session to be ready"""
        print(f"\nWaiting for session {session_id} to be ready...")
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            try:
                session = self._request("GET", f"sessions/{session_id}")
                state = session.get("state", "").lower()
                print(f"Session state: {state}")
                print(f"Full session info: {json.dumps(session, indent=2)}")
                
                if state == "idle":
                    print("Session is ready")
                    return True
                if state in ["error", "dead", "killed"]:
                    print(f"Session failed with state: {state}")
                    print(f"Session details: {json.dumps(session, indent=2)}")
                    raise Exception(f"Session failed: {state}")
                
                print(f"Waiting for session... (state: {state})")
                time.sleep(5)
                
            except Exception as e:
                print(f"Error checking session state: {str(e)}")
                raise
        
        raise TimeoutError("Session startup timed out")
    
    def _wait_for_completion(self, session_id: str, statement_id: str, timeout: int = 300) -> dict:
        """Wait for statement execution to complete"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            result = self._request("GET", f"sessions/{session_id}/statements/{statement_id}")
            state = result.get("state", "").lower()
            
            # Print output if available
            output = result.get("output", {})
            if output:
                if output.get("data", {}).get("text/plain"):
                    print(f"Output: {output['data']['text/plain']}")
                if output.get("traceback"):
                    print(f"Error: {''.join(output['traceback'])}")
            
            if state == "available":
                return result
            if state in ["error", "cancelled"]:
                if output and output.get("traceback"):
                    print(f"Error: {''.join(output['traceback'])}")
                raise Exception(f"Statement failed: {state}")
            
            print(f"Statement state: {state}")
            time.sleep(2)
        raise TimeoutError("Statement execution timed out")

    def run_spark_job(
        self,
        code_fn: Union[str, Callable],
        mode: str = "cluster",
        executors: Dict[str, Union[int, float]] = {"num_executors": 4, "cpu": 1, "mem": 1}
    ) -> Optional[dict]:
        """Run a Spark job with specified configuration
        
        Args:
            code_fn: Either a file path or a function containing the Spark code
            mode: Execution mode ("cluster" or "client")
            executors: Dictionary with executor configuration:
                - num_executors: Number of executors
                - cpu: CPU cores per executor
                - mem: Memory per executor in GB
        
        Returns:
            Dictionary containing job results if successful
        """
        if mode not in ["cluster", "client"]:
            raise ValueError("Mode must be either 'cluster' or 'client'")

        # Create session configuration
        config = {
            "kind": "pyspark",
            "name": "PySpark Job",
            "numExecutors": executors["num_executors"],
            "executorMemory": f"{executors['mem']}g",
            "conf": {
                "spark.kubernetes.namespace": "namvq",
                "spark.kubernetes.container.image": "registry.ird.vng.vn/databloom/databloom-worker:v2.0.61",
                "spark.driver.memory": "1g",
                "spark.executor.memory": f"{executors['mem']}g",
                "spark.executor.instances": str(executors["num_executors"]),
                "spark.executor.cores": str(executors["cpu"]),
                "spark.driver.cores": "1",
                "spark.dynamicAllocation.enabled": "false"
            }
        }
        
        try:
            # Create session
            print(f"Creating Spark session with {executors['num_executors']} executors...")
            session_id = self._create_session()
            
            # Handle code based on type
            if callable(code_fn):
                # Get function source
                code = inspect.getsource(code_fn)
                
                # Create a temporary file with the code
                tmp_file = Path(f"/tmp/{session_id}.py")
                
                # Extract the function body (everything between try and finally)
                code_lines = code.split('\n')
                try_start = code_lines.index('    try:')
                finally_start = code_lines.index('    finally:')
                function_body = code_lines[try_start + 1:finally_start]
                
                # Process the function body to maintain proper indentation
                processed_lines = []
                for line in function_body:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    if 'def ' in line:  # Function definition
                        processed_lines.append('    ' + stripped)
                    elif line.strip().startswith(('return', 'x =', 'y =')):  # Function body
                        processed_lines.append('        ' + stripped)
                    else:  # Regular lines
                        processed_lines.append('    ' + stripped)
                
                # Create the final code structure
                final_code = f"""#!/usr/bin/env python3
import random
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \\
    .appName("Calculate Pi") \\
    .getOrCreate()

try:
{chr(10).join(processed_lines)}
finally:
    spark.stop()
"""
                # Write to temporary file
                print(f"Writing code to temporary file: {tmp_file}")
                tmp_file.write_text(final_code)
                print("Code written to file:")
                print("-" * 40)
                print(final_code)
                print("-" * 40)
                
                code = final_code
            else:
                # Read from file
                if not Path(code_fn).exists():
                    raise FileNotFoundError(f"Code file not found: {code_fn}")
                with open(code_fn) as f:
                    code = f.read()
            
            # Wait for session to be ready
            self._wait_for_session(session_id)
            
            # Submit code
            print("Submitting code...")
            statement = self._request(
                "POST",
                f"sessions/{session_id}/statements",
                json={"code": code, "kind": "pyspark"}
            )
            
            # Wait for completion and get results
            result = self._wait_for_completion(session_id, statement["id"])
            print("Job completed successfully")
            return result
            
        except Exception as e:
            print(f"Error running job: {str(e)}")
            raise
        finally:
            # Cleanup
            if "session_id" in locals():
                print("Cleaning up session...")
                try:
                    # Clean up temporary file if it exists
                    if callable(code_fn):
                        tmp_file = Path(f"/tmp/{session_id}.py")
                        if tmp_file.exists():
                            tmp_file.unlink()
                            print(f"Removed temporary file: {tmp_file}")
                    
                    # Delete session
                    try:
                        self._request("DELETE", f"sessions/{session_id}")
                        print("Session cleaned up")
                    except:
                        pass
                except Exception as e:
                    print(f"Cleanup error: {str(e)}")


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
