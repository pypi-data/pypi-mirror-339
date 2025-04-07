"""
Spark session management for DataBloom SDK.
"""
import os
import logging
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

logger = logging.getLogger(__name__)

class SparkSessionManager:
    """Manager class for Spark session."""
    
    def __init__(self):
        """Initialize Spark session manager."""
        self._session = None
        
    def get_session(self, app_name: str = "DataBloom") -> SparkSession:
        """
        Get or create a Spark session.
        
        Args:
            app_name: Name for the Spark application
            
        Returns:
            SparkSession instance
        """
        if not self._session:
            try:
                # Get environment variables
                nessie_uri = os.getenv("NESSIE_URI")
                
                # Create Spark session builder with packages
                packages = [
                    # Nessie + s3 with iceberg
                    "org.projectnessie.nessie-integrations:nessie-spark-extensions-3.5_2.12:0.99.0",
                    "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.0",
                    "software.amazon.awssdk:bundle:2.28.17",
                    "software.amazon.awssdk:url-connection-client:2.28.17",
                    # Postgresql
                    "org.postgresql:postgresql:42.2.5"

                ]
                
                # Create Spark configuration
                conf = SparkConf()
                conf.set("spark.app.name", app_name)
                conf.set("spark.master", "local[*]")
                conf.set("spark.jars.packages", ",".join(packages))
                conf.set("spark.sql.extensions", 
                        "org.projectnessie.spark.extensions.NessieSparkSessionExtensions,org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
                conf.set("spark.sql.catalog.nessie", "org.apache.iceberg.spark.SparkCatalog")
                conf.set("spark.sql.catalog.nessie.type", "rest")
                conf.set("spark.sql.catalog.nessie.uri", nessie_uri)
                conf.set("spark.sql.catalogImplementation", "in-memory")
                
                # Create session
                self._session = SparkSession.builder \
                    .config(conf=conf) \
                    .enableHiveSupport() \
                    .getOrCreate()
                self._session.sparkContext.setLogLevel("WARN")
                
                # Create default namespace if it doesn't exist
                try:
                    self._session.sql("CREATE NAMESPACE IF NOT EXISTS nessie.default")
                    logger.info("Default namespace created or already exists")
                except Exception as e:
                    logger.warning(f"Failed to create default namespace: {e}")
                
                logger.info("Successfully created Spark session")
                
            except Exception as e:
                logger.error(f"Failed to create Spark session: {e}")
                raise
                
        return self._session
        
    def stop_session(self):
        """Stop the Spark session if it exists."""
        if self._session:
            try:
                self._session.stop()
                self._session = None
                logger.info("Successfully stopped Spark session")
            except Exception as e:
                logger.error(f"Failed to stop Spark session: {e}")
                raise 