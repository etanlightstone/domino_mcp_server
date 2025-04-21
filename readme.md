# Domino MCP Server for Cursor

This project provides a Model Context Protocol (MCP) server that allows Cursor to interact with the Domino Data Lab platform. It enables you to start and check the status of Domino jobs directly from the Cursor chat interface.

## Features

*   **Run Domino Jobs:** Execute commands (e.g., Python scripts) as jobs within a specified Domino project.
*   **Check Job Status:** Retrieve the status and results of a specific Domino job run.

## Setup

1.  **Clone the Repository:**
    ```bash
    # If you haven't already, clone the repository containing this server
    git clone <your-repo-url>
    cd <repository-directory>
    ```

2.  **Install Dependencies:**
    This server requires Python and the following libraries. Install them using pip:
    ```bash
    pip install fastmcp requests
    ```

3.  **Set Environment Variable:**
    The server needs your Domino API key to authenticate requests. Obtain your API key from your Domino account settings and set it as an environment variable.
    *   **MacOS/Linux:**
        ```bash
        export DOMINO_API_KEY='your_api_key_here'
        ```
    *   **Windows (Command Prompt):**
        ```bash
        set DOMINO_API_KEY=your_api_key_here
        ```
    *   **Windows (PowerShell):**
        ```powershell
        $env:DOMINO_API_KEY = 'your_api_key_here'
        ```
    *Note: You might want to add this export line to your shell profile (e.g., `.zshrc`, `.bashrc`, `.bash_profile`) for persistence.*

4.  **Configure Cursor:**
    To make Cursor aware of this MCP server, you need to configure it. Create or edit the MCP configuration file for your project or globally:
    *   **Project-specific:** Create a file named `.cursor/mcp.json` in the root of your project directory.
    *   **Global:** Create a file named `~/.cursor/mcp.json` in your home directory.

    Add the following JSON configuration to the file, adjusting the `<path_to_script>` to the actual absolute path of the `domino_mcp_server.py` file on your system:

    ```json
    {
      "mcpServers": {
        "domino_server": {
          "command": "python",
          "args": ["<path_to_script>/domino_mcp_server.py"],
          "env": {
            "DOMINO_API_KEY": "${env:DOMINO_API_KEY}" 
          }
        }
      }
    }
    ```
    *Replace `<path_to_script>` with the correct absolute path.*
    *Using `"${env:DOMINO_API_KEY}"` allows Cursor to securely pass the environment variable you set in step 3 to the server process.*

5.  **Restart Cursor:** Restart Cursor completely to load the new MCP configuration.

6.  **Verify:** Go to Cursor Settings -> Context -> Model Context Protocol. You should see "domino_server" listed under Available Tools.

## Usage in Cursor

Once configured, you can interact with the Domino server directly in the Cursor chat:

*   **To run a job:**
    ```
    @domino_server run the command 'python my_script.py --arg value' in the 'my-project-name' project for user 'my-username' with the title 'Running my analysis script'.
    ```
    Or more simply:
    ```
    @domino_server run_domino_job user_name='my-username' project_name='my-project-name' run_command='python my_script.py --arg value' title='My Job Title'
    ```

*   **To check a job status:**
    ```
    @domino_server check the status of run 'run_id_here' in the 'my-project-name' project for user 'my-username'.
    ```
    Or more simply:
    ```
    @domino_server check_domino_job_run_result user_name='my-username' project_name='my-project-name' run_id='run_id_here'
    ```

Cursor's agent will understand your request and use the appropriate tool from the `domino_server`. It will ask for confirmation before executing the tool (unless you have auto-run enabled). The results from the Domino API will be displayed in the chat.

## How it Works

The `domino_mcp_server.py` script uses the `fastmcp` library to define an MCP server. It exposes two functions (`run_domino_job` and `check_domino_job_run_result`) as tools that Cursor can call. These functions make authenticated REST API calls to the Domino platform (`https://cloud-dogfood.domino.tech`) using the provided `DOMINO_API_KEY`.

The server is configured to run using `stdio` transport, meaning Cursor starts and manages the Python script process locally and communicates with it via standard input/output.
