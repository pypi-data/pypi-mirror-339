"""
Module for managing database credentials and connections.
"""
import os
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CredentialsManager:
    """Manages database credentials and connection information."""
    
    DEFAULT_UUID = "FAKEUUID"
    
    def __init__(self):
        """Initialize credentials manager."""
        self._credentials = {}
        self._load_credentials_from_env()
        self._s3_credentials = {
            'endpoint': os.getenv('S3_ENDPOINT', 'localhost:9000'),
            'access_key': os.getenv('S3_ACCESS_KEY_ID', 'admin'),
            'secret_key': os.getenv('S3_SECRET_ACCESS_KEY', 'password'),
            'region': os.getenv('S3_REGION', 'us-east-1')
        }
    
    def _load_credentials_from_env(self):
        """Load credentials from environment variables."""
        # Load PostgreSQL credentials
        logger.info("Loading PostgreSQL credentials from environment")
        postgres_vars = {
            'POSTGRES_HOST': None,
            'POSTGRES_PORT': '5432',  # Default port if not specified
            'POSTGRES_USER': None,
            'POSTGRES_PASSWORD': None
        }
        
        # Check for missing required variables
        missing_vars = []
        for var, default in postgres_vars.items():
            value = os.getenv(var, default)
            if value is None:
                missing_vars.append(var)
                
        if missing_vars:
            logger.warning(f"Missing PostgreSQL environment variables: {missing_vars}")
        else:
            # Create credentials dictionary
            creds = {
                "type": "postgresql",
                "host": os.getenv('POSTGRES_HOST'),
                "port": int(os.getenv('POSTGRES_PORT', '5432')),
                "user": os.getenv('POSTGRES_USER'),
                "password": os.getenv('POSTGRES_PASSWORD')
            }
            
            # Store under FAKEUUID for testing
            self._credentials[f"{self.DEFAULT_UUID}:postgresql"] = creds
            logger.info(f"Loaded PostgreSQL credentials for host: {creds['host']}")

        # Load MySQL credentials
        logger.info("Loading MySQL credentials from environment")
        mysql_vars = {
            'MYSQL_HOST': None,
            'MYSQL_PORT': '3306',  # Default port if not specified
            'MYSQL_USER': None,
            'MYSQL_PASSWORD': None
        }
        
        # Check for missing required variables
        missing_vars = []
        for var, default in mysql_vars.items():
            value = os.getenv(var, default)
            if value is None:
                missing_vars.append(var)
                
        if missing_vars:
            logger.warning(f"Missing MySQL environment variables: {missing_vars}")
        else:
            # Create credentials dictionary
            creds = {
                "type": "mysql",
                "host": os.getenv('MYSQL_HOST'),
                "port": int(os.getenv('MYSQL_PORT', '3306')),
                "user": os.getenv('MYSQL_USER'),
                "password": os.getenv('MYSQL_PASSWORD')
            }
            
            # Store under FAKEUUID for testing
            self._credentials[f"{self.DEFAULT_UUID}:mysql"] = creds
            logger.info(f"Loaded MySQL credentials for host: {creds['host']}")
    
    def get_credentials_by_uuid(self, uuid: str, type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get credentials by UUID and type.
        
        Args:
            uuid: UUID for the credentials
            type: Optional type of credentials to get
            
        Returns:
            Dict containing credential information or None if not found
        """
        if uuid == self.DEFAULT_UUID:
            if type:
                creds = self._credentials.get(f"{uuid}:{type}")
            else:
                # Try to find any credentials for this UUID
                for key, value in self._credentials.items():
                    if key.startswith(f"{uuid}:"):
                        creds = value
                        break
                else:
                    creds = None
                    
            if creds:
                logger.info(f"Found credentials for UUID {uuid} of type {creds.get('type')}")
                return creds
            logger.warning(f"No credentials found for UUID {uuid}")
        elif uuid == "test":
            return {
                "uri": "http://localhost:19120/api/v1",
                "ref": "main",
                "warehouse": "s3a://nessie/",
                "io_impl": "org.apache.iceberg.hadoop.HadoopFileIO"
            }
        return None

    def get_jdbc_credentials_from_env(self, type: Optional[str] = None, dbname: Optional[str] = None) -> str:
        """Get JDBC credentials by source ID."""
        assert type in ["postgresql", "mysql"], "Invalid type"
        if type == "postgresql":
            POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
            POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
            POSTGRES_USER = os.environ.get('POSTGRES_USER')
            POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
            if dbname:
                POSTGRES_DBNAME = dbname
            else:
                POSTGRES_DBNAME = os.environ.get('POSTGRES_DB')
            jdbc_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}?user={POSTGRES_USER}&password={POSTGRES_PASSWORD}"
            return jdbc_url
        elif type == "mysql":
            return f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
        else:
            raise ValueError(f"Invalid type: {type}")
    
    def get_nessie_credentials(self, source_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get Nessie credentials by source ID."""
        if source_id is None:
            source_id = "nessie_source:default"
        if not source_id.startswith("nessie_source:"):
            source_id = f"nessie_source:{source_id}"
        return self._credentials.get(source_id)
    
    def get_postgresql_credentials(self, source_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get PostgreSQL credentials by source ID."""
        if source_id is None:
            source_id = "postgresql_source:default"
        if not source_id.startswith("postgresql_source:"):
            source_id = f"postgresql_source:{source_id}"
        return self._credentials.get(source_id)

    def get_mysql_credentials(self, source_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get MySQL credentials by source ID."""
        if source_id is None:
            source_id = "mysql_source:default"
        if not source_id.startswith("mysql_source:"):
            source_id = f"mysql_source:{source_id}"
        return self._credentials.get(source_id)
    
    def validate_nessie_connection(self, source_id: Optional[str] = None) -> bool:
        """
        Validate Nessie connection using stored credentials.
        
        Args:
            source_id: Optional source ID. If None, validates default credentials
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        creds = self.get_nessie_credentials(source_id)
        if not creds:
            return False
            
        try:
            # Basic validation of required fields
            required_fields = ['uri', 'ref', 'warehouse', 'io_impl']
            return all(field in creds for field in required_fields)
        except Exception:
            return False

    def get_s3_credentials(self) -> Dict[str, str]:
        """
        Get S3 credentials from environment.
        
        Returns:
            Dict containing S3 credentials
        """
        return self._s3_credentials