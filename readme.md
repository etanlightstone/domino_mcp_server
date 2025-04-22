# Domino MCP Server for Cursor

This project provides a Model Context Protocol (MCP) server that allows Cursor to interact with the Domino Data Lab platform. It enables you to start and check the status of Domino jobs directly from the Cursor chat interface.

## Features

*   **Run Domino Jobs:** Execute commands (e.g., Python scripts) as jobs within a specified Domino project.
*   **Check Job Status:** Retrieve the status and results of a specific Domino job run.

## Setup

1.  **Clone the Repository:**
    ```bash
    # If you haven't already, clone the repository containing this server
    git clone https://github.com/etanlightstone/domino_mcp_server.git
    cd domino_mcp_server
    ```

2.  **Install Dependencies:**
    This server requires Python and the `fastmcp` and `requests` libraries. Ensure you have `uv` installed ([https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)). Install the dependencies using `uv`:
    ```bash
    uv pip install -e .
    ```

3.  **Set API Key using .env file:**
    The server needs your Domino API key to authenticate requests. Obtain your API key from your Domino account settings. Create a file named `.env` in the root directory of this project (the same directory as `domino_mcp_server.py`) and add the following line, replacing `'your_api_key_here'` with your actual key:
    ```dotenv
    DOMINO_API_KEY='your_api_key_here'
    ```
    *Note: Ensure `.env` is added to your `.gitignore` file to prevent accidentally committing your API key.*

4.  **Configure Cursor:**
    To make Cursor aware of this MCP server, you need to configure it. Create or edit the MCP configuration file for your project or globally:
    *   **Project-specific:** Create a file named `.cursor/mcp.json` in the root of your project directory.
    *   **Global:** Create a file named `~/.cursor/mcp.json` in your home directory.

    Add the following JSON configuration to the file, adjusting the `<path_to_directory>` to the actual absolute path of the directory containing the `domino_mcp_server.py` script and your `.env` file:

   ```json
        {
            "mcpServers": {
                "domino_server": {
                "command": "uv",
                "args": [
                    "--directory",
                    "/Users/etan.lightstone/Documents/code_projects/domino_mcp_server",
                    "run",
                    "domino_mcp_server.py"
                ] 
                }
            }
        }
   ```
    *Replace `<path_to_directory>` with the correct absolute path to the folder containing `domino_mcp_server.py` and `.env`.*
    *`uv run` will automatically load the `DOMINO_API_KEY` from the `.env` file located in the specified directory.*

5.  **Restart Cursor:** Restart Cursor completely to load the new MCP configuration.

6.  **Verify:** Go to Cursor Settings -> Context -> Model Context Protocol. You should see "domino_server" listed under Available Tools.

## Usage in Cursor

Once the MCP server is configured, add two files to your datascience project. First add a cursor rule:
*cursor/rules/domino-project-rule.mdc*  (SET TO ALWAYS)

You are a Domino Data Lab powered agentic coding tool that helps write code in addition to running tasks on the Domino Data Lab platform on behalf of the user using available tool functions provided by the domino_server MCP server. Including functions like domino_server. Whenever possible run commands as domino jobs rather than on the local terminal. 

The domino project name and user name are required and available in a file called domino_project_settings.md which need to be used in most tool calls by the agentic assistant.

When running a job, always check its status and return any conclusions from the result of the job run.

*domino_project_settings.md* (in your main project folder)

# Domino project settings to use with the mcp server domino_server and its job runner functions
project_name="diabetes-predict"
user_name="etan_lightstone"

Once configured, you can interact with the Domino server directly in the Cursor chat:

*   **To run a job:**
    ```
    Run the script train_my_model.py and pipe the results into a results.txt file. Check that the job run executed correctly afterwards.
    ```

    ```
    Read how the domino_trainer.py is called and run two seperate jobs, one using a larger neural net and the other smaller, both can be 20 epochs.
    ```
*   

Cursor's agent will understand your request and use the appropriate tool from the `domino_server`. It will ask for confirmation before executing the tool (unless you have auto-run enabled). The results from the Domino API will be displayed in the chat.

## How it Works

The `domino_mcp_server.py` script uses the `fastmcp` library to define an MCP server. It exposes two functions (`run_domino_job` and `check_domino_job_run_result`) as tools that Cursor can call. These functions make authenticated REST API calls to the Domino platform (`https://cloud-dogfood.domino.tech`) using the `DOMINO_API_KEY` loaded from the `.env` file (local to the mcp server not your cursor project).

The server is configured to run using `stdio` transport, meaning Cursor starts and manages the Python script process locally (using `uv run`) and communicates with it via standard input/output.
