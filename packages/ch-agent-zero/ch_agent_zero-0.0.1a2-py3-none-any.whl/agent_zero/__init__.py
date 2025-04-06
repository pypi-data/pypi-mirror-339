"""Agent Zero package for ClickHouse database management."""

__version__ = '0.0.1a2'

from agent_zero.mcp_server import (
    create_clickhouse_client,
    list_databases,
    list_tables,
    run_select_query,
)

__all__ = ["create_clickhouse_client", "list_databases", "list_tables", "run_select_query"]
