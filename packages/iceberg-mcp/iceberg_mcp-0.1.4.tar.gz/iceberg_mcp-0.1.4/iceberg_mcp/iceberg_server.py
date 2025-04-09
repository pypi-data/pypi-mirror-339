from typing import Any, TypedDict

import boto3
import httpx
from fastmcp import Context
from mcp.server.fastmcp import FastMCP
from pyiceberg.catalog import Catalog
from pyiceberg.catalog.glue import GlueCatalog

# Initialize FastMCP server
mcp = FastMCP("iceberg-mcp", "Iceberg MCP Server", version="0.1.0")


class SchemaField(TypedDict):
    id: int
    name: str
    type: str
    required: bool
    doc: str | None


class TableProperties(TypedDict):
    total_size_in_bytes: int
    total_records: int


@mcp.tool()
def get_namespaces() -> str:
    """Provides a list of namespaces from the Glue catalog."""
    catalog = get_catalog()
    namespaces = catalog.list_namespaces()
    return "\n".join(ns[0] for ns in namespaces)


@mcp.tool()
def get_iceberg_tables(namespace: str) -> str:
    """Provides a list of iceberg tables from the Glue catalog for a given namespace"""
    catalog = get_catalog()
    tables = catalog.list_tables(namespace)
    print(tables)
    return "\n".join(t[1] for t in tables)


@mcp.tool()
def get_table_schema(
        full_table_name: str,
) -> list[SchemaField]:
    catalog: Catalog = get_catalog()
    table_obj = catalog.load_table(full_table_name)
    schema = table_obj.schema()

    fields = []
    for field in schema.fields:
        fields.append(
            {
                "id": field.field_id,
                "name": field.name,
                "type": str(field.field_type),
                "required": field.required,
                "doc": field.doc if field.doc else None,
            }
        )

    return fields


@mcp.tool()
def get_table_properties(
        full_table_name: str,
) -> TableProperties:
    catalog: Catalog = get_catalog()
    table_obj = catalog.load_table(full_table_name)
    current_snapshot = table_obj.current_snapshot()
    return TableProperties(total_size_in_bytes=current_snapshot.summary['total-files-size'],
                           total_records=current_snapshot.summary['total-records'])


def get_catalog() -> GlueCatalog:
    session = boto3.Session(profile_name='demo')
    credentials = session.get_credentials().get_frozen_credentials()

    catalog = GlueCatalog("glue", **{
        "client.access-key-id": credentials.access_key,
        "client.secret-access-key": credentials.secret_key,
        "client.session-token": credentials.token,
        "client.region": "us-east-1"
    })
    return catalog

def main() -> None:
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()