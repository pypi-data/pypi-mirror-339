from typing import Dict, List

from mcp.server.fastmcp import FastMCP
from requests.exceptions import HTTPError

from gibson.api.DataApi import DataApi
from gibson.api.ProjectApi import ProjectApi
from gibson.core.Configuration import Configuration

mcp = FastMCP("GibsonAI")

# Note: Resources are not yet supported by Cursor, everything must be implemented as a tool
# See https://docs.cursor.com/context/model-context-protocol#limitations


@mcp.tool()
def get_projects() -> List[Dict]:
    """Get all GibsonAI projects"""
    project_api = ProjectApi(Configuration())
    try:
        return project_api.list()
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def create_project() -> Dict:
    """Create a new GibsonAI project"""
    project_api = ProjectApi(Configuration())
    try:
        return project_api.create()
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def get_project_details(uuid: str) -> Dict:
    """Get a GibsonAI project's details"""
    project_api = ProjectApi(Configuration())
    try:
        return project_api.lookup(uuid=uuid)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def get_project_hosted_api_details(uuid: str) -> str:
    """
    Get a GibsonAI project's hosted API details
    This includes necessary context for an LLM to understand and generate API calls related to fetching or modifying the project's data
    """
    project_api = ProjectApi(Configuration())
    try:
        return project_api.mcp(uuid=uuid)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def update_project(uuid: str, project_name: str) -> Dict:
    """
    Update a GibsonAI project's details
    This currently only updates the project's name
    Returns the updated project details
    """
    project_api = ProjectApi(Configuration())
    try:
        return project_api.update(uuid=uuid, name=project_name)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def submit_data_modeling_request(uuid: str, data_modeling_request: str) -> Dict:
    """
    Submit a data modeling request for a GibsonAI project
    This tool fully handles all data modeling, you should provide the user's request as-is
    Returns the response from the LLM
    """
    project_api = ProjectApi(Configuration())
    try:
        return project_api.submit_message(uuid=uuid, message=data_modeling_request)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def deploy_project(uuid: str) -> None:
    """
    Deploy a GibsonAI project's hosted databases
    This deploys both the development and production databases simultaneously and automatically handles the migrations
    """
    project_api = ProjectApi(Configuration())
    try:
        return project_api.deploy(uuid=uuid)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def get_project_schema(uuid: str) -> str:
    """
    Get the schema for a GibsonAI project
    This includes any changes made to the schema since the last deployment
    """
    project_api = ProjectApi(Configuration())
    try:
        return project_api.schema(uuid=uuid)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def get_deployed_schema(uuid: str) -> str:
    """
    Get the deployed schema for a GibsonAI project
    This is the schema that is currently live on the project's hosted databases
    """
    project_api = ProjectApi(Configuration())
    try:
        return project_api.database_schema(uuid=uuid)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}


@mcp.tool()
def query_database(api_key: str, query: str) -> List[Dict] | None | Dict:
    """
    Query a GibsonAI project's hosted database using SQL
    Note: the environment-specific API key must be provided
    """
    data_api = DataApi(Configuration(), api_key=api_key)
    try:
        return data_api.query(query=query)
    except HTTPError as e:
        return {"status_code": e.response.status_code, "error": e.response.json()}
