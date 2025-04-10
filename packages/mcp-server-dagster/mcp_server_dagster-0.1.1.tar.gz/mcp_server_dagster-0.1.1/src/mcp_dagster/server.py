import json
from typing import Any, Dict, List, Optional, Union

import httpx
from mcp.server.fastmcp import FastMCP


class DagsterGraphqlClient:
    """Client for interacting with Dagster GraphQL API"""

    def __init__(self, graphql_url: str = "http://localhost:3000/graphql"):
        self.graphql_url = graphql_url

    async def execute_graphql(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a GraphQL query against the Dagster API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.graphql_url, json={"query": query, "variables": variables or {}}
            )
            return response.json()

    async def list_repositories(self) -> Dict[str, Union[List[Dict[str, str]], str]]:
        """List all available Dagster repositories"""
        query = """
        query {
          repositoriesOrError {
            ... on RepositoryConnection {
              nodes {
                name
                location {
                  name
                }
              }
            }
          }
        }
        """
        result = await self.execute_graphql(query)
        if "errors" in result:
            return {"error": result["errors"][0]["message"]}

        repos = result.get("data", {}).get("repositoriesOrError", {}).get("nodes", [])
        return {
            "repositories": [
                {"name": r["name"], "location": r["location"]["name"]} for r in repos
            ]
        }

    async def list_jobs(
        self, repository_location: str, repository_name: str
    ) -> Dict[str, Any]:
        """List all jobs in a specific repository"""
        query = """
        query JobsQuery($repositoryLocationName: String!, $repositoryName: String!) {
          repositoryOrError(
            repositorySelector: {
              repositoryLocationName: $repositoryLocationName
              repositoryName: $repositoryName
            }
          ) {
            ... on Repository {
              jobs {
                name
                description
              }
            }
          }
        }
        """
        variables = {
            "repositoryLocationName": repository_location,
            "repositoryName": repository_name,
        }

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"error": result["errors"][0]["message"]}

        jobs = result.get("data", {}).get("repositoryOrError", {}).get("jobs", [])
        return {"jobs": jobs}

    async def list_assets(
        self, repository_location: str, repository_name: str
    ) -> Dict[str, Any]:
        """List all assets in a specific repository"""
        query = """
        query AssetsQuery($repositoryLocationName: String!, $repositoryName: String!) {
          repositoryOrError(
            repositorySelector: {
              repositoryLocationName: $repositoryLocationName
              repositoryName: $repositoryName
            }
          ) {
            ... on Repository {
              assetNodes {
                assetKey {
                  path
                }
                description
              }
            }
          }
        }
        """
        variables = {
            "repositoryLocationName": repository_location,
            "repositoryName": repository_name,
        }

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"error": result["errors"][0]["message"]}

        assets = (
            result.get("data", {}).get("repositoryOrError", {}).get("assetNodes", [])
        )
        formatted_assets = []
        for asset in assets:
            key = asset.get("assetKey", {}).get("path", [])
            formatted_assets.append(
                {"asset_key": "/".join(key), "description": asset.get("description")}
            )

        return {"assets": formatted_assets}

    async def get_recent_runs(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent Dagster runs"""
        query = """
        query RecentRunsQuery($limit: Int!) {
          runsOrError(limit: $limit) {
            ... on Runs {
              results {
                runId
                status
                jobName
                startTime
                endTime
              }
            }
          }
        }
        """
        variables = {"limit": limit}

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"error": result["errors"][0]["message"]}

        runs = result.get("data", {}).get("runsOrError", {}).get("results", [])
        return {"runs": runs}

    async def get_run_info(self, run_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific run"""
        query = """
        query RunQuery($runId: ID!) {
          runOrError(runId: $runId) {
            ... on Run {
              runId
              status
              jobName
              startTime
              endTime
              tags {
                key
                value
              }
            }
          }
        }
        """
        variables = {"runId": run_id}

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"error": result["errors"][0]["message"]}

        run = result.get("data", {}).get("runOrError", {})
        return {"run": run}

    async def launch_run(
        self,
        repository_location: str,
        repository_name: str,
        job_name: str,
        run_config: str = "{}",
    ) -> Dict[str, Any]:
        """Launch a Dagster job run"""
        query = """
        mutation LaunchRunMutation(
          $repositoryLocationName: String!
          $repositoryName: String!
          $jobName: String!
          $runConfigData: RunConfigData!
        ) {
          launchRun(
            executionParams: {
              selector: {
                repositoryLocationName: $repositoryLocationName
                repositoryName: $repositoryName
                jobName: $jobName
              }
              runConfigData: $runConfigData
            }
          ) {
            __typename
            ... on LaunchRunSuccess {
              run {
                runId
                status
              }
            }
            ... on RunConfigValidationInvalid {
              errors {
                message
              }
            }
            ... on PythonError {
              message
            }
          }
        }
        """

        try:
            config_data = json.loads(run_config)
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": f"Invalid JSON in run_config: {run_config}",
            }

        variables = {
            "repositoryLocationName": repository_location,
            "repositoryName": repository_name,
            "jobName": job_name,
            "runConfigData": config_data,
        }

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"success": False, "message": result["errors"][0]["message"]}

        launch_result = result.get("data", {}).get("launchRun", {})

        if launch_result.get("__typename") == "LaunchRunSuccess":
            run = launch_result.get("run", {})
            return {
                "success": True,
                "message": f"Run launched successfully with ID: {run.get('runId')} (status: {run.get('status')})",
                "run": run,
            }
        elif launch_result.get("__typename") == "RunConfigValidationInvalid":
            errors = [error.get("message") for error in launch_result.get("errors", [])]
            return {
                "success": False,
                "message": f"Config validation error: {'; '.join(errors)}",
            }
        else:
            return {
                "success": False,
                "message": launch_result.get("message", "Unknown error"),
            }

    async def materialize_asset(
        self, asset_key: str, repository_location: str, repository_name: str
    ) -> Dict[str, Any]:
        """Materialize a specific Dagster asset"""
        # Query to get all jobs in the repository
        jobs_query = """
        query JobsQuery($repositoryLocationName: String!, $repositoryName: String!) {
          repositoryOrError(
            repositorySelector: {
              repositoryLocationName: $repositoryLocationName
              repositoryName: $repositoryName
            }
          ) {
            ... on Repository {
              jobs {
                name
              }
            }
          }
        }
        """

        jobs_variables = {
            "repositoryLocationName": repository_location,
            "repositoryName": repository_name,
        }

        jobs_result = await self.execute_graphql(jobs_query, jobs_variables)
        if "errors" in jobs_result:
            return {"success": False, "message": jobs_result["errors"][0]["message"]}

        jobs = jobs_result.get("data", {}).get("repositoryOrError", {}).get("jobs", [])
        if not jobs:
            return {"success": False, "message": "No jobs found in the repository"}

        asset_job_name = None
        for job in jobs:
            if asset_key in job["name"]:
                asset_job_name = job["name"]
                break

        if not asset_job_name:
            for job in jobs:
                if any(
                    keyword in job["name"].lower()
                    for keyword in ["materialize", "asset", "build"]
                ):
                    asset_job_name = job["name"]
                    break

        if not asset_job_name and jobs:
            asset_job_name = jobs[0]["name"]

        if not asset_job_name:
            return {
                "success": False,
                "message": "Could not determine which job to use for asset materialization",
            }

        launch_query = """
        mutation LaunchRunMutation(
          $repositoryLocationName: String!
          $repositoryName: String!
          $jobName: String!
        ) {
          launchRun(
            executionParams: {
              selector: {
                repositoryLocationName: $repositoryLocationName
                repositoryName: $repositoryName
                jobName: $jobName
              }
            }
          ) {
            __typename
            ... on LaunchRunSuccess {
              run {
                runId
                status
              }
            }
            ... on PythonError {
              message
            }
          }
        }
        """

        launch_variables = {
            "repositoryLocationName": repository_location,
            "repositoryName": repository_name,
            "jobName": asset_job_name,
        }

        launch_result = await self.execute_graphql(launch_query, launch_variables)
        if "errors" in launch_result:
            return {"success": False, "message": launch_result["errors"][0]["message"]}

        run_data = launch_result.get("data", {}).get("launchRun", {})

        if run_data.get("__typename") == "LaunchRunSuccess":
            run = run_data.get("run", {})
            return {
                "success": True,
                "message": f"Job started for asset materialization with run ID: {run.get('runId')} (status: {run.get('status')})",
                "run": run,
            }
        else:
            return {
                "success": False,
                "message": run_data.get("message", "Unknown error"),
            }

    async def terminate_run(self, run_id: str) -> Dict[str, Any]:
        """Terminate an in-progress Dagster run"""
        query = """
        mutation TerminateRunMutation($runId: String!) {
          terminateRun(runId: $runId) {
            __typename
            ... on TerminateRunSuccess {
              run {
                runId
                status
              }
            }
            ... on TerminateRunFailure {
              message
            }
            ... on RunNotFoundError {
              runId
            }
            ... on PythonError {
              message
            }
          }
        }
        """

        variables = {"runId": run_id}

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"success": False, "message": result["errors"][0]["message"]}

        terminate_result = result.get("data", {}).get("terminateRun", {})

        if terminate_result.get("__typename") == "TerminateRunSuccess":
            run = terminate_result.get("run", {})
            return {
                "success": True,
                "message": f"Run {run.get('runId')} terminated successfully (new status: {run.get('status')})",
                "run": run,
            }
        elif terminate_result.get("__typename") == "RunNotFoundError":
            return {
                "success": False,
                "message": f"Run with ID {terminate_result.get('runId')} not found",
            }
        else:
            return {
                "success": False,
                "message": terminate_result.get("message", "Unknown error"),
            }

    async def get_asset_info(self, asset_key: str) -> Dict[str, Any]:
        """Get detailed information about a specific asset"""
        query = """
        query AssetQuery($assetKey: AssetKeyInput!) {
          assetOrError(assetKey: $assetKey) {
            ... on Asset {
              key {
                path
              }
              definition {
                description
              }
            }
            ... on AssetNotFoundError {
              message
            }
          }
        }
        """

        asset_key_parts = asset_key.split("/")
        variables = {"assetKey": {"path": asset_key_parts}}

        result = await self.execute_graphql(query, variables)
        if "errors" in result:
            return {"error": result["errors"][0]["message"]}

        asset_data = result.get("data", {}).get("assetOrError", {})

        if "message" in asset_data:
            return {"error": asset_data["message"]}

        formatted_asset = {
            "asset_key": "/".join(asset_data.get("key", {}).get("path", [])),
            "description": asset_data.get("definition", {}).get("description"),
        }
        jobs_query = """
        query AssetJobsQuery($assetKey: AssetKeyInput!) {
          assetOrError(assetKey: $assetKey) {
            ... on Asset {
              definition {
                jobNames
              }
            }
          }
        }
        """

        jobs_result = await self.execute_graphql(jobs_query, variables)
        if "errors" not in jobs_result:
            jobs_data = (
                jobs_result.get("data", {})
                .get("assetOrError", {})
                .get("definition", {})
            )
            if "jobNames" in jobs_data:
                formatted_asset["materialized_by_jobs"] = jobs_data["jobNames"]

        return formatted_asset


