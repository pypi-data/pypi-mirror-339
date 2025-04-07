# DataBloom SDK Client

A Python SDK client for data integration with PostgreSQL, MySQL, Nessie, and S3.

## Quick Start

```bash
# Setup environment
conda create -n data_bloom python=3.9
conda activate data_bloom

# Install
pip install -e ".[dev]"
```

## Configuration

Create `.env` file with your credentials:

```bash
# Database Credentials
POSTGRES_HOST=10.237.96.186
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=8>w[:~WfUYzCL-f3F<p1
POSTGRES_DATABASE=postgres

MYSQL_HOST=10.237.96.186
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=8>w[:~WfUYzCL-f3F<p1
MYSQL_DB=information_schema

# Nessie & S3
NESSIE_URI=http://localhost:19120/api/v1
NESSIE_REF=main

S3_ENDPOINT=localhost:9000
S3_ACCESS_KEY_ID=admin
S3_SECRET_ACCESS_KEY=password
S3_WAREHOUSE=s3a://nessie/
```

## Testing

```bash
# Run all tests
make test

# Test specific components
make test-db          # Database connections
make test-nessie      # Nessie integration
make test-metadata    # Metadata operations

# Run database connection example
make test-db-example
```

## Development

```bash
make format          # Format code
make lint           # Run linter
make doc            # Build docs
```

## License

MIT License
