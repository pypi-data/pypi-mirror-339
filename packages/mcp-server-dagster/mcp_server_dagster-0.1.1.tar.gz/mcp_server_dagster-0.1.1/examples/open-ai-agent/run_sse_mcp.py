from mcp_dagster.server import mcp

if __name__ == "__main__":
    mcp.run(transport="sse")