mcp = FastMCP(
    "Dagster Explorer",
    description="A simple MCP server for Dagster",
    dependencies=["httpx"],
)
dagster_client = DagsterGraphqlClient()


@mcp.tool()
async def list_repositories() -> dict:
    """List all available Dagster repositories"""
    return await dagster_client.list_repositories()


@mcp.tool()
async def list_jobs(repository_location: str, repository_name: str) -> dict:
    """List all jobs in a specific repository"""
    return await dagster_client.list_jobs(repository_location, repository_name)


@mcp.tool()
async def list_assets(repository_location: str, repository_name: str) -> dict:
    """List all assets in a specific repository"""
    return await dagster_client.list_assets(repository_location, repository_name)


@mcp.tool()
async def recent_runs(limit: int = 10) -> dict:
    """Get recent Dagster runs"""
    return await dagster_client.get_recent_runs(limit)


@mcp.tool()
async def get_run_info(run_id: str) -> dict:
    """Get detailed information about a specific run"""
    return await dagster_client.get_run_info(run_id)


@mcp.tool()
async def launch_run(
    repository_location: str,
    repository_name: str,
    job_name: str,
    run_config: str = "{}",
) -> dict:
    """Launch a Dagster job run"""
    return await dagster_client.launch_run(
        repository_location, repository_name, job_name, run_config
    )


@mcp.tool()
async def materialize_asset(
    asset_key: str, repository_location: str, repository_name: str
) -> dict:
    """Materialize a specific Dagster asset"""
    return await dagster_client.materialize_asset(
        asset_key, repository_location, repository_name
    )


@mcp.tool()
async def terminate_run(run_id: str) -> dict:
    """Terminate an in-progress Dagster run"""
    return await dagster_client.terminate_run(run_id)


@mcp.tool()
async def get_asset_info(asset_key: str) -> dict:
    """Get detailed information about a specific asset"""
    return await dagster_client.get_asset_info(asset_key)


if __name__ == "__main__":
    # Run with SSE transport
    mcp.run(transport="sse")
