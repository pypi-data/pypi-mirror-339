import pytest
from unittest.mock import AsyncMock

from mcp_dagster.server import DagsterGraphqlClient


@pytest.fixture
def mock_client():
    client = DagsterGraphqlClient()
    client.execute_graphql = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_list_repositories_success(mock_client):
    # Setup mock response
    mock_client.execute_graphql.return_value = {
        "data": {
            "repositoriesOrError": {
                "nodes": [{"name": "test_repo", "location": {"name": "test_location"}}]
            }
        }
    }

    # Execute method
    result = await mock_client.list_repositories()

    # Assert result
    assert result == {
        "repositories": [{"name": "test_repo", "location": "test_location"}]
    }


@pytest.mark.asyncio
async def test_list_repositories_error(mock_client):
    # Setup mock error response
    mock_client.execute_graphql.return_value = {
        "errors": [{"message": "Connection error"}]
    }

    # Execute method
    result = await mock_client.list_repositories()

    # Assert error is returned
    assert result == {"error": "Connection error"}


@pytest.mark.asyncio
async def test_list_jobs(mock_client):
    # Setup mock response
    mock_client.execute_graphql.return_value = {
        "data": {
            "repositoryOrError": {
                "jobs": [
                    {"name": "job1", "description": "First job"},
                    {"name": "job2", "description": "Second job"},
                ]
            }
        }
    }

    # Execute method
    result = await mock_client.list_jobs("test_location", "test_repo")

    # Assert result
    assert result == {
        "jobs": [
            {"name": "job1", "description": "First job"},
            {"name": "job2", "description": "Second job"},
        ]
    }


@pytest.mark.asyncio
async def test_get_run_info(mock_client):
    # Setup mock response
    mock_client.execute_graphql.return_value = {
        "data": {
            "runOrError": {
                "runId": "test_run_id",
                "status": "SUCCESS",
                "jobName": "test_job",
                "startTime": 1622548800,
                "endTime": 1622549000,
                "tags": [{"key": "tag1", "value": "value1"}],
            }
        }
    }

    # Execute method
    result = await mock_client.get_run_info("test_run_id")

    # Assert result
    assert result == {
        "run": {
            "runId": "test_run_id",
            "status": "SUCCESS",
            "jobName": "test_job",
            "startTime": 1622548800,
            "endTime": 1622549000,
            "tags": [{"key": "tag1", "value": "value1"}],
        }
    }


@pytest.mark.asyncio
async def test_launch_run_success(mock_client):
    # Setup mock response
    mock_client.execute_graphql.return_value = {
        "data": {
            "launchRun": {
                "__typename": "LaunchRunSuccess",
                "run": {"runId": "new_run_id", "status": "STARTED"},
            }
        }
    }

    # Execute method
    result = await mock_client.launch_run(
        "test_location", "test_repo", "test_job", "{}"
    )

    # Assert result
    assert result["success"] is True
    assert "new_run_id" in result["message"]
    assert result["run"] == {"runId": "new_run_id", "status": "STARTED"}


@pytest.mark.asyncio
async def test_launch_run_invalid_config(mock_client):
    # Execute method with invalid JSON
    result = await mock_client.launch_run(
        "test_location", "test_repo", "test_job", "invalid json"
    )

    # Assert error
    assert result["success"] is False
    assert "Invalid JSON" in result["message"]
