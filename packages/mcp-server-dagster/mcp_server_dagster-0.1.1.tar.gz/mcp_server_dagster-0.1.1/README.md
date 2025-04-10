# mcp-dagster: A Dagster MCP Server

> The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. This repository provides an MCP server for interacting with [Dagster](https://dagster.io/), the data orchestration platform.

## Overview

A Model Context Protocol server that enables AI agents to interact with Dagster instances, explore data pipelines, monitor runs, and manage assets. It serves as a bridge between LLMs and your data engineering workflows.

## Components

### Tools

The server implements several tools for Dagster interaction:

- `list_repositories`: Lists all available Dagster repositories
- `list_jobs`: Lists all jobs in a specific repository
- `list_assets`: Lists all assets in a specific repository
- `recent_runs`: Gets recent Dagster runs (default limit: 10)
- `get_run_info`: Gets detailed information about a specific run
- `launch_run`: Launches a Dagster job run
- `materialize_asset`: Materializes a specific Dagster asset
- `terminate_run`: Terminates an in-progress Dagster run
- `get_asset_info`: Gets detailed information about a specific asset

## Configuration

The server connects to Dagster using these defaults:
- GraphQL endpoint: `http://localhost:3000/graphql`
- Transport: SSE (Server-Sent Events)
- Dependencies: `httpx`

## Quickstart

### Running the Example

1. Start the Dagster instance with your pipeline:
```bash
uv run dagster dev -f ./examples/open-ai-agent/pipeline.py
```

2. Run the MCP server with SSE transport:
```bash
uv run examples/open-ai-agent/run_sse_mcp.py
```

3. Start the agent loop to interact with Dagster:
```bash
uv run ./examples/open-ai-agent/agent.py
```

### Example Interactions

Once the agent is running, you can ask questions like:

- "What assets are available in my Dagster instance and what do they do?"
- "Can you materialize the continent_stats asset and show me the result?"
- "Check the status of recent runs and provide a summary of any failures"
- "Create a new monthly aggregation asset that depends on continent_stats"

The agent will use the MCP server to interact with your Dagster instance and provide answers based on your data pipelines.
