import os

profile_name = os.environ.get("ICEBERG_MCP_PROFILE") or 'demo'
region = os.environ.get("ICEBERG_AWS_REGION") or 'us-east-1'