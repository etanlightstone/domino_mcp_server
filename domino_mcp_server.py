# MCP Server functions that wrap the Domino API
# Domino API docs, specifically to run a job here: https://docs.dominodatalab.com/en/latest/api_guide/8c929e/rest-api-reference/#_startJob
# how to get your domino project ID: https://support.domino.ai/support/s/article/How-can-I-find-my-Project-ID-and-available-Hardware-Tier-IDs

from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
import requests
import asyncio
import os

# Initialize the Fast MCP server
mcp = FastMCP("domino_server")

# Load API key from environment variable
domino_api_key = os.getenv("DOMINO_API_KEY")
if not domino_api_key:
    raise ValueError("DOMINO_API_KEY environment variable not set.")


@mcp.tool()
async def check_domino_job_run_result(user_name: str, project_name: str, run_id: str) -> Dict[str, Any]:
    """
    The check_domino_job_run_result function checks the status of a job run and retrieves results from the domino data science platform

    Args:
        user_name (str): The user name associated with the Domino Project
        project_name (str): The name of the Domino project.
        run_id (str): The run id of the job run to return the status of
    """
    api_url = f"https://cloud-dogfood.domino.tech/v1/projects/{user_name}/{project_name}/runs/{run_id}"
    headers = {
        "X-Domino-Api-Key": domino_api_key
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()
    except requests.exceptions.RequestException as e:
        result = {"error": f"API request failed: {e}"}
    except Exception as e:
        result = {"error": f"An unexpected error occurred: {e}"}

    return result

@mcp.tool()
async def run_domino_job(user_name: str, project_name: str, run_command: str, title: str) -> Dict[str, Any]:
    """
    The run_domino_job function runs a command as a job on the domino data science platform, typically a python script such a 'python my_script.py --arg1 arv1_val --arg2 arv2_val' on the Domino cloud platform.

    Args:
        user_name (str): The user name associated with the Domino project.
        project_name (str): The name of the Domino project.
        run_command (str): The command to run on the domino platform. Example: 'python my_script.py --arg1 arv1_val --arg2 arv2_val'
        title (str): A title of the job that helps later identify the job. Example: 'running training.py script'
        tier (str | None, optional): The hardware tier to run the job on. Defaults to None (project default).
    """
    ### implementation goes here ###
    # Construct the API URL
    # must be in this format: https://cloud-dogfood.domino.tech/v1/projects/user_name/project_name/runs
    api_url = f"https://cloud-dogfood.domino.tech/v1/projects/{user_name}/{project_name}/runs"

    # Prepare the request headers
    headers = {
        "X-Domino-Api-Key": domino_api_key,
        "Content-Type": "application/json",
    }

    # Prepare the request body according to the specified requirements
    # for the /v1/projects/{user_name}/{project_name}/runs endpoint.
    payload = {
        "command": run_command.split(), # Split the command string into a list
        "isDirect": False, # Matching successful curl command
        "title": title,
        "publishApiEndpoint": False,
    }
    # Conditionally add the tier if provided
    # if tier:
    #     payload["tier"] = tier

    # print(f"API URL: {api_url}")
    # print(f"Headers: {headers}")
    # print(f"Payload: {payload}")

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        # print(f"Response Status Code: {response.status_code}")
        # print(f"Response Headers: {response.headers}")
        # print(f"Response Text: {response.text}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()
    except requests.exceptions.RequestException as e:
        result = {"error": f"API request failed: {e}"}
    except Exception as e:
        result = {"error": f"An unexpected error occurred: {e}"}

    return result

async def main():
    # test project ID: 6806b69e1baf462351041f7f - No longer needed directly in the function call
    print("making domino API call")
    result = await run_domino_job(user_name='etan_lightstone', project_name='diabetes-predict', run_command='python diabetes_model.py', title='run2 test of diabetes model')
    #result = await check_domino_job_run_result(user_name='etan_lightstone', project_name='diabetes-predict', run_id='6806c7e01baf462351041f9a')
    print(result)

if __name__ == "__main__":
    # Initialize and run the server using stdio transport
    mcp.run(transport='stdio') 
    #asyncio.run(main())